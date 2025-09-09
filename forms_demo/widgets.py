from django import forms

class TagWidget(forms.Widget):
    template_name = 'forms_demo/widgets/tag_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # The value from the form is a list of string
        context['widget']['tags'] = value if value else []
        return value
