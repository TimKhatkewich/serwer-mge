from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import VotingSession, Choice, Vote
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.contrib.auth import get_user_model




def home(request):
    return render(request, 'home_page.html')


def glosowania(request):
    sessions = VotingSession.objects.prefetch_related('choices').all()
    voted_session_ids = []
    if request.user.is_authenticated:
        voted_session_ids = list(Vote.objects.filter(user=request.user).values_list('session_id', flat=True))

    return render(request, 'glosowania.html', {
        'sessions': sessions,
        'voted_session_ids': voted_session_ids,
    })


def vote(request, choice_id) -> HttpResponseRedirect:
    choice = get_object_or_404(Choice, id=choice_id)
    session = choice.session

    if not request.user.is_authenticated:
        messages.error(request, 'Musisz być zalogowany, aby zagłosować.')
    elif not session.is_active:
        messages.warning(request, 'To głosowanie jest już zakończone.')
    else:
        already_voted = Vote.objects.filter(user=request.user, session=session).exists()
        if not already_voted:
            Vote.objects.create(user=request.user, session=session, choice=choice)
            choice.votes += 1
            choice.save()
            messages.success(request, 'Twój głos został zapisany.')
        else:
            messages.warning(request, 'Możesz zagłosować tylko raz w tej sesji.')

    return redirect('glosowania')
def dodaj_glosowanie(request):
    if request.method == "POST":
        name = request.POST.get("name")
        choices = request.POST.getlist("choices[]")
        session = VotingSession.objects.create(name=name)
        for choice_text in choices:
            if choice_text.strip() != "":
                Choice.objects.create(session=session, text=choice_text)

        return redirect('glosowania')

    return render(request, 'dodaj_glosowanie.html')

def onas(request):
    return render(request, 'o_nas.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        user_model = get_user_model()

        if not username or not password or not password_confirm:
            messages.error(request, 'Wypełnij wszystkie pola.')
        elif password != password_confirm:
            messages.error(request, 'Hasła nie są takie same.')
        else:
            if user_model.objects.filter(username=username).exists():
                messages.error(request, 'Użytkownik o tej nazwie już istnieje.')
            else:
                user_model.objects.create_user(username=username, password=password)
                messages.success(request, 'Konto zostało utworzone. Zaloguj się.')
                return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło.')
    return render(request, 'login.html')


