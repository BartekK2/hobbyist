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
                if 'next' in request.GET:
                    return redirect(request.GET.get('next'))
                else:
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
        if request.method == 'POST':
            form, profile_form = CreateUserForm(request.POST), UserProfileForm(request.POST)
            if form.is_valid() and profile_form.is_valid():
                if is_field_unique(form, "email", User):
                    user, profile = form.save(), profile_form.save(commit=False)
                    # Saving address
                    if profile_form.cleaned_data.get('place'):
                        try:
                            profile.place = geolocalize(profile_form)
                        except:
                            profile.place = ''
                            messages.warning(request, "Nie udało się ustalić miejsca skąd pochodzisz być może jest to chwilowy błąd, spróbuj później to zmienić w ustawieniach profilu")
                    profile.user = user
                    profile.save()
                    send_email(form)
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
        obiekty = Post.objects.filter(autor=request.user).order_by('-id')
        post_numbers = Post.objects.filter(autor=request.user).count()
        if request.method == 'POST':
            profile_form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user.userprofile)
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                try:
                    profile.place = geolocalize(profile_form)
                except:
                    profile.place = ''
                profile.save()
                return redirect('Profil', request.user.id)
        paginator = Paginator(obiekty, 12)
        strona = request.GET.get('strona')
        obiekty = paginator.get_page(strona)
        kontekst = {'profile_form': profile_form, 'obiekty': obiekty}
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
                return redirect('Profil', pk=pk)
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
            if obj.userprofile.profile_pic:
                obj.userprofile.profile_pic.delete()
            obj.delete()
            return redirect('Logowanie')
        kontekst = {"user": obj}
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
        kontekst = {"post": obj}
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
            return redirect('S_post', pk=pk)

    kontekst={
        'post': post,
        'form':form,
        'comments': comments,
    }
    return render(request, "singlepost.html", kontekst)

# ...COMMENTS...
@login_required()
def delete_comment(request, pk, postpk):
    comment = get_object_or_404(Comment, id=pk)
    comment.delete()
    return redirect('S_post', pk=postpk)

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
            return redirect('MeetMe!')
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

def info(request):
    return render(request, "info.html")
def oTworcach(request):
    return render(request, "about.html")
@login_required()
def kontakt(request):
    form = SendMessageForm()
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            send_email(form, email_type=2, username=request.user.username)
            return redirect('MeetMe!')
    kontekst={
        'form':form,
    }
    return render(request, "kontakt.html", kontekst)