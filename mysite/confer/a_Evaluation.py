import os
from collections import Counter
import moviepy.editor as mp
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from confer.e_classification_emotion import classification_video
from confer.a_pdf_to_segment import segment
from confer.b_data_extraction import affiche
from confer.c_sentiment_analysis import analyser
from confer.d_classification_photo import classification

# Profil , Expérience académique , Hard skills et projets , Soft skills , certifications et compétitions


def competences(id_candidat,cv_path):
    cv = segment(id_candidat, cv_path)
    if 'Expérience académique' in cv:
        exp = cv['Expérience académique']
    else:
        exp = ''
    if 'Hard skills et projets' in cv:
        hard = cv['Hard skills et projets']
    else:
        hard = ''
    if 'Soft skills' in cv:
        soft = cv['Soft skills']
    else:
        soft = ''
    if 'certifications et compétitions' in cv:
        cert = cv['certifications et compétitions']
    else:
        cert = ''

    extraction = exp + hard + soft + cert
    return(affiche(extraction))

def evaluation_photo(id_candidat,cv_path):
    return(round(classification(id_candidat, cv_path)))




def evaluation(reponse):
    sentiment = analyser(reponse)
    if(sentiment <= -1 ):
        return 0
    if(sentiment > -1 and sentiment <= 0):
        return 1
    if(sentiment > 0 and sentiment <= 1):
        return 2
    else:
        return 3

def to_list(dict):
    list_rec = []
    for valeur in dict.values():
        for j in valeur:
            list_rec.append(j)
    return(list_rec)

def matching(dict_cv,dict_rec):
    matching = 0
    list_rec = to_list(dict_rec)
    list_cand = to_list(dict_cv)
    for i in list_rec:
        for j in list_cand:
            if i == j:
                matching = matching+1
    return round(matching / len(list_rec) * 100)

def evaluation_video(path_video,id_candidat):
    list = []
    #clip = mp.VideoFileClip(path_video).subclip(22,25)
    #clip.audio.write_audiofile('emotion_detection/dataset/data_emotion_jpg/candidats_to_audio/'+str(id_candidat)+".wav")
    coeff = classification_video(path_video,id_candidat)
    #list.append(coeff)
    return(coeff)

#print(evaluation_video('1.mp4',7))
