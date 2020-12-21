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

SIM_NAO_CHOICES_FILTRO = ((None, '-----'), (True, 'Sim'), (False, 'Não'))
SIM_NAO_CHOICES_COMPARTILHADA_FILTRO = ((None, '-----'), (False, 'Sim'), (True, 'Não'))


class EstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = EstabelecimentoSaude
        fields = '__all__'
        widgets = {
            "codigo_cnes": forms.TextInput(attrs={'class': 'form-control'}),
            "municipio": ModelSelect2Widget(queryset=Municipio.objects.order_by('nome'),
                                            search_fields=['nome__icontains', 'codigo__icontains'],
                                            attrs={'class': 'form-control'}),
        }


class FiltroEstabelecimentoForm(forms.Form):
    cnes = forms.CharField(label="CNES", max_length=12, required=False)
    nome = forms.CharField(max_length=80, required=False)


class FiltroNomeForm(forms.Form):
    nome = forms.CharField(max_length=255, required=False)


class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = '__all__'


class FiltroMunicipioForm(forms.Form):
    ibge = forms.CharField(label="IBGE", max_length=12, required=False)
    nome = forms.CharField(max_length=80, required=False)
    estado = forms.ModelChoiceField(
        label=u'Estado', required=False,
        queryset=UnidadeFederativa.objects.all().order_by("nome"))


class VacinaForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = '__all__'


class VacinaEstoqueForm(forms.Form):
    estabelecimento = forms.ModelChoiceField(
        label=u'Estabelecimento',
        queryset=EstabelecimentoSaude.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    qtd = forms.IntegerField(label="Quantidade", min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))


VacinaEstoqueFormSet = formset_factory(VacinaEstoqueForm)


class VinculoForm(forms.Form):
    estabelecimento = forms.ModelChoiceField(
        label=u'Estabelecimento',
        queryset=EstabelecimentoSaude.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    ativo = forms.BooleanField(label="Ativo", required=False)


VinculoFormSet = formset_factory(VinculoForm)


class NovoUsuarioForm(forms.ModelForm):
    nome = forms.CharField()
    grupo = forms.ModelChoiceField(label=u'Perfil', queryset=Group.objects.all(),
                                                widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    data_nascimento = forms.DateField(label=u'Data de Nascimento',
                                      widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'}),
                                      input_formats=('%d/%m/%Y',))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    password1 = forms.CharField(label=_("Senha"), min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    password2 = forms.CharField(label=_("Confirmação de senha"), min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_("Enter the same password as above, for verification."), required=False)

    class Meta:
        model = Usuario
        fields = ('cpf', 'data_nascimento', 'telefone')
        labels = {'cpf': 'CPF'}

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if cpf:
            validador_cpf = BRCPFField()
            validador_cpf.clean(cpf)

        return cpf
    
    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(u'As senhas não coincidem.')
        return self.cleaned_data


class NovoUsuarioExternoForm(forms.ModelForm):
    nome = forms.CharField()
    data_nascimento = forms.DateField(label=u'Data de Nascimento',
                                      widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'}),
                                      input_formats=('%d/%m/%Y',))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    password1 = forms.CharField(label=_("Senha"), min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    password2 = forms.CharField(label=_("Confirmação de senha"), min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=_("Enter the same password as above, for verification."), required=False)

    class Meta:
        model = Usuario
        fields = ('cpf', 'data_nascimento', 'telefone')
        labels = {'cpf': 'CPF'}

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if cpf:
            validador_cpf = BRCPFField()
            validador_cpf.clean(cpf)

        return cpf
    
    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(u'As senhas não coincidem.')
        return self.cleaned_data

