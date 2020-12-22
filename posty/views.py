from django.shortcuts import render, redirect, get_object_or_404  # Rendering
from .forms import *
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
from .utils import *


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
                messages.error(request, 'Login lub hasło nie poprawne')
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
                            print(info)
                            # Poszukaj wśród danych zwróconych możliwe dane zwracające np miasto wieś itd
                            possibilities = ['city', 'village', 'administrative']
                            city = ""
                            for x in possibilities:
                                if x in info:
                                    city = info[x]
                            if city == "":
                                raise ValueError('Nie ustalono')
                            profile.place = city
                        except:
                            profile.place = ''
                            messages.warning(request, "Nie udało się ustalić miejsca skąd pochodzisz być może jest to chwilowy błąd, spróbuj później to zmienić w ustawieniach profilu")
                    profile.user = user
                    profile.save()
                    send_email(form, 'Hobbyist.pl Podziękowanie za rejestracje')
                    username = form.cleaned_data.get('username')
                    messages.success(request, f'Konto użytkownika {username} zostało stworzone.')
                    return redirect('Logowanie')
                else:
                    messages.error(request, 'Istnieje już użytkownik z takim Emailem prosze wybierz inny lub zaloguj sie na swoje konto')
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
    if 'city' in request.GET:
        # nowy sącz -> Nowy Sącz, kraków -> Kraków
        request.GET = request.GET.copy()  # odpakuj żeby dało się zmienić wartość
        request.GET['city'] = request.GET['city'].title()  # Zmień wartość na tą samą ale z dużych liter
    myFilter = PostFilter(request.GET, queryset=Post.objects.filter())
    obiekty = myFilter.qs.order_by('-id')
    paginator = Paginator(obiekty, 12)
    strona = request.GET.get('strona')
    obiekty = paginator.get_page(strona)
    kontekst = {
        "obiekty": obiekty,
        "form": form,
        "myFilter": myFilter,
    }
    return render(request, "mainpage.html", kontekst)
<<<<<<< HEAD

def info(request):
    return render(request, "info.html")
=======
>>>>>>> c9ac0423370cae63b8287505511c215f0a989a6c
