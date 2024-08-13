
'''
    1) __init__.py
    2) custom tag 생성(수정) 후에 server reset 해야 함
    3) 사용할 html에 {% load board_tags %} 해야 함
'''

from django import template

register = template.Library()

@register.filter # {{start | nextpage : bottomLine}}
def nextpage(start, bottonLine) :
    return start+bottonLine

@register.filter # {{start | prepage : bottomLine}}
def prepage(start, bottonLine) :
    return start-bottonLine

@register.simple_tag
def addtags(value1, value2) : # {% addtags value1 value2 %}
    return value1 + value2

@register.simple_tag
def minustags(value1, value2) : # {% minustags value1 value2 %}
    return value1 - value2 + 1