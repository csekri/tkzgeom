"""
defines syntax_function which turns str into CSS/HTML formatted
syntax highlighted TikZ code
"""


import re


def pygments_syntax_highlight(text):
    """
    SUMMARY
        returns CSS/HTML syntax highlighted TikZ code using pygments
        (works if and only if pygments is installed)

    PARAMETERS
        text: tex source code to be syntax highlighted

    RETURNS
        str: CSS/HTML syntax highlighted tikz code
    """
    style = get_style_by_name('colorful')
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
    def replace_pivot_spaces(text):
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
    """
    HELPER FUNCTION
        Syntax highlights the entire line, if "%" is preceded by "\n"
    """
    def highlight_comments(text):
        text = text.split('\n')
        for i in range(len(text)):
            if len(text[i]) > 0 and text[i][0] == "%":
                text[i] = '<span style="color:blue;font-weight:bold">' + text[i] + '</span>'
        return '\n'.join(text)

    # text = highlight_comments(text)
    match = re.findall(r'[^\\](%.*)\n', text)
    # print(match)
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


# check for pygments
syntax_highlight = lambda x: None
try:
    from pygments import highlight, lexers
    from pygments.styles import get_style_by_name
    from pygments.formatters import HtmlFormatter
    syntax_highlight = pygments_syntax_highlight
    print(1/0)  # TODO delete this when there will be an option to choose
except:
    syntax_highlight = alternative_syntax_highlight
