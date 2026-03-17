from django import forms
from django.core.exceptions import ValidationError
from .models import Paciente, TriagemHipertensao, AtendimentoMedico
from core.models import Usuario


def validate_cpf(cpf):
    if len(cpf) < 11:
        return False
    if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
        return False
    calc = lambda t: int(t[1]) * (t[0] + 2)
    d1 = ((sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11) % 10
    d2 = ((sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11) % 10
    return str(d1) == cpf[-2] and str(d2) == cpf[-1]


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'data_insercao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf = ''.join(filter(str.isdigit, str(cpf)))
        if not validate_cpf(cpf):
            raise ValidationError("O número de CPF informado é inválido.")
        return cpf


class TriagemHASForm(forms.ModelForm):
    class Meta:
        model = TriagemHipertensao
        fields = [
            'pa_sistolica_1', 'pa_diastolica_1',
            'pa_sistolica_2', 'pa_diastolica_2',
            'pa_sistolica_3', 'pa_diastolica_3',
            'qtd_antihipertensivos', 'risco_loa_presente'
        ]
        widgets = {
            'pa_sistolica_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PAS 1'}),
            'pa_diastolica_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PAD 1'}),
            'pa_sistolica_2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PAS 2'}),
            'pa_diastolica_2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PAD 2'}),
            'pa_sistolica_3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PAS 3'}),
            'pa_diastolica_3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'PAD 3'}),
            'qtd_antihipertensivos': forms.NumberInput(attrs={'class': 'form-control'}),
            'risco_loa_presente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AtendimentoMedicoForm(forms.ModelForm):
    class Meta:
        model = AtendimentoMedico
        fields = [
            'subjetivo', 'objetivo', 'avaliacao', 'plano',
            'cid10_1', 'cid10_2', 'cid10_3'
        ]
        widgets = {
            'subjetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                               'placeholder': 'Queixa principal, HMA, Revisão de Sistemas...'}),
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                              'placeholder': 'Exame físico, Sinais Vitais, Resultados de Exames...'}),
            'avaliacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                               'placeholder': 'Hipóteses diagnósticas e Raciocínio Clínico...'}),
            'plano': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Conduta, Orientações, Solicitações...'}),
            'cid10_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: I10 (Obrigatório)'}),
            'cid10_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: E11'}),
            'cid10_3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Z00'}),
        }
