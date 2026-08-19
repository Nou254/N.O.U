"""
CV text extraction - pure standard library.

Extracts plain text from an uploaded CV (PDF / DOCX / TXT / DOC) using only
the Python standard library so no extra dependencies are required:

- .txt  -> read as UTF-8 (fallback latin-1/replace)
- .docx -> it is a ZIP of XML; walk word/document.xml for <w:t> runs
- .pdf  -> decompress FlateDecode streams (zlib) and pull the text out of
           BT/ET blocks (Tj / TJ operators) - best effort for text PDFs
- .doc  -> legacy binary; best effort: keep printable ASCII/UTF-8 runs

Scanned/image PDFs have no text layer; in that case the extractor returns an
empty string and the admin is told the CV has no extractable text.
"""

import os
import re
import zipfile
import zlib
import xml.etree.ElementTree as ET

DOCX_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# PDF text-showing operators we can extract from.
_PDF_TEXT_RE = re.compile(rb"\((?:[^()\\]|\\.)*\)|\[(?:[^\[\]\\]|\\.)*\]\s*TJ")


def _read_bytes(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()


def _extract_text_file(file_path: str) -> str:
    """Plain text (and legacy .doc best-effort: printable runs)."""
    data = _read_bytes(file_path)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            text = data.decode("utf-16-le")
        except UnicodeDecodeError:
            text = data.decode("latin-1", errors="replace")
    # Keep printable characters and sensible whitespace.
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\x80-\uFFFF]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_docx(file_path: str) -> str:
    try:
        with zipfile.ZipFile(file_path) as zf:
            xml_bytes = zf.read("word/document.xml")
    except (KeyError, zipfile.BadZipFile):
        return ""
    root = ET.fromstring(xml_bytes)
    paragraphs = []
    for para in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        runs = [
            node.text or ""
            for node in para.iter(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"
            )
        ]
        text = "".join(runs).strip()
        if text:
            paragraphs.append(text)
    return "\n".join(paragraphs)


def _pdf_streams(data: bytes):
    """Yield decompressed PDF object streams (FlateDecode)."""
    # Object streams look like: stream ... endstream
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.DOTALL):
        raw = match.group(1)
        try:
            if raw.startswith(b"\x78\x9c") or b"FlateDecode" in data[max(0, match.start() - 200): match.start()]:
                yield zlib.decompress(raw)
        except zlib.error:
            pass


def _extract_pdf(file_path: str) -> str:
    data = _read_bytes(file_path)
    chunks = []
    for stream in _pdf_streams(data):
        # Pull text-showing operators from the decompressed content stream.
        for token in _PDF_TEXT_RE.findall(stream):
            if token.endswith(b"TJ"):
                # Array of (string, number) - take the strings.
                for part in re.finditer(rb"\((?:[^()\\]|\\.)*\)", token):
                    chunks.append(part.group(0)[1:-1])
            else:
                chunks.append(token[1:-1])  # strip parentheses
    if not chunks:
        # Fall back to any readable text in the raw bytes (uncompressed PDFs).
        for token in _PDF_TEXT_RE.findall(data):
            chunks.append(token[1:-1] if not token.endswith(b"TJ") else token)
    if not chunks:
        return ""
    # Unescape PDF string escapes.
    out = []
    for raw in chunks:
        s = raw.decode("latin-1")
        s = (
            s.replace(r"\(", "(")
            .replace(r"\)", ")")
            .replace(r"\\", "\\")
            .replace(r"\n", " ")
            .replace(r"\r", " ")
            .replace(r"\t", " ")
        )
        out.append(s)
    text = " ".join(out)
    text = re.sub(r"\s+", " ", text)
    # Try to recover line boundaries heuristically (PDF has no line info here).
    return text.strip()


def extract_cv_text(file_path: str) -> str:
    """Return the plain text of a CV at ``file_path`` (best effort)."""
    if not file_path or not os.path.isfile(file_path):
        return ""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".docx":
            return _extract_docx(file_path)
        if ext == ".pdf":
            return _extract_pdf(file_path)
        return _extract_text_file(file_path)
    except Exception:  # noqa: BLE001 - a CV is never allowed to break the API
        return ""
