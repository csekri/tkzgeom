"""
defines syntax_function which turns str into CSS/HTML formatted
syntax highlighted TikZ code
"""
import re
try:
    from pygments import highlight, lexers
    from pygments.styles import get_style_by_name
    from pygments.formatters import HtmlFormatter
except ImportError:
    highlight, lexers, get_style_by_name, HtmlFormatter = 4 * [None]


def pygments_syntax_highlight(method, text):
    """Return CSS/HTML syntax-highlighted TikZ code using Pygments."""
    print(method)
    style = get_style_by_name(method)
    formatter = HtmlFormatter(full=True, noclasses=True, style=style)
    lex = lexers.get_lexer_by_name("latex")
    return highlight(text, lex, formatter)


def alternative_syntax_highlight(text):
    """Return syntax-highlighted text for LaTeX code using regex."""
    def replace_pivot_spaces(text):  # TODO replace whole function with a regular expression substitution
        """Replace leading spaces to HTML &nbsp."""
        exit_condition = True
        while exit_condition:
            exit_condition = False
            for i in range(len(text)-1):
                if text[i] == '\n' and text[i+1] == ' ':
                    numspace = 1
                    while text[i+1+numspace] == ' ':
                        numspace += 1
                    text = text[:i+1] + numspace*'&nbsp;' + text[i+1+numspace:]
                    exit_condition = True
        return text

    match = re.findall(r'[^\\](%.*)\n', text)  # find all inline comments
    does_not_contain_this_word = ''
    for i in range(5, 10000):  # find a word not present in the text
        if text.find(i * 'a') == -1:
            does_not_contain_this_word = i * 'a'
            break

    for i, result in enumerate(match):  # replace and index the inline comments in the text
        text = text.replace(result, str(i) + does_not_contain_this_word)

    # highlight begin-end environments
    text = re.sub(r'(\\begin{.+}|\\end{.*})', r'<span style="color:DarkCyan;font-weight:bold">\1</span>', text)
    # highlight commands starting with "\"
    text = re.sub(r'(?!\\begin|\\end)(\\\w+)', r'<span style="color:brown;font-weight:bold">\1</span>', text)
    # highlight %\, \\, \#
    text = re.sub(r'(\\%|\\\\|\\#)', r'<span style="color:brown;font-weight:bold">\1</span>', text)
    # highlight numbers
    text = re.sub(r'(\W)(\d*\.?\d+)(\W)', r'\1<span style="color:green">\2</span>\3', text)
    text = replace_pivot_spaces(text)

    text = text.replace('\n', '<br>')

    for i, result in enumerate(match):  # load back the inline comments and add syntax highlight
        text = text.replace(str(i) + does_not_contain_this_word,
                            f'<span style="color:blue;font-weight:bold">{result}</span>')

    return text


def syntax_highlight(method, text):
    """Highlight syntax either with or without Pygments."""
    method = '' if method[0] == '$' else method[1:]
    if not method:
        return alternative_syntax_highlight(text)
    try:
        return pygments_syntax_highlight(method, text)
    except ImportError:
        return alternative_syntax_highlight(text)
