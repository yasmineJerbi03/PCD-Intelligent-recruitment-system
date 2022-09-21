from django.urls import path
from.import views
urlpatterns = [
    path('', views.index, name='index'),
    path('HR', views.rindex, name='rindex'),
    path('Candidate', views.cindex, name='cindex'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('job_applications', views.job_applications, name='job_applications'),
    path('job_detail', views.job_detail, name='job_detail'),
    path('job_detailc', views.job_detailc, name='job_detailc'),
    path('mes_offres',views.mes_offres,name='mes_offres'),
    path('about', views.about, name='about'),
    path('aboutc', views.aboutc, name='aboutc'),
    path('aboutr', views.aboutr, name='aboutr'),
    path('subvideo', views.subvideo, name='subvideo'),
    path('demandeoffre', views.demandeoffre, name='demandeoffre'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('submitresume', views.submitresume, name='submitresume'),
    path('profil_recr',views.profil_recr, name='profil_recr'),
    path('profil_cand',views.profil_cand, name='profil_cand'),
    path('choix_hr', views.choix_hr, name='choix_hr'),
    path('ranking', views.ranking, name='ranking'),
    path('choix_candidat', views.choix_candidat, name='choix_candidat'),
    path('dir_ins', views.dir_ins, name='dir_ins'),
    #path('notification/',views.notification,name='notification'),
]
