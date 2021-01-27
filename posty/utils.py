# HTML EMAIL
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from geopy.geocoders import Nominatim  # Get city by address for example post card
from .models import User
from django.core.exceptions import ValidationError

# Dodalem to bo zwykle unique nie pozwalalo na required = False (wartość null też była unikalna)
def is_email_unique(value):
    if value != "" and User.objects.filter(**{'email': value}):
        raise ValidationError('Istnieje już użytkownik z takim Emailem prosze wybierz inny lub zaloguj sie na swoje konto')
    return True


def send_email(form, title='Hobbyist.pl Podziękowanie za rejestracje', email_type=1, username=None, text=None):
    # Sending emails
    if email_type == 1:
        if form.cleaned_data.get("email"):
            html_email = render_to_string("email_template.html", {'username': form.cleaned_data.get('username')})
            text_email = strip_tags(html_email)
            email = EmailMultiAlternatives(
                title,
                text_email,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data.get('email')],
            )
            email.attach_alternative(html_email, "text/html")
            email.send()
    elif email_type == 2:
        email = EmailMultiAlternatives(
            username+form.cleaned_data.get("title_email"),
            form.cleaned_data.get("opis"),
            settings.EMAIL_HOST_USER,
            ['hobbyistpl@gmail.com', 'barteksp82@gmail.com'],
        )
        email.send()


def geolocalize(profile_form):
    geolocator = Nominatim(user_agent='meet_my')
    if profile_form.cleaned_data.get('place') != "":
        location_ = profile_form.cleaned_data.get('place')
        location = geolocator.geocode(location_, addressdetails=True, timeout=None)
        info = location.raw['address']
        # Poszukaj wśród danych zwróconych możliwe dane zwracające np miasto wieś itd
        possibilities = ['city', 'village', 'administrative']
        city = ""
        for x in possibilities:
            if x in info:
                city = info[x]
        if city == "":
            raise ValueError('Nie ustalono')
    return city