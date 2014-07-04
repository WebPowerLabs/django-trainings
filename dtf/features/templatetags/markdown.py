from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re
import HTMLParser
import misaka

register = template.Library()


@register.filter
@stringfilter
def markdown(string):
    '''
    Receives Markdown-formatted string and returns it HTML5-formatted.
    '''
    string = re.sub('```\s*?\\n', '```', string)
    html_parser = HTMLParser.HTMLParser()

    def replace(re_match):
        return escape(re_match.group())

    string = re.sub(r'\<.*\>', replace, string)
    string = misaka.html(string,
                extensions=misaka.EXT_AUTOLINK |
                           misaka.EXT_FENCED_CODE |
                           misaka.EXT_NO_INTRA_EMPHASIS |
                           misaka.EXT_STRIKETHROUGH |
                           misaka.EXT_SUPERSCRIPT |
                           misaka.EXT_TABLES)

    def unreplace(re_match):
        return html_parser.unescape(re_match.group())

    string = re.sub(r'(?<=\<code\>).*(?=\<\/code\>)', unreplace, string,
                    flags=re.S)

    def replace_br(re_match):
        return re_match.group().replace('\n', '<br/>')

    string = re.sub(r'(?<=\<p\>).*?(?=\<\/p\>)', replace_br, string,
                    flags=re.S)
    return mark_safe(string)

