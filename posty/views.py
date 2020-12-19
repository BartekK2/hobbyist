from django.shortcuts import render, redirect, get_object_or_404  # Rendering
from .forms import *  # Forms
from django.conf import settings  # Settings
# Models
from .models import Post, Comment
from django.contrib.auth.models import User
# Login and authentication system
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .filters import PostFilter  # Filter posts by for example category etc.
from django.core.paginator import Paginator  # Next and previous pages
from geopy.geocoders import Nominatim  # Get city by address for example post card
# HTML EMAIL
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# ...PROFILE & USERS...
def login_page(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('MeetMe!')
    else:
        kontekst = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('MeetMe!')
            else:
                messages.info(request, 'Login lub hasło nie poprawne')
        return render(request, "login.html", kontekst)


def logout_user(request):
    logout(request)
    return redirect('Logowanie')


def registration(request):
    if request.user.is_authenticated:
        return redirect('MeetMe!')
    else:
        form, profile_form = CreateUserForm(), UserProfileForm()
        geolocator = Nominatim(user_agent='meet_my')
        if request.method == 'POST':
            form, profile_form = CreateUserForm(request.POST), UserProfileForm(request.POST)
            if form.is_valid() and profile_form.is_valid():
                if is_field_unique(form, "email", User):
                    user, profile = form.save(), profile_form.save(commit=False)
                    # Saving address
                    if profile_form.cleaned_data.get('place') != "":
                        try:
                            location_ = profile_form.cleaned_data.get('place')
                            location = geolocator.geocode(location_, addressdetails=True, timeout=None)
                            info = location.raw['address']
                            # sprawdz czy dana wartosc zwroci miasto czy wieś i uzyskaj to co zwróciła
                            city = info['city'] if 'city' in info else info['village']
                            profile.place = city
                        except:
                            profile.place = ''
                            messages.success(request, "Nie udało się ustalić miejsca skąd pochodzisz być może jest to chwilowy błąd, spróbuj później to zmienić w ustawieniach profilu")
                    profile.user = user
                    profile.save()
                    # Sending emails
                    if form.cleaned_data.get("email"):
                        html_email = render_to_string("email_template.html", {'username': form.cleaned_data.get('username')})
                        text_email = strip_tags(html_email)
                        email = EmailMultiAlternatives(
                            'Hobbyist.pl Podziękowanie za rejestracje',
                            text_email,
                            settings.EMAIL_HOST_USER,
                            [form.cleaned_data.get('email')],
                        )
                        email.attach_alternative(html_email, "text/html")
                        email.send()
                    username = form.cleaned_data.get('username')
                    messages.success(request, f'Konto użytkownika {username} zostało stworzone.')
                    return redirect('Logowanie')
                else:
                    messages.success(request, 'Istnieje już użytkownik z takim Emailem prosze wybierz inny lub zaloguj sie na swoje konto')
        kontekst = {'form': form, 'profile_form': profile_form}
        return render(request, "registration.html", kontekst)


@login_required
def edit_profile(request):
        profile_form = UserProfileForm(instance=request.user.userprofile)
        obiekty = Post.objects.filter(autor=request.user).order_by('-data')
        if request.method == 'POST':
            profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user.userprofile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('Profil', request.user.id)
        kontekst = {'profile_form': profile_form, 'obiekty':obiekty}
        return render(request, "editprofile.html", kontekst)


@login_required()
def profile(request, pk):
    profile_user = get_object_or_404(User, id=pk)
    obiekty = Post.objects.filter(autor=profile_user).order_by('-id')
    post_numbers = Post.objects.filter(autor=profile_user).count()
    if profile_user == request.user:
        form = CreatePostForm()
        if request.method == 'POST':
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.autor = request.user
                post.save()

    paginator = Paginator(obiekty, 12)
    strona = request.GET.get('strona')
    obiekty = paginator.get_page(strona)
    kontekst = {
        "profile_user": profile_user,
        "obiekty": obiekty,
        "post_numbers": post_numbers,
    }
    if profile_user == request.user: kontekst['form'] = form
    return render(request, "profile.html", kontekst)


@login_required()
def delete_user(request, pk):
    obj = get_object_or_404(User, id=pk)
    if request.user == obj:
        if request.method == "POST":
            obj.delete()
            return redirect('Logowanie')
        kontekst = {"user":obj}
        return render(request, "delete_post.html", kontekst)
    else:
        return redirect('MeetMe!')


# ...POSTS...
@login_required()
def delete_post(request, pk):
    obj = get_object_or_404(Post, id=pk)
    if request.user == obj.autor:
        if request.method == "POST":
            obj.delete()
            return redirect('MeetMe!')
        kontekst = {"post":obj}
        return render(request, "delete_post.html", kontekst)
    else:
        return redirect('MeetMe!')


@login_required()
def show_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=post).order_by('-id')
    form = CreateCommentForm()
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.autor = request.user
            comment.post = post
            comment.save()

    kontekst={
        'post': post,
        'form':form,
        'comments': comments,
    }
    return render(request, "singlepost.html", kontekst)


# ...OTHER...
@login_required()
def index(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.city = request.user.userprofile.place
            post.save()
    obiekty = Post.objects.filter().order_by('-id')
    myFilter = PostFilter(request.GET, queryset=obiekty)
    obiekty = myFilter.qs
    paginator = Paginator(obiekty, 12)
    strona = request.GET.get('strona')
    obiekty = paginator.get_page(strona)
    kontekst = {
        "obiekty": obiekty,
        "css": "css/main.css",
        "form": form,
        "myFilter": myFilter,
    }
    return render(request, "mainpage.html", kontekst)
