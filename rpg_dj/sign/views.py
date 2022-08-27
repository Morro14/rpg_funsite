from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import BaseRegisterForm
from .email import send_registration_code
from .models import OneTimeCode
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


User = get_user_model()


class BaseRegisterView(CreateView):
    model = get_user_model()
    form_class = BaseRegisterForm
    success_url = '/board'


def register_with_code(request):
    if request.method == 'GET':
        form = BaseRegisterForm()
        return render(request, template_name='sign/sign_up.html', context={'form': form})
    if request.method == 'POST':
        form = BaseRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            create_code = OneTimeCode.objects.create(user=user.username)
            # единственный способ перенести user.pk и код до регистрации, который я нашел - через url encode
            # возможно, лучше создать промежуточную модель и сохранять инфо в ней?
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            code_pk = urlsafe_base64_encode(force_bytes(create_code.pk))
            send_registration_code(user.email, create_code.code)
            return redirect('verification', uidb64=uid, token=code_pk)
        else:
            return redirect('exception')


def verification(request, uidb64, token):
    if request.method == 'GET':
        return render(request, template_name='sign/verification.html')
    if request.method == 'POST':
        #        try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        code_pk = smart_str(urlsafe_base64_decode(token))
        code_user = OneTimeCode.objects.get(pk=code_pk)
        #        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        #            user = None

        if user is not None and code_user.code == request.POST.get('code'):
            user.is_active = True
            user.email_confirmed = True
            try:
                user.save()
                login(request, user)
                return redirect('/board')

            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                return redirect('exception')


def exception(request):
    return render(request, template_name='exceptions/exception_1.html')
