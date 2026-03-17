from django.contrib import admin
from .models import Paciente, Medicamento, Afericao, AtendimentoMultidisciplinar, AvaliacaoPrevent, TriagemHipertensao, AtendimentoMedico, PrescricaoMedica, ItemPrescricao

admin.site.register(Paciente)
admin.site.register(Medicamento)
admin.site.register(Afericao)
admin.site.register(AtendimentoMultidisciplinar)
admin.site.register(AvaliacaoPrevent)
admin.site.register(TriagemHipertensao)
admin.site.register(AtendimentoMedico)
admin.site.register(PrescricaoMedica)
admin.site.register(ItemPrescricao)
