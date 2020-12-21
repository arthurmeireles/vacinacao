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

class HorarioForm(forms.Form):
    data = forms.DateField(label=u'Data:', widget=forms.DateInput(format='%d/%m/%Y',
                                                         attrs={'class': 'form-control'}),
                                      input_formats=('%d/%m/%Y',))
    hora = forms.TimeField(widget=forms.TimeInput(format='%H:%M',
                                                         attrs={'class': 'form-control'}),
                                  input_formats=('%H:%M',), label="Hora")
    vagas = forms.IntegerField(label="Vagas", min_value=0, widget=forms.NumberInput(
                                                         attrs={'class': 'form-control'}),)

HorarioFormSet = formset_factory(HorarioForm)

class AgendamentoForm(forms.ModelForm):
    data = forms.DateTimeField(label=u'Data/Hora:', widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M',
                                                         attrs={'class': 'form-control'}),
                                      input_formats=('%d/%m/%Y %H:%M',))
    class Meta:
        model = Agendamento
        fields = ('data', 'vacina', 'estabelecimento')
        # widgets = {
        #     "codigo_cnes": forms.TextInput(attrs={'class': 'form-control'}),
        #     "nome": forms.TextInput(attrs={'class': 'form-control'}),
        #     "municipio": ModelSelect2Widget(queryset=Municipio.objects.order_by('nome'),
        #                                     search_fields=['nome__icontains', 'codigo__icontains'],
        #                                     attrs={'class': 'form-control'}),
        # }