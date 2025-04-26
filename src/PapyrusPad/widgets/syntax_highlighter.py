"""Syntax highlighters for different document types."""

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Python code."""

    # Python keywords
    keywords = [
        "and",
        "assert",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "exec",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "not",
        "or",
        "pass",
        "print",
        "raise",
        "return",
        "try",
        "while",
        "yield",
        "None",
        "True",
        "False",
    ]

    # Python operators
    operators = [
        "=",
        # Comparison
        "==",
        "!=",
        "<",
        "<=",
        ">",
        ">=",
        # Arithmetic
        "\+",
        "-",
        "\*",
        "/",
        "//",
        "\%",
        "\*\*",
        # In-place
        "\+=",
        "-=",
        "\*=",
        "/=",
        "\%=",
        # Bitwise
        "\^",
        "\|",
        "\&",
        "\~",
        ">>",
        "<<",
    ]

    # Python braces
    braces = [
        "\{",
        "\}",
        "\(",
        "\)",
        "\[",
        "\]",
    ]

    def __init__(self, document):
        """Initialize the highlighter with styles."""
        super().__init__(document)

        # Styles
        self.styles = {
            "keyword": self._format(QColor("#569CD6")),
            "operator": self._format(QColor("#D4D4D4")),
            "brace": self._format(QColor("#D4D4D4")),
            "defclass": self._format(QColor("#4EC9B0")),
            "string": self._format(QColor("#CE9178")),
            "string2": self._format(QColor("#CE9178")),
            "comment": self._format(QColor("#6A9955")),
            "self": self._format(QColor("#569CD6")),
            "numbers": self._format(QColor("#B5CEA8")),
        }

        # Multi-line strings (expression, flag, style)
        self.tri_single = (QRegularExpression("'''"), 1, self.styles["string2"])
        self.tri_double = (QRegularExpression('"""'), 2, self.styles["string2"])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r"\b%s\b" % w, 0, self.styles["keyword"]) for w in PythonHighlighter.keywords]
        rules += [(r"%s" % o, 0, self.styles["operator"]) for o in PythonHighlighter.operators]
        rules += [(r"%s" % b, 0, self.styles["brace"]) for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r"\bself\b", 0, self.styles["self"]),
            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles["string"]),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles["string"]),
            # 'def' followed by an identifier
            (r"\bdef\b\s*(\w+)", 1, self.styles["defclass"]),
            # 'class' followed by an identifier
            (r"\bclass\b\s*(\w+)", 1, self.styles["defclass"]),
            # From '#' until a newline
            (r"#[^\n]*", 0, self.styles["comment"]),
            # Numeric literals
            (r"\b[+-]?[0-9]+[lL]?\b", 0, self.styles["numbers"]),
            (r"\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b", 0, self.styles["numbers"]),
            (r"\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b", 0, self.styles["numbers"]),
        ]

        # Build a QRegularExpression for each pattern
        self.rules = [(QRegularExpression(pat), index, fmt) for (pat, index, fmt) in rules]

    def _format(self, color, style=None):
        """Return a QTextCharFormat with the given attributes."""
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        if style == "bold":
            fmt.setFontWeight(QFont.Weight.Bold)
        elif style == "italic":
            fmt.setFontItalic(True)
        return fmt

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text."""
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(nth), match.capturedLength(nth), format)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self._match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self._match_multiline(text, *self.tri_double)

    def _match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings."""
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            match = delimiter.match(text)
            if match.hasMatch():
                start = match.capturedStart()
                add = match.capturedLength()
            else:
                return False

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            match = delimiter.match(text, start + add)
            end = match.capturedStart()
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + match.capturedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            match = delimiter.match(text, start + length)
            if match.hasMatch():
                start = match.capturedStart()
            else:
                break

        # Return True if still inside a multi-line string, False otherwise
        return self.currentBlockState() == in_state


class MarkdownHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Markdown text."""

    def __init__(self, document):
        """Initialize the highlighter with styles."""
        super().__init__(document)

        # Styles
        self.styles = {
            "header": self._format(QColor("#569CD6"), "bold"),
            "emphasis": self._format(QColor("#D4D4D4"), "italic"),
            "strong": self._format(QColor("#D4D4D4"), "bold"),
            "code": self._format(QColor("#CE9178")),
            "link": self._format(QColor("#4EC9B0"), "underline"),
            "list": self._format(QColor("#6A9955")),
        }

        # Rules
        self.rules = [
            # Headers (# Header)
            (QRegularExpression(r"^#+ .*$"), 0, self.styles["header"]),
            # Emphasis (*text* or _text_)
            (QRegularExpression(r"\*[^*\n]+\*|_[^_\n]+_"), 0, self.styles["emphasis"]),
            # Strong (**text** or __text__)
            (QRegularExpression(r"\*\*[^*\n]+\*\*|__[^_\n]+__"), 0, self.styles["strong"]),
            # Code (`code`)
            (QRegularExpression(r"`[^`\n]+`"), 0, self.styles["code"]),
            # Links ([text](url))
            (QRegularExpression(r"\[([^\]]+)\]\(([^)]+)\)"), 0, self.styles["link"]),
            # Lists (- item or * item or 1. item)
            (QRegularExpression(r"^\s*[\*\-\+]\s+.*$|^\s*\d+\.\s+.*$"), 0, self.styles["list"]),
        ]

    def _format(self, color, style=None):
        """Return a QTextCharFormat with the given attributes."""
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        if style == "bold":
            fmt.setFontWeight(QFont.Weight.Bold)
        elif style == "italic":
            fmt.setFontItalic(True)
        elif style == "underline":
            fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
        return fmt

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text."""
        for expression, nth, format in self.rules:
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(nth), match.capturedLength(nth), format)
