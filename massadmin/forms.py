# -*- coding: utf-8 -*-

from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from extended_choices import Choices

CHARFIELD_ACTIONS = Choices(
    ('DEFINE', 'define', _('Define (if empty)')),
    ('REPLACE', 'replace', _('Replace')),
    ('PREPEND', 'prepend', _('Add before')),
    ('APPEND', 'append', _('Add after'))
)


class MassOptionsForField(forms.Form):
    """
    A dynamic form that displays mass change options for a given model field.

    In most common case, it just generates a checkbox to enable user
    to choose whether or not he wants to handle mass change of this given field.
    If given field is a CharField and its widget is not
    a sub-instance of MultiWidget, expose more advanced options like
    'prepend', 'append', 'empty', etc.
    """
    CHARFIELD_ACTIONS = CHARFIELD_ACTIONS
    def __init__(self, *args, **kwargs):
        self.model_field_name = kwargs.pop('field_name')
        self.model_field = kwargs.pop('field')
        super(MassOptionsForField, self).__init__(*args, **kwargs)

        mass_field_name = self.get_mass_field_name()

        # Always create an "activate" checkbox
        self.fields[mass_field_name] = forms.BooleanField(required=False)

        # According to field type and widget, optionally create mass options field
        if isinstance(self.model_field, forms.CharField) and not isinstance(self.model_field.widget, widgets.MultiWidget):
            self.fields[mass_field_name + '_action'] = forms.ChoiceField(choices=CHARFIELD_ACTIONS)

    def get_mass_field_name(self):
        return '_mass_change_' + self.model_field_name