'''
Created on 09.07.2010

@author: ekondrashev
'''
from django import forms
from django.utils.translation import ugettext as _

from dj_test.makler.widgets import AutocompleteWidget

SPORTS_CHOICES = (
    ('basketball', _('Basketball')),
    ('football', _('Football')),
    ('hockey', _('Hockey')),
)

class SampleForm(forms.Form):
    name = forms.CharField(label=_('Name'))
    #country = forms.CharField(label=_('Country'), widget=AutocompleteWidget(choices_url='autocomplete_countries', related_fields=('city',)))
    #city = forms.CharField(label=_('City'), widget=AutocompleteWidget(choices_url='autocomplete_cities', related_fields=('country',)))
    sports = forms.ChoiceField(label=_('Sports'), choices=SPORTS_CHOICES,
                               widget=AutocompleteWidget(options={'minChars': 0, 'autoFill': True, 'mustMatch': True}))
