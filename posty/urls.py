from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
import django.views.static

urlpatterns = [
    path('', views.index, name='MeetMe!'),
    path('login/', views.login_page, name='Logowanie'),
    path('wyloguj/', views.logout_user, name='Wylogowanie'),
    path('rejestracja/', views.registration, name='Rejestracja'),
    path('profil/<int:pk>', views.profile, name='Profil'),
    path('profil/<int:pk>/usun', views.delete_user, name='delete_user'),
    path('edycja_profilu/', views.edit_profile, name='edit_profile'),
    path('post/<int:pk>', views.show_post, name='S_post'),
    path('post/<int:pk>/usun', views.delete_post, name='delete_post'),
    path('comment/<int:pk>/<int:postpk>/usun', views.delete_comment, name='delete_comment'),
    path('info/', views.info, name="Info"),
    path('tworcy/', views.oTworcach, name="o_tworcach"),
    path('kontakt/', views.kontakt, name="kontakt"),
    path('test/', views.test, name="test"),
]
urlpatterns += [
   url(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}),
   url(r'^static/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
]