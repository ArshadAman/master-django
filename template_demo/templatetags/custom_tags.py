# template_demo/templatetags/custom_tags.py
from django import template
from django.template.base import Node, TemplateSyntaxError

register = template.Library()

@register.tag(name='greet')
def do_greet(parser, token):
    """
    Custom tags that compiles to efficent python code.
    Usage: {% great user.first_name %}
    """
    try:
        # token.split_contents() knows how to handle quoted strings
        tag_name, variable_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires single arguments"
        )

    # Create a filter expression to resolve the variable name against the context
    person_variable = parser.compile_filter(variable_name)
    return GreetingNode(person_variable)

class GreetingNode(Node):
    def __init__(self, person_variable):
        self.person_variable = person_variable
    
    def render(self, context):
        try:
            person_name = self.person_variable.resolve(context)
        except template.VariableDoesNotExist:
            person_name = "World"
        
        if not person_name:
            person_name = "World"
        
        return f"Hello, {person_name}!"