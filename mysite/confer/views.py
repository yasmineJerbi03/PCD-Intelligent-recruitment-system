from django.shortcuts import render, redirect
from confer.models import offre, submit, candidat, recruteur
from confer.a_pdf_to_segment import segment
from confer.a_Evaluation import competences, evaluation_photo, matching, to_list, evaluation, evaluation_video
import confer.b_data_extraction, confer.c_sentiment_analysis, confer.d_photo_extraction
from confer.b_data_extraction import affiche
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import *
import datetime

from django.contrib.auth.forms import UserCreationForm
from .decorators import *
from django.contrib.auth.models import Group


@recruteur_only
def rindex(request):
    off = offre.objects.filter()
    rec = recruteur.objects.filter()
    offres = offre.objects.raw('SELECT * FROM confer_offre order by id desc ')
    if request.method == 'POST':
        id2 = request.POST.get('idof', None)
        user1 = offre.objects.filter(id=id2)
        if user1 is not None:
            return render(request, 'job-detail.html', {"users": user1})
        endif
    else:
        return render(request, 'rindex.html', {'offs': off, 'recs': rec, 'offres': offres})


def index(request):
    off = offre.objects.filter()
    if request.method == 'POST':
        id2 = request.POST.get('idof', None)
        user1 = offre.objects.filter(id=id2)
        if user1 is not None:
            return render(request, 'job-detail.html', {"users": user1})
        endif
    else:
        return render(request, 'index.html', {'offres': off})


@candidat_only
def cindex(request):
    offres = offre.objects.raw('SELECT * FROM confer_offre order by id desc ')
    if request.method == 'POST':
        id2 = request.POST.get('idof', None)
        request.session['username'] = id2
        # user1 = offre.objects.filter(id=id2)
        return redirect(job_detailc)
    else:
        return render(request, 'cindex.html', {'offres': offres})


def dir_ins(request):
    return render(request, 'register.html')


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        #  register=register()
        username = request.POST["username"]
        mot_passe = request.POST["PASSWORD"]
        user = authenticate(username=username, password=mot_passe)
        if user is not None:
            login(request, user)
            # usern=candidat.objects.filter(user=username)
            return redirect('profil_cand')
        else:
            messages.info(request, 'Username or Password is incorrect')
    return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('index')


@unauthenticated_user
def choix_candidat(request):
    form = CreateUserForm()
    global usr, mdp
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            mot_passe = form.cleaned_data.get('password1')
            # messages.success(request,'Account was created for'+username)
            group = Group.objects.get(name='les_candidats')
            user.groups.add(group)
            candidat.objects.create(
                user=user,
                email=request.POST['email'],
                description=request.POST['description'],
                github=request.POST['github'],
                linkedin=request.POST['linkedin'],
            )
        else:
            username = ''
            mot_passe = ''
        user1 = authenticate(username=username, password=mot_passe)
        if user1 is not None:
            login(request, user1)
            # usern=candidat.objects.filter(user=username)
            return redirect('cindex')

    context = {'form': form}
    return render(request, 'register-candidat.html', context)


@unauthenticated_user
def choix_hr(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            mot_passe = form.cleaned_data.get('password1')
            # messages.success(request,'Account was created for'+username)
            group = Group.objects.get(name='les_recruteurs')
            user.groups.add(group)
            recruteur.objects.create(
                user=user,
                email=request.POST['email'],
                societe=request.POST['societe'],
            )
        else:
            username = ''
            mot_passe = ''
        user = authenticate(username=username, password=mot_passe)
        if user is not None:
            login(request, user)
            # usern=candidat.objects.filter(user=username)
            return redirect('profil_recr')

    context = {'form': form}
    return render(request, 'register-recruteur.html', context)


def job_detail(request):
    return render(request, 'job-detail.html')


from django.urls import reverse


def job_detailc(request):
    idf = request.session['username']
    user1 = offre.objects.filter(id=idf)
    if request.method == 'POST':
        id2 = request.POST.get('idof', None)
        request.session['username'] = id2
        # q=0
        # offre.objects.raw('SELECT question into'+ q+ 'FROM confer_offre where id='+id2)
        # request.session['question']= q
        return redirect(submitresume)
    else:
        return render(request, 'job-detailc.html', {"users": user1})


@recruteur_only
def job_applications(request):
    dict = {}
    off = offre.objects.filter(recruteur=recruteur.objects.get(user=request.user))

    context = {'offs': off}
    if request.method == 'POST':
        id = request.POST.get('idof', None)
        sub = submit.objects.raw('SELECT * FROM confer_submit where offre_id= ' + id)

        print(f'......................................................{id}')
        return render(request, 'ranking.html', {'dict': sub})
    else:
        return render(request, 'applications.html', context)


def ranking(request):
    return render(request, 'ranking.html')


@candidat_only
def mes_offres(request):
    off1 = submit.objects.filter(candidat=candidat.objects.get(user=request.user))
    context = {"offres": off1}
    return render(request, 'mes-offres.html', context)


def about(request):
    return render(request, 'about-us.html')


def aboutc(request):
    return render(request, 'about-usc.html')


def aboutr(request):
    return render(request, 'about-usr.html')


@allowed_users(allowed_roles=['les_candidats', 'les_recruteurs'])
@candidat_only
def profil_cand(request):
    cand = request.user.candidat
    form = candidatForm(instance=cand)
    if request.method == 'POST':
        form = candidatForm(request.POST, request.FILES, instance=cand)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'profil_candidat.html', context)


@recruteur_only
def profil_recr(request):
    recrut = request.user.recruteur
    form = recruteurForm(instance=recrut)
    if request.method == 'POST':
        form = recruteurForm(request.POST, request.FILES, instance=recrut)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, "profil_recruteur.html", context)


@recruteur_only
def demandeoffre(request):
    global register
    if request.method == 'POST':
        register = offre()
        salaire = request.POST['SALAIRE']
        annonce = request.POST['OFFRE']
        deadline = str(request.POST.get('deadline'))
        question = request.POST['question']
        register.deadline = deadline
        register.question = question
        register.salaire = salaire
        register.annonce = annonce
        register.date_publication = datetime.datetime.today().strftime('%Y-%m-%d')
        register.extraction = affiche(annonce)
        register.recruteur = recruteur.objects.get(user=request.user)
        register.save()
        user = offre.objects.filter(annonce=annonce)
        if user is not None:
            return render(request, 'job-detail.html', {"users": user})
        endif
    else:
        return render(request, 'form-recruteur.html')


# Create your views here.
@recruteur_only
def ranking(request):
    return render(request, 'ranking.html')


@candidat_only
def submitresume(request):
    global register
    idf = request.session['username']
    user1 = offre.objects.filter(id=idf)
    if request.method == 'POST':
        register = submit()
        cv = request.FILES['cv']
        id_annonce = request.POST['id_offre']
        print(id_annonce)
        test = request.POST['reponse']
        fs = FileSystemStorage()
        cv_path = fs.save(cv.name, cv)
        register.cv = 'static/images/hire/' + cv_path
        register.test = test
        register.offre = offre.objects.get(id=id_annonce)
        register.candidat = candidat.objects.get(user=request.user)
        register.cv_extraction = competences(register.candidat.id, 'static/images/hire/' + cv_path)
        print(f'.......................................{register.cv_extraction}')
        register.res_test = evaluation(test)
        print(f'.......................................{register.res_test}')
        ann = register.offre.extraction
        register.res_cv = matching(register.cv_extraction, ann)
        register.res_photo = evaluation_photo(register.candidat.id, 'static/images/hire/' + cv_path)
        register.rank = round((register.res_cv + register.res_test + register.res_photo) / 3)
        register.save()
        if matching(register.cv_extraction, ann) >= 40:
            #request.session['id_annonce'] = id_annonce
            return redirect(subvideo)
        return render(request, 'cindex.html')
        return render(request, 'cindex.html')
    else:
        return render(request, 'submitresume.html', {"users": user1})

import moviepy.editor as mp

def subvideo(request):
    idf = request.session['username']
    user1 = offre.objects.get(id=idf)
    if request.method == 'POST':
        video = request.FILES['video']
        fs = FileSystemStorage()
        video_path = fs.save(video.name, video)
        off1 = submit.objects.get(candidat=candidat.objects.get(user=request.user),offre=user1)
        off1.video = 'static/images/hire/' + video_path
        off1.res_video = evaluation_video('static/images/hire/1.wav',1)
        off1.save()
        return redirect (cindex)
    return render(request,"video.html")
# @candidat_only
# def notification(request):
#    offres = offre.objects.raw('SELECT * FROM confer_offre order by id desc ')
#   if request.method == 'POST':
#      id2 = request.POST.get('idof', None)
#   request.session['username']=id2
# user1 = offre.objects.filter(id=id2)
#   return redirect(index)
#  else:
#  return render(request, 'notification.html', {'offres': offres})
