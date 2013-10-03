from jinja2.ext import Markup

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter


def highlight_filter(code, language=None, **kwargs):
    if language is None:
        lexer = guess_lexer(code)
    else:
        lexer = get_lexer_by_name(language, stripall=False)

    formatter = HtmlFormatter(**kwargs)
    code = highlight(Markup(code).unescape(), lexer, formatter)
    return code
