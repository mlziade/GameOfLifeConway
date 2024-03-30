# Game of life

# Prelude
    # Tanto faz, eu tô chapado e vi esse vídeo "Math's Fundamental Flaw" https://youtu.be/HeQX2HjkcNo?si=89_5bHk-IF4SBUYd&t=65

# Tabuleiro
    # Um grid 100x100 preenchidos com 1 ou 0

# Regras
    # Para cada espaço populado
        # Cada celula com menos de 2 vizinhos vivos morre
        # Cada celula com mais de 3 vizinhos morre
        # Cada celula com 2 ou 3 vizinhos vive
    # Para cada espaço vazio
        # Cada celular com exatamente três vizinhos vive

# Input
    # A quantidade de celulas preenchidas com 1, equivalente a n
    # As posições x e y de n celulas 

# Output
    # Uma série matrizes, formatadas para leitura, de frames com o estado do grid

# Naming Convention
    # https://visualgit.readthedocs.io/en/latest/pages/naming_convention.html