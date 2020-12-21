# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from datetime import date as datetime_date

from django.contrib.auth.models import Group, User
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from django.forms.models import ModelChoiceField, inlineformset_factory
from django import forms
from administracao.models import *
from django.utils.translation import ugettext_lazy as _
from localflavor.br.forms import BRCPFField
from django.forms import formset_factory
from .models import *


class VacinaPrivadaForm(forms.ModelForm):
    class Meta:
        model = VacinaUsuario
        fields = ('vacina', 'data')


class FiltroVacinaForm(forms.Form):
    data = forms.DateField(label=u'Data', required=False,
                                      widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'}),
                                      input_formats=('%d/%m/%Y',))