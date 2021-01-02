from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='MeetMe!'),
    path('login/', views.login_page, name='Logowanie'),
    path('wyloguj/', views.logout_user, name='Wylogowanie'),
    path('registration/', views.registration, name='Rejestracja'),
    path('profile/<int:pk>', views.profile, name='Profil'),
    path('profile/<int:pk>/usun', views.delete_user, name='delete_user'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:pk>', views.show_post, name='S_post'),
    path('post/<int:pk>/usun', views.delete_post, name='delete_post'),
    path('info/', views.info, name="Info"),
    path('tworcy/', views.oTworcach, name="o_tworcach"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
