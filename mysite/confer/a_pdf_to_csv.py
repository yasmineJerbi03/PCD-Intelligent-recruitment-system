import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import re
import os

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import HTMLConverter
from io import StringIO
from bs4 import BeautifulSoup
import xlwt
# from main import scanner
import pandas as pd
import numpy as np

import nltk
from Levenshtein import distance


def conversion_html(path):
    Manager = PDFResourceManager()
    string_io = StringIO()
    laparams = LAParams()
    device = HTMLConverter(Manager, string_io, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(Manager, device)
    for page in PDFPage.get_pages(fp, set(), maxpages=0, password="", caching=True,
                                  check_extractable=True):
        interpreter.process_page(page)

    fp.close()
    device.close()
    text = string_io.getvalue()
    return text


def data_manipulation(html, res):
    soup = BeautifulSoup(html, 'html.parser')
    if res == 0:
        return soup.get_text()
    pix = re.compile("font-size:(\d+)")
    if res == 1:
        empty = []
        font_size = {}
        for tag in soup.select("[style*=font-size]"):
            font_size[tag.text.strip()] = pix.search(tag["style"]).group(1)
        for cle in font_size.keys():
            if str(cle) == '':
                empty.append(cle)
        for i in empty:
            del font_size[i]
        return font_size
    if res == 2:
        empty = []
        font_family = {}
        pix = re.compile("font-family:(\s\w+)([\s,+\w+,-]*)")
        for tag in soup.select("[style*=font-family]"):
            font_family[tag.text.strip()] = pix.search(tag["style"]).group()
        for cle in font_family.keys():
            if str(cle) == '':
                empty.append(cle)
        for i in empty:
            del font_family[i]
        return font_family


def data_manipulation(html, res):
    soup = BeautifulSoup(html, 'html.parser')
    if res == 0:
        return soup.get_text()
    pix = re.compile("font-size:(\d+)")
    if res == 1:
        empty = []
        font_size = {}
        for tag in soup.select("[style*=font-size]"):
            font_size[tag.text.strip()] = pix.search(tag["style"]).group(1)
        for cle in font_size.keys():
            if str(cle) == '':
                empty.append(cle)
        for i in empty:
            del font_size[i]
        return font_size
    if res == 2:
        empty = []
        font_family = {}
        pix = re.compile("font-family:(\s\w+)([\s,+\w+,-]*)")
        for tag in soup.select("[style*=font-family]"):
            font_family[tag.text.strip()] = pix.search(tag["style"]).group()
        for cle in font_family.keys():
            if str(cle) == '':
                empty.append(cle)
        for i in empty:
            del font_family[i]
        return font_family


def data_cleaning(path, i):
    dict = data_manipulation(conversion_html(path), i)
    pop_list = []
    dict1 = {}
    dict_n = []
    for cle in dict.keys():
        cle = str(cle).replace('\n', '  ')
        if len(str(cle)) <= 3:
            pop_list.append(cle)
    for i in range(0, len(pop_list)):
        dict.pop(pop_list[i])
    for cle1 in dict.keys():
        cle1 = re.sub('[^A-Za-z0-9 ' ' | éèà À Á Â Æ Ç È É Ê Ë Ì Í Î Ï Ñ Ò Ó Ô Œ Ù Ú Û Ü Ý Ÿà á â æ ç è é ê'
                      '	ë ì	í î	ï ñ	ò ó	ô œ	ù ú	û ü	ý ÿ]+', '', str(cle1))
        cle1 = re.sub('[" "][" "]+', '  ', str(cle1))
        dict_n.append(cle1)
    s = 0
    for value in dict.values():
        dict1[dict_n[s]] = value
        s = s + 1
    pop_list = []
    for cle in dict1.keys():
        if str(cle).startswith(','):
            cle = str(cle).replace(',', ' ', 1)
        if len(str(cle)) <= 3:
            pop_list.append(cle)
    for i in range(0, len(pop_list)):
        dict1.pop(pop_list[i])

    return dict1


def nb_mots(chaine):
    liste = chaine.split()
    l = len(liste)
    return l


def case(chaine):
    if chaine.isupper():
        return 1
    else:
        return 0


def font_size(path):
    font_size = data_cleaning(path, 1)
    s = 0
    cles = 0
    for value in font_size.values():
        s = s + float(value)
        cles = cles + 1
    average = s / cles
    for cle in font_size.keys():
        if float(font_size[cle]) < average:
            font_size[cle] = 0
        else:
            font_size[cle] = 1
    return font_size


def font_family(path):
    i = 0
    cles = 0
    s = 0
    font_family = data_cleaning(path, 2)
    fonts = {}
    for cle in font_family.keys():
        for cle1 in font_family.keys():
            if font_family[cle] == font_family[cle1]:
                i = i + 1
        fonts[font_family[cle]] = i
        i = 0
    for cle in fonts.keys():
        cles = cles + 1
        s = s + fonts[cle]
    average = s / cles
    for cle in fonts.keys():
        if float(fonts[cle]) < average:
            fonts[cle] = 0
        else:
            fonts[cle] = 1
    for cle in font_family.keys():
        font_family[cle] = fonts[font_family[cle]]
    return (font_family)


def bold_exist(path):
    font_family = data_cleaning(path, 2)
    for cle in font_family.keys():
        if "Bold" in font_family[cle] or "bold" in font_family[cle]:
            font_family[cle] = 1
        else:
            font_family[cle] = 0
    return font_family


def nb_noms(chaine):
    s = 0
    tab = nltk.pos_tag(nltk.word_tokenize(chaine))
    for i in range(0, len(tab)):
        fonc = tab[i][1]
        if fonc.startswith('NN'):
            s = s + 1
    return s


def nb_VERBS(chaine):
    s = 0
    tab = nltk.pos_tag(nltk.word_tokenize(chaine))
    for i in range(0, len(tab)):
        fonc = tab[i][1]
        if fonc.startswith('VB'):
            s = s + 1
    return s


def cmp(chaine1, chaine2):
    chaine2 = chaine2.replace('/n', '')
    edit_dist = distance(chaine1, chaine2)
    return edit_dist


def to_excel(max):
    workbook = xlwt.Workbook()
    for j in range(1, max + 1):
        sheet = workbook.add_sheet(f'{j}', cell_overwrite_ok=True)
        f = 0
        list = ['bloc', 'label', 'font_size', 'font_family', 'nb_mots', 'nb_verbes', 'nb_noms', 'case', 'bold']
        for i in range(0, 9):
            sheet.write(0, f, list[i])
            f = f + 1
        dict = data_cleaning(f'cv_analysis/dataset/data/{j}.pdf', 2)
        size = font_size(f'cv_analysis/dataset/data/{j}.pdf')
        family = font_family(f'cv_analysis/dataset/data/{j}.pdf')
        bold = bold_exist(f'cv_analysis/dataset/data/{j}.pdf')
        i = 1
        for cle in dict.keys():
            sheet.write(i, 0, cle)
            sheet.write(i, 4, nb_mots(cle))
            sheet.write(i, 5, nb_VERBS(cle))
            sheet.write(i, 6, nb_noms(cle))
            sheet.write(i, 7, case(cle))

            i = i + 1
        i = 1
        for cle in size.keys():
            sheet.write(i, 2, size[cle])
            i = i + 1
        i = 1
        for cle in family.keys():
            sheet.write(i, 3, family[cle])
            i = i + 1

        i = 1
        for cle in bold.keys():
            sheet.write(i, 8, bold[cle])
            i = i + 1

    workbook.save('dataset/resume.xls')


def input_cv(path, id):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('1', cell_overwrite_ok=True)
    f = 0
    list = ['bloc', 'label', 'font_size', 'font_family', 'nb_mots', 'nb_verbes', 'nb_noms', 'case', 'bold']
    for i in range(0, 9):
        sheet.write(0, f, list[i])
        f = f + 1

    dict = data_manipulation(conversion_html(path), 2)
    size = font_size(path)
    family = font_family(path)
    bold = bold_exist(path)
    i = 1
    for cle in dict.keys():
        sheet.write(i, 0, cle)
        sheet.write(i, 4, nb_mots(cle))
        sheet.write(i, 5, nb_VERBS(cle))
        sheet.write(i, 6, nb_noms(cle))
        sheet.write(i, 7, case(cle))
        i = i + 1
    i = 1
    for cle in size.keys():
        sheet.write(i, 2, size[cle])
        i = i + 1
    i = 1
    for cle in family.keys():
        sheet.write(i, 3, family[cle])
        i = i + 1

    i = 1
    for cle in bold.keys():
        sheet.write(i, 8, bold[cle])
        i = i + 1
    workbook.save(f'confer/cv_analysis/dataset/{id}.xls')

    read_file = pd.read_excel(f'confer/cv_analysis/dataset/{id}.xls', index_col=None)
    read_file.to_csv(f'confer/cv_analysis/dataset/{id}.csv', index=None, header=True)
    df = pd.read_csv(f'confer/cv_analysis/dataset/{id}.csv', usecols=[j for j in range(1, 9)])
    mat = df.to_numpy()
    np.savetxt(f'confer/cv_analysis/dataset/{id}{id}.csv', mat, delimiter=",")
    os.remove(f'confer/cv_analysis/dataset/{id}.csv')

