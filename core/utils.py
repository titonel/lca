"""
Utilitários compartilhados entre todas as linhas de cuidado.
"""

# Partículas que devem sempre ficar em minúsculas nos nomes próprios.
# Inclui preposições e conjunções comuns em nomes brasileiros e de origem estrangeira.
_PARTICULAS = {
    # Português
    'de', 'da', 'do', 'das', 'dos',
    'di', 'du',
    'e', 'em', 'com',
    'a', 'o', 'as', 'os',
    # Espanhol / Italiano
    'del', 'della', 'des', 'el', 'la', 'los', 'las', 'y',
    # Outras origens comuns no Brasil
    'von', 'van', 'den', 'der', 'ter',
}


def normalizar_nome(nome: str) -> str:
    """
    Normaliza um nome próprio:
      - Remove espaços extras nas extremidades e espaços duplos internos.
      - Primeira letra de cada palavra em maiúscula, restante em minúscula.
      - Partículas (de, da, do, das, dos, di, e, el, von, van etc.) permanecem
        em minúsculas, exceto se forem a primeira palavra do nome.

    Exemplos:
      'ADRIANA FELIX SOARES DA SILVA' → 'Adriana Felix Soares da Silva'
      'abigailton jose da silva'       → 'Abigailton Jose da Silva'
      'maria DE LOURDES dos santos'    → 'Maria de Lourdes dos Santos'
      'PEDRO VON DER HEIDE'            → 'Pedro von der Heide'
    """
    if not nome:
        return nome
    palavras = nome.strip().split()  # split() já elimina espaços duplos
    resultado = []
    for i, palavra in enumerate(palavras):
        lower = palavra.lower()
        if i > 0 and lower in _PARTICULAS:
            resultado.append(lower)
        else:
            resultado.append(lower.capitalize())
    return ' '.join(resultado)
