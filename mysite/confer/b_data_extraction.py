import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import spacy
import pandas as pd
import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
import re
from sklearn.feature_extraction.text import CountVectorizer

test = pd.read_csv("confer/Data extraction/dataset/Classeur.csv", sep=';', encoding='latin-1', engine='python')
test = test.fillna(0)
pst = PorterStemmer()
stemmer = WordNetLemmatizer()
nlp = spacy.load("fr_core_news_sm")
ro = set(stopwords.words('french'))


def technologies() :
    list=test.technologies.tolist()
    technologies=[]
    for i in range (len(list)):
        c=test.technologies[i]
        if c !=0 :
            technologies.append(c)
    return(technologies)

def experience() :
    list=test.experience.tolist()
    experience=[]
    for i in range (len(list)):
        c=test.experience[i]
        if c !=0 :
            experience.append(c)
    return(experience)

def specialité() :
    list=test.specialite.tolist()
    specialité=[]
    for i in range (len(list)):
        c=test.specialite[i]
        if c !=0 :
            specialité.append(c)
    return(specialité)

def critère():
    list=test.critère.tolist()
    critère=[]
    for i in range (len(list)):
        c=test.critère[i]
        if c !=0 :
            critère.append(c)
    return(critère)

def langue():
    list=test.langue.tolist()
    langue=[]
    for i in range (len(list)):
        c=test.langue[i]
        if c !=0 :
            langue.append(c)
    return(langue)

def années():
    list=test.années.tolist()
    années=[]
    for i in range (len(list)):
        c=test.années[i]
        if c !=0 :
            années.append(c)
    return(années)

def annestemming():
    list=années()
    annestemming=[]
    for word in list:
        annestemming.append(pst.stem(word).replace('ans','an'))
    return(annestemming)


def langstemming():
    list = langue()
    langstemming = []
    for word in list:
        langstemming.append(pst.stem(word))
    return (langstemming)


def techstemming():
    list = technologies()
    techstemming = []
    for word in list:
        techstemming.append(pst.stem(word))
    return (techstemming)


def expstemming():
    list = experience()
    expstemming = []
    for word in list:
        expstemming.append(pst.stem(word))
    return (expstemming)


def critstemming():
    list= critère()
    critstemming=[]
    for word in list:
        critstemming.append(pst.stem(word))
    return(critstemming)

def specstemming():
    list= specialité()
    specstemming=[]
    for word in list:
            specstemming.append(pst.stem(word))
    return(specstemming)

crit=critstemming()
spec=specstemming()
exp=expstemming()
tech=techstemming()
anne=annestemming()
lang=langstemming()

def recruteur(ph):
    text = []
    for sentence in ph:
        words = word_tokenize(sentence)
        stemmed = []
        for word in words:
            if word not in ro :
                if word not in [",","/",".",":"]:
                      stemmed.append(stemmer.lemmatize(word))
        text.append(' '.join(stemmed))
    return(text)


def demande(phrase):
    vec = CountVectorizer(analyzer='word', ngram_range=(1,4) ,tokenizer=TreebankWordTokenizer().tokenize)
    X = vec.fit_transform(phrase)
    liste=vec.get_feature_names()
    return(liste)


def final(phrase):
    stemmedtok = recruteur(phrase)
    final = demande(stemmedtok)
    return (final)


def affiche(demande):
    input = [demande]
    test2 = final(input)
    test_ia = 1
    test_ml = 1
    liste_tech = []
    liste_crit = []
    liste_spec = []
    liste_lang = []
    liste_exp = []
    liste_anne = []
    liste_ia = ['ia', 'ai', 'IA', 'AI', 'intelligence artificielle', "l'intelligence artificielle"]
    liste_ml = ['ml', 'machine learning', 'ML']
    offre = {}
    # offre= {"téchnologie":,"critére":,"specialité":,"expérience","langue":,"année_experience":}
    for word in test2:
        if (pst.stem(word.lower())) in tech:
            if (word not in liste_tech):
                if (word in liste_ml):
                    if test_ml == 1:
                        test_ml = 0
                        liste_tech.append('machine learning')
                elif (word in liste_ia):
                    if test_ia == 1:
                        test_ia = 0
                        liste_tech.append('intelligence artificielle')
                else:
                    liste_tech.append(word)
    offre["téchnologies"] = liste_tech

    for word in test2:
        if pst.stem(word.lower()) in crit:
            if word not in liste_crit:
                liste_crit.append(word)
    offre["critére"] = liste_crit
    for word in test2:
        if pst.stem(word.lower()) in spec:
            if word not in liste_spec:
                liste_spec.append(word)
    offre["specialité"] = liste_spec
    for word in test2:
        if pst.stem(word.lower()) in exp:
            if word not in liste_exp:
                liste_exp.append(word)
    offre["expériences"] = liste_exp
    for word in test2:
        if pst.stem(word.lower()) in lang:
            if word not in liste_lang:
                liste_lang.append(word)
    offre["langages"] = liste_lang
    for word in test2:
        if pst.stem(word.lower()) in anne:
            if int(word[0]) > 1:
                if word not in liste_anne:
                    liste_anne.append(word.replace('an', 'ans'))
                    offre["années_expérience"] = liste_anne
            else:
                liste_anne.append(word)
                offre["années_expérience"] = liste_anne
    return (offre)


#input="bonjour, je demande des stagiers qui maitrisent les technologies suivantes :java,c++, ML, ia, machine learning, ia , l'intelligence artificielle
# , Csharp et qui ont des des experiences en des club
# ou des entreprises et il a des compétences techniques. je souhaite qu'il maitrise la langage russe. 6 ans d'expérience"
#print(affiche(input))
