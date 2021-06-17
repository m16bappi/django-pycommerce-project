from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import Accounts

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def registerView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
            mail_subject = "Please active your account"
            message = render_to_string('mail-templates/email_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            to_email = form.cleaned_data['email']
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email='+to_email)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user=user)
            try:
                next = request.GET['next']
                return redirect(next)
            except KeyError:
                return redirect('home')
        else:
            messages.error(request, 'Invaild username or password')
            return redirect('login')
    return render(request, 'signin.html')


def logoutView(request):
    logout(request)
    messages.success(request, 'Your account successfully logout')
    return redirect('login')


def AccountActive(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! your account active successfully')
    else:
        messages.error(request, 'Your activation link Invalid')
    return redirect('login')


@login_required(login_url='login')
def Dashboard(request):
    return render(request, 'dashboard.html')


def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user = Accounts.objects.get(email__iexact=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('mail-templates/reset-password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(
                request, 'Check your email for reset your password!')
            return redirect('login')
        else:
            messages.error(
                request, 'Your email address Invalid! Please enter correct address.')
            return redirect('forget-password')

    return render(request, 'forget-password.html')


def resetPasswordValided(request, uidb64, token):
    return render(request, 'reset-password-valided.html')
