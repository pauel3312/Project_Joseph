import os


def chtdct(ch):
    """
    gestionnaire de fichiers de sauvegarde : permet de transformer des chaines en dictionnaire
    (Json n'était pas utilisable ici car il ne prend pas en charge les tuples)
    :param ch : chaîne de caractères en entrée
    :return :dictionnaire correspondant
    """
    rt = {}
    texts = []
    texts_but_not_only = ch.split("'")
    for i in range(len(texts_but_not_only)):
        if i % 2 == 1:
            texts.append(texts_but_not_only[i])
    for i in range(len(texts)):
        if texts[i] in ('ws', 'src', 'app', 'innerFct'):
            if texts[i] not in ('src'):
                rt[texts[i - 2]] = (texts[i - 1], texts[i])
            else:
                rt[(texts[i - 3], texts[i - 2])] = (texts[i - 1], texts[i])
    return rt


def save(dct):
    """
    Fonction de sauvegarde des commandes
    :param dct: dictionnaire des commandes
    :return: rien
    """
    f = open(os.path.dirname(__file__) + '\\commands.txt', 'w', encoding='UTF-8')
    f.write(str(dct))
    f.close()


def load():
    """
    Charge le dictionnaire des commandes
    :return: dictionnaire des commandes
    """
    f = open(os.path.dirname(__file__) + '\\commands.txt', 'r', encoding='UTF-8')
    s = f.read()
    f.close()
    return chtdct(s)
