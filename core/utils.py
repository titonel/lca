"""
Utilitários compartilhados entre todas as linhas de cuidado.
"""

# Partículas que devem sempre ficar em minúsculas nos nomes próprios.
_PARTICULAS = {'de', 'da', 'do', 'das', 'dos', 'e'}


def normalizar_nome(nome: str) -> str:
    """
    Normaliza um nome próprio:
      - Remove espaços extras nas extremidades.
      - Primeira letra de cada palavra em maiúscula, restante em minúscula.
      - Partículas ('de', 'da', 'do', 'das', 'dos', 'e') permanecem em minúsculas,
        exceto se forem a primeira palavra do nome.

    Exemplos:
      'ADRIANA FELIX SOARES DA SILVA' → 'Adriana Felix Soares da Silva'
      'abigailton jose da silva'       → 'Abigailton Jose da Silva'
      'maria DE LOURDES dos santos'    → 'Maria de Lourdes dos Santos'
    """
    if not nome:
        return nome
    palavras = nome.strip().split()
    resultado = []
    for i, palavra in enumerate(palavras):
        lower = palavra.lower()
        if i > 0 and lower in _PARTICULAS:
            resultado.append(lower)
        else:
            resultado.append(lower.capitalize())
    return ' '.join(resultado)
