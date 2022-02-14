import os


def chtdct(ch):
    rt = {}
    texts = []
    texts_but_not_only = ch.split("'")
    for i in range(len(texts_but_not_only)):
        if i % 2 == 1:
            texts.append(texts_but_not_only[i])
    for i in range(len(texts)):
        if texts[i] in ('ws', 'src', 'app'):
            if texts[i] not in ('src'):
                rt[texts[i - 2]] = (texts[i - 1], texts[i])
            else:
                rt[(texts[i - 3], texts[i - 2])] = (texts[i - 1], texts[i])
    return rt


def save(dct):
    f = open(os.path.dirname(__file__) + '\\commands.txt', 'w')
    f.write(str(dct))
    f.close()


def load():
    f = open(os.path.dirname(__file__) + '\\commands.txt', 'r')
    s = f.read()
    f.close()
    return chtdct(s)


print(load())
