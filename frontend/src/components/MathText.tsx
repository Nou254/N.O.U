import katex from 'katex'
import 'katex/dist/katex.min.css'

/**
 * Render a LaTeX fragment as HTML using KaTeX. `throwOnError: false` means
 * invalid math falls back to a readable plain-text rendering instead of an
 * exception. KaTeX escapes all input, so this is safe to inject via
 * dangerouslySetInnerHTML (no script execution possible).
 */
function renderLatex(latex: string, displayMode = false): string {
  try {
    return katex.renderToString(latex, {
      throwOnError: false,
      displayMode,
      strict: false,
    })
  } catch {
    return latex
  }
}

interface MathTextProps {
  text?: string | null
  className?: string
}

/**
 * Renders a string, converting any `$...$` delimited segments into rendered
 * math. Everything outside the delimiters is rendered as plain text.
 */
const MathText = ({ text, className }: MathTextProps) => {
  if (!text) return null

  const parts = String(text).split(/(\$[^$]+\$)/g)

  return (
    <span className={className}>
      {parts.map((part, i) => {
        if (part.startsWith('$') && part.endsWith('$') && part.length > 2) {
          const latex = part.slice(1, -1)
          return (
            <span
              key={i}
              className="math-inline"
              dangerouslySetInnerHTML={{ __html: renderLatex(latex) }}
            />
          )
        }
        return <span key={i}>{part}</span>
      })}
    </span>
  )
}

export default MathText
