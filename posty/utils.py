# HTML EMAIL
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# Dodalem to bo zwykle unique nie pozwalalo na required = False (wartość null też była unikalna)
def is_field_unique(form, field, model):
    if form.cleaned_data.get(field) != "" and model.objects.filter(**{field: form.cleaned_data.get(field)}):
        return False
    return True


def send_email(form, title):
    # Sending emails
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