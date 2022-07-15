# Используются библиотеки nltk, collections, pymorhy2

from nltk.corpus import stopwords  # для обработки стоп-слов
from nltk.tokenize import word_tokenize  # для токенизации слов
from collections import Counter  # для подсчёта вторым способом
from pymorphy2 import MorphAnalyzer  # для морфологического разбора
import math # для вычисления idf(log по основанию 10)

from sklearn.metrics.pairwise import cosine_similarity # для проверки косинусной метрики

spis_form = []  # список получившихся лемм из текста
kvo = 0  # количество каждой леммы
morph = MorphAnalyzer()  # необходимо для морфологического анализа
res = []  # список, полученный после токенизации слов
tf_idf = []
# знаки препинания, которые используются в тексте
# От них не нужно получать леммы, поэтому они отбрасываются и в res их нет
znaki_prep = {'.', ',', ':', '!', '?', '...', ';', '(', ')', '"', '-'}
list_files = ["test1.txt", "test2.txt", "test3.txt", "test4.txt", "test5.txt", "test6.txt", "test7.txt", "test8.txt", "test9.txt", "test10.txt"]


def token(list_files, res): # функция для получения всех уникальных слов в текстах
    for i in list_files:
        f = open(i, 'r', encoding='utf-8')
        for line in f:
            # стоп-слова здесь по умолчанию, но их можно добавить, если необходимо
            stw = stopwords.words('russian')
            #  stw.append('это') - добавление любого слова в список стоп-слов
            word_tokens = word_tokenize(line)  # токенизируем слова в строке файла
            for w in word_tokens:
                if w.lower() not in stw and w not in znaki_prep:
                    #  w.lower() - возавращает символ в нижнем регистре
                    #  Необходимо, чтобы, например, 'В' тоже считалось стоп-словом
                    #  Слова в список стоп-слов нужно добавлять тоже в нижнем регистре
                    p = morph.parse(w.lower())[0]  # получаем разбор слова
                    #  индекс 0, чтобы получить только первую форму(для омонимии)
                    if p.normal_form not in res:
                        res.append(p.normal_form)  # добавляем в конец списка лемму слова
        f.close()
    return res


def vectorize(list_files, list_form): # фунцкия векторизации каждого текста
    res = []
    vector = []
    for i in list_files:
        tmp = []
        f = open(i, 'r', encoding='utf-8')
        for line in f:
            # стоп-слова здесь по умолчанию, но их можно добавить, если необходимо
            stw = stopwords.words('russian')
            #  stw.append('это') - добавление любого слова в список стоп-слов
            word_tokens = word_tokenize(line)  # токенизируем слова в строке файла
            for w in word_tokens:
                if w.lower() not in stw and w not in znaki_prep:
                    #  w.lower() - возавращает символ в нижнем регистре
                    #  Необходимо, чтобы, например, 'В' тоже считалось стоп-словом
                    #  Слова в список стоп-слов нужно добавлять тоже в нижнем регистре
                    p = morph.parse(w.lower())[0]  # получаем разбор слова
                    #  индекс 0, чтобы получить только первую форму(для омонимии)
                    res.append(p.normal_form)  # добавляем в конец списка лемму слова
        kvo = 0
        for k in list_form:  # проходимся по списку всех уникальных слов в текстах, полученному функцией "token"
            for j in res:  # проходимся по списку всех слов каждого текста
                if k == j:
                    kvo += 1  # считаем кол-во каждого слова
            tmp.append(kvo)  # формируем вектор
            kvo = 0
        vector.append(tmp)  # добавляем полученный вектор в список
        tmp = []
        res = []
        f.close()
    return vector  # возвращаем список векторов каждого текста


def tf_idf(vector):  # функция вычисления tf-idf
    kvo_doc = []
    for k in range(len(vector[0])): # создаем список "kvo_doc", элементами которого являются кол-во
        # текстов, в которое входит каждое слово. В формуле idf это знаменатель под логарифмом
        kvo = 0
        for j in range(len(vector)):
            if vector[j][k] != 0:
                kvo += 1
        kvo_doc.append(kvo)
    print(kvo_doc)
    for i in range(len(vector)):
        for j in range(len(vector[0])):  # вычисляем tf-idf
            vector[i][j] = (vector[i][j] / len(vector[0])) * math.log10(len(vector) / kvo_doc[j])
    return vector


def cosine(list_files, list_form, vector):  # функция подсчета косинусной метрики
    for i in range(len(list_files)):
        for j in range(i + 1, len(list_files)):
            sum = 0
            delit1 = 0
            delit2 = 0
            for k in range(len(vector[0])):
                sum += vector[i][k]*vector[j][k]  # числитель в формуле
                delit1 += vector[i][k] ** 2  # два делителя - это абсолютная величина векторов
                delit2 += vector[j][k] ** 2
            print("Косинусное расстояние между ", list_files[i], 'и ', list_files[j], "равно ", sum / (math.sqrt(delit1) * math.sqrt(delit2)))

def text_similarity(list_files):
    res = []
    res = token(list_files, res)
    # print("Все слова ", res)
    vector = vectorize(list_files, res)
    # print(vector)
    vector = tf_idf(vector)
    # print(vector)
    cosine(list_files, res, vector)
    print("*" * 100)
    print(cosine_similarity(vector))

text_similarity(list_files)

'''res = token(list_files, res)
# print("Все слова ", res)
vector = vectorize(list_files, res)
print(vector)
vector = tf_idf(vector)
print(vector)
cosine(list_files, res, vector)
print("xxxxxxxxxx", cosine_similarity(vector))'''


