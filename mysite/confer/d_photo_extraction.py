import fitz
import cv2
import os
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def extract_image(id_candidat, path_pdf):
    pdf = fitz.open(path_pdf)
    image_list = pdf.getPageImageList(0)
    i = 0
    for image in image_list:
        xref = image[0]
        pix = fitz.Pixmap(pdf, xref)
        if pix.n < 4:
            pix.writePNG(f'confer/photo_analysis/dataset/photo/candidats/{id_candidat}_{i}.png')
        else:
            pixint = fitz.Pixmap(fitz.csGRAY, pix)
            pixint.writePNG(f'confer/photo_analysis/dataset/photo/candidats/{id_candidat}_{i}.png')
        i = i + 1

    face_cascade = cv2.CascadeClassifier('confer/photo_analysis/models/haarcascade_frontalface_alt.xml')
    fichier = os.listdir('confer/photo_analysis/dataset/photo/candidats/')
    for nom in fichier:
        if nom.startswith(f'{id_candidat}_'):
            img = cv2.imread('confer/photo_analysis/dataset/photo/candidats/' + nom)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 1)
            if len(faces) == 0:
                os.remove('confer/photo_analysis/dataset/photo/candidats/' + nom)
            else:
                continue
    fichier = os.listdir('confer/photo_analysis/dataset/photo/candidats/')
    for nom in fichier:
        if nom.startswith(f'{id_candidat}_'):
            profile_cascade = cv2.CascadeClassifier('confer/photo_analysis/models/haarcascade_profileface.xml')
            img = cv2.imread('confer/photo_analysis/dataset/photo/candidats/' + nom)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = profile_cascade.detectMultiScale(gray, 1.1, 1)
            if len(faces) == 0:
                os.remove('confer/photo_analysis/dataset/photo/candidats/' + nom)
            else:
                os.rename('confer/photo_analysis/dataset/photo/candidats/' + nom, f'confer/photo_analysis/dataset/photo/candidats/{id_candidat}.png')
                fichier = os.listdir('confer/photo_analysis/dataset/photo/candidats/')
                for nom in fichier:
                    if nom.startswith(f'{id_candidat}_'):
                        os.remove('confer/photo_analysis/dataset/photo/candidats/' + nom)
#os.chdir('../')
#extract_image(10, 'cv_analysis/dataset/aa.pdf')