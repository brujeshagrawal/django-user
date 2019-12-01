from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from .forms import SignupForm, ProfileForm, ProfileEditForm, ProfilePicForm
from django.contrib.auth import get_user_model
import json


# Create your views here.

def index(request):
    return render(request, 'reg/index.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                password = form.clean_password2()
            except Exception as e:
                error_message = str(e)
                return render(request, 'reg/user_signup.html',{'form':form, 'error_message':error_message})
            user = form.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('reg/account_activation_mail.html',{'user':user, 'domain':current_site.domain, 'uid':urlsafe_base64_encode(force_bytes(user.pk)),'token':account_activation_token.make_token(user)})
            user.email_user(subject,message)
            return redirect('reg:account_activation_sent')
        else:
            errors = json.loads(form.errors.as_json())
            for field, error in errors.items():
                error_message = error[0]['message']
                if field == 'email':
                    break
            return render(request, 'reg/user_signup.html',{'form':form, 'error_message':error_message})
    else:
        form = SignupForm()
        return render(request, 'reg/user_signup.html',{'form':form})

def account_activation_sent(request):
    return render(request,'reg/account_activation_sent.html')

def activate(request, uid64, token):
    try :
        uid = force_text(urlsafe_base64_decode(uid64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.joined_date = timezone.now()
        user.save()
        return redirect('login')
    else:
        return render(request, 'reg/account_activation_invalid.html')

@login_required
def user_profile(request):
        usr = request.user
        user = get_user_model().objects.get(email=usr)
        form = ProfileForm(instance=user)
        return render(request, 'reg/user_profile.html', {'form':form})

@login_required
def user_profile_edit(request):
    usr = request.user
    user = get_user_model().objects.get(email=usr)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect('reg:user_profile')
        # else:
            # print(form.errors)
            # errors = json.loads(form.errors.as_json())
            # for field, error in errors.items():

    else:
        form = ProfileEditForm(instance=user)
    return render(request, 'reg/user_profile_edit.html', {'form':form})

@login_required
def user_profile_pic_update(request):
    usr = request.user
    user = get_user_model().objects.get(email=usr)
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image_file']
            user.profile_pic = image_file
            user.save()
            return redirect('reg:user_profile')
        else:
            print(form.errors)
    else:
        form = ProfilePicForm()
        return render(request, 'reg/user_profile_pic_update.html', {'form':form})
    