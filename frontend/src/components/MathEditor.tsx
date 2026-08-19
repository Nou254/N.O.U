import { useRef } from 'react'
import katex from 'katex'
import 'katex/dist/katex.min.css'

/**
 * The symbol palette offered to applicants while answering Mathematics
 * questions. Each entry inserts the given LaTeX snippet at the cursor.
 */
const SYMBOLS: { label: string; latex: string; title?: string }[] = [
  { label: 'x²', latex: '^{2}', title: 'Superscript / power' },
  { label: 'xₙ', latex: '_{n}', title: 'Subscript' },
  { label: '√', latex: '\\sqrt{ }', title: 'Square root' },
  { label: '∛', latex: '\\sqrt[3]{ }', title: 'Cube root' },
  { label: '⅟', latex: '\\frac{a}{b}', title: 'Fraction' },
  { label: 'π', latex: '\\pi', title: 'Pi' },
  { label: '∑', latex: '\\sum_{i=1}^{n}', title: 'Summation' },
  { label: '∫', latex: '\\int_{a}^{b}', title: 'Integral' },
  { label: 'lim', latex: '\\lim_{x \\to \\infty}', title: 'Limit' },
  { label: '±', latex: '\\pm', title: 'Plus-minus' },
  { label: '×', latex: '\\times', title: 'Multiply' },
  { label: '÷', latex: '\\div', title: 'Divide' },
  { label: '≤', latex: '\\leq', title: 'Less than or equal' },
  { label: '≥', latex: '\\geq', title: 'Greater than or equal' },
  { label: '≠', latex: '\\neq', title: 'Not equal' },
  { label: '≈', latex: '\\approx', title: 'Approximately' },
  { label: '∞', latex: '\\infty', title: 'Infinity' },
  { label: '°', latex: '^{\\circ}', title: 'Degrees' },
  { label: '%', latex: '\\%', title: 'Percent' },
  { label: 'α', latex: '\\alpha', title: 'Alpha' },
  { label: 'β', latex: '\\beta', title: 'Beta' },
  { label: 'θ', latex: '\\theta', title: 'Theta' },
  { label: 'λ', latex: '\\lambda', title: 'Lambda' },
  { label: 'Δ', latex: '\\Delta', title: 'Delta' },
  { label: '∀', latex: '\\forall', title: 'For all' },
  { label: '∃', latex: '\\exists', title: 'There exists' },
  { label: '∈', latex: '\\in', title: 'Element of' },
  { label: '⊆', latex: '\\subseteq', title: 'Subset of' },
  { label: '∪', latex: '\\cup', title: 'Union' },
  { label: '∩', latex: '\\cap', title: 'Intersection' },
  { label: '∅', latex: '\\emptyset', title: 'Empty set' },
  { label: '→', latex: '\\rightarrow', title: 'Implies' },
  { label: '⇒', latex: '\\Rightarrow', title: 'Logical implication' },
  { label: '⇔', latex: '\\Leftrightarrow', title: 'Logical equivalence' },
  { label: '¬', latex: '\\neg', title: 'Logical NOT' },
  { label: '∧', latex: '\\land', title: 'Logical AND' },
  { label: '∨', latex: '\\lor', title: 'Logical OR' },
  { label: '⊕', latex: '\\oplus', title: 'XOR' },
  { label: '⊗', latex: '\\otimes', title: 'Tensor product' },
  { label: 'sin', latex: '\\sin x', title: 'Sine' },
  { label: 'cos', latex: '\\cos x', title: 'Cosine' },
  { label: 'tan', latex: '\\tan x', title: 'Tangent' },
  { label: 'log', latex: '\\log_{b} x', title: 'Logarithm' },
  { label: 'ln', latex: '\\ln x', title: 'Natural log' },
  { label: 'e', latex: 'e^{x}', title: 'Exponential' },
  { label: '|x|', latex: '\\left| x \\right|', title: 'Absolute value' },
  { label: '( )', latex: '\\left(  \\right)', title: 'Parentheses' },
  { label: '[ ]', latex: '\\left[  \\right]', title: 'Brackets' },
]

interface MathEditorProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  rows?: number
  disabled?: boolean
}

/**
 * Text editor for mathematical answers. Provides:
 *  - a LaTeX symbol palette (click to insert at the cursor),
 *  - a live rendered preview of the answer below the textarea,
 *  - plain text as a fallback when no LaTeX is used.
 */
const MathEditor = ({ value, onChange, placeholder, rows = 10, disabled }: MathEditorProps) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const insertSymbol = (latex: string) => {
    if (disabled) return
    const el = textareaRef.current
    const current = value || ''
    const start = el?.selectionStart ?? current.length
    const end = el?.selectionEnd ?? current.length
    const next = current.slice(0, start) + latex + current.slice(end)
    onChange(next)
    // Restore focus + cursor to just after the inserted snippet.
    requestAnimationFrame(() => {
      if (el) {
        el.focus()
        el.setSelectionRange(start + latex.length, start + latex.length)
      }
    })
  }

  // Live preview: render $...$ segments as math, everything else as text.
  const renderPreview = () => {
    if (!value.trim()) return null
    const parts = value.split(/(\$[^$]+\$)/g)
    return parts.map((part, i) => {
      if (part.startsWith('$') && part.endsWith('$') && part.length > 2) {
        try {
          return (
            <span
              key={i}
              dangerouslySetInnerHTML={{
                __html: katex.renderToString(part.slice(1, -1), {
                  throwOnError: false,
                  displayMode: false,
                  strict: false,
                }),
              }}
            />
          )
        } catch {
          return <span key={i}>{part}</span>
        }
      }
      return <span key={i}>{part}</span>
    })
  }

  return (
    <div>
      {/* Symbol palette */}
      <div className="flex flex-wrap gap-1.5 mb-3">
        {SYMBOLS.map((symbol) => (
          <button
            key={symbol.label}
            type="button"
            title={symbol.title || symbol.label}
            onClick={() => insertSymbol(symbol.latex)}
            disabled={disabled}
            className="px-2.5 py-1.5 text-sm font-mono bg-white border border-gray-200 rounded-lg text-gray-700 hover:border-primary-400 hover:text-primary-700 hover:bg-primary-50 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {symbol.label}
          </button>
        ))}
      </div>

      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={rows}
        disabled={disabled}
        className="input w-full font-mono"
        placeholder={
          placeholder ||
          'Type your working here. Use the palette above for math symbols, e.g. $\\frac{a}{b}$, $x^{2}$, $\\sqrt{x}$, or write in plain text.'
        }
      />

      {/* Live rendered preview */}
      {value.trim() && (
        <div className="mt-3 border border-gray-200 bg-gray-50 rounded-lg p-4 min-h-[3rem]">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Preview — how your math renders
          </p>
          <div className="text-gray-900 overflow-x-auto">{renderPreview()}</div>
        </div>
      )}
    </div>
  )
}

export default MathEditor
