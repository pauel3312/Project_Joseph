# --coding: utf-8 --
import os
import json as js



def save(lst):
    """
    Fonction de sauvegarde des commandes
    :param lst: Liste des commandes
    :return: rien
    """
    f = open(os.path.dirname(__file__) + '\\commandes.txt', 'w', encoding='UTF-8')
    jsStr = js.dumps(lst)
    f.write(jsStr)
    f.close()


def load():
    """
    Charge le dictionnaire des commandes
    :return: liste des commandes
    """
    f = open(os.path.dirname(__file__) + '\\commandes.txt', 'r', encoding='UTF-8')
    s = f.read()
    f.close()
    lst = js.loads(s)
    return lst
