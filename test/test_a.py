def moyenne(*nombres):
    taille = len(nombres)
    if taille == 0:
        return None
    somme = 0
    for nombre in nombres:
        if not isinstance(nombre, int):
            raise TypeError(f'"{nombre}" is not a number')
        somme += nombre
    return somme / taille


def test_moyenne():
    assert moyenne(5) == 5
    assert moyenne() is None
    assert moyenne(5, 8, 9) == 7
    assert moyenne(5, 8, 9, 78, 43) == 28
    assert moyenne(5, 8,'e', 9)


def test_moyenne_with_no_parameters():
    assert moyenne() is None
