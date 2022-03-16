"""
defines syntax_function which turns str into CSS/HTML formatted
syntax highlighted TikZ code
"""


import re
try:
    from pygments import highlight, lexers
    from pygments.styles import get_style_by_name
    from pygments.formatters import HtmlFormatter
except:
    pass


def pygments_syntax_highlight(method, text):
    """
    SUMMARY
        returns CSS/HTML syntax highlighted TikZ code using pygments
        (works if and only if pygments is installed)

    PARAMETERS
        text: tex source code to be syntax highlighted

    RETURNS
        str: CSS/HTML syntax highlighted tikz code
    """
    print(method)
    style = get_style_by_name(method)
    formatter = HtmlFormatter(full=True, noclasses=True, style=style)
    lex = lexers.get_lexer_by_name("latex")
    return highlight(text, lex, formatter)


def alternative_syntax_highlight(text):
    """
    SUMMARY
        returns package-free syntax highlighted text for TikZ code
        (backup plan if pygments is not installed on the computer)

    PARAMETERS
        text: tex source code to be syntax highlighted

    RETURNS
        str: CSS/HTML syntax highlighted tikz code
    """

    """
    HELPER FUNCTION
        replaces pivot spaces with "&nbsp;", needed for HTML
    """
    def replace_pivot_spaces(text):  # TODO replace whole function with a regular expression substitution
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

    match = re.findall(r'[^\\](%.*)\n', text)
    does_not_contain_this_word = ''
    for i in range(5, 10000):
        if text.find(i * 'a') == -1:
            does_not_contain_this_word = i * 'a'
            break

    for i, result in enumerate(match):
        text = text.replace(result, str(i) + does_not_contain_this_word)

    text = re.sub(r'(\\begin{.+}|\\end{.*})', r'<span style="color:DarkCyan;font-weight:bold">\1</span>', text)
    text = re.sub(r'(?!\\begin|\\end)(\\\w+)', r'<span style="color:brown;font-weight:bold">\1</span>', text)
    text = re.sub(r'(\\%|\\\\|\\#)', r'<span style="color:brown;font-weight:bold">\1</span>', text)
    text = re.sub(r'(\W)(\d*\.?\d+)(\W)', r'\1<span style="color:green">\2</span>\3', text)
    text = replace_pivot_spaces(text)

    text = text.replace('\n', '<br>')

    for i, result in enumerate(match):
        text = text.replace(str(i) + does_not_contain_this_word, f'<span style="color:blue;font-weight:bold">{result}</span>')

    return text


def syntax_highlight(method, text):
    if not method:
        return alternative_syntax_highlight(text)
    try:
        return pygments_syntax_highlight(method, text)
    except:
        return alternative_syntax_highlight(text)