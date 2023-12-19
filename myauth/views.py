from django.shortcuts import render

# Create your views here.
def register(request):
    context = dict()
    return render(request, "myauth/register.html", context)

def home(request):
    context = dict()
    return render(request, "myauth/home.html", context)

def login(request):
    context = dict()
    context['title'] = 'Sign in'
    return render(request, "myauth/login.html", context)

def verify(request, token, ):
    context = dict()
    context['title'] = 'Verify'
    return render(request, "myauth/verify.html", context)

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import ( login as auth_login,
    logout as auth_logout, authenticate
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django import template
from myauth.forms import *
from myauth.models import *
from myauth.tasks import send_verification_email
from webcivils import settings


def home(request):
    context = dict()
    return render(request, "basic/home.html", context)


def about(request):
    context = dict()
    context['title'] = "About"
    return render(request, "basic/about.html", context)

def steam(request):
    context = dict()
    context['title'] = "Team"
    return render(request, "basic/team.html", context)


def services(request):
    context = dict()
    context['title'] = "Services"
    return render(request, "basic/services.html", context)


def faq(request):
    context = dict()
    context['title'] = "FAQ"
    return render(request, "basic/faq.html", context)


def login(request):
    context = dict()
    context['title'] = "Login"
    return render(request, "myauth/login.html", context)

def portfolio(request):
    context = dict()
    context['title'] = "Portfolio"
    return render(request, "basic/portfolio.html", context)


# """
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = NewUser.objects.filter(Q(email=data) | Q(username=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					plaintext = template.loader.get_template(
					    'registration/password_reset_email.txt')
					htmltemp = template.loader.get_template('email/confirm.html')
					# htmltemp = template.loader.get_template('registration/password_reset_email.html')
					c = {
					"email": user.email,
					'domain': request.META['HTTP_HOST'],
					'site_name': 'FlexyTuta',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': request.scheme,
                    'web_link':  request.scheme + "://" + request.META['HTTP_HOST'] + "/"
					}
					text_content = plaintext.render(c)
					html_content = htmltemp.render(c)
					try:
						msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [
						                             user.email], headers={'Reply-To': f'{user.email}'})
						msg.attach_alternative(html_content, "text/html")
						msg.send()
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.info(
					    request, "Password reset instructions have been sent to the email address entered.")
					return redirect("password_reset_done")


           
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form, "title":"Reset your password"})
# """
def account_verification(request, uidb64, token):
    from django.utils.http import urlsafe_base64_decode
    user_id = urlsafe_base64_decode(uidb64)
    user_id = int(user_id)
    form = AccountVerificationForm()
    if request.method == "POST":
        form = AccountVerificationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['is_active']
            id = form.cleaned_data['id']
            try:
                user = get_object_or_404(NewUser, pk=int(id))
                user.is_active = True
                user.save()
                #print(user, id)
                messages.success(request, "Your account has been verified successfully, log in now!")
                return redirect ("login")
            except:
                messages.error(request, "This user does not exist")
                return redirect ("register")
    return render(request=request, template_name="registration/account_verification.html", context={"form":form, "title":"Confirm your account", "user_id":user_id})


def logout_view(request):
	auth_logout(request)
	messages.success(request,f"You are now logged out of your account!")
	return redirect('login')




def signup(request):
    context = {
    "title": "Register"
    }


    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))
    request.session['next'] = request.GET.get('next', None)


    user = request.user
    if user.is_authenticated:
        return redirect("profile")

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            form.save()
            user = authenticate(email=email, password=raw_password)
            # print(account, email, raw_password)
            user = get_object_or_404(NewUser, email=email)
            if user is not None:
                auth_login(request, user)
                auth_logout(request)
                auth_login(request, user)
                user.is_active = False
                user.save()
                email = user.email
                
                send_verification_email(request, user)
                messages.success(request,f"Your registration was successful, You can now sign in to your account!")
            
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return redirect(next_url)
                next_url = request.session.get("next")
                if next_url:
                        
                    return redirect(next_url)
                else:
                    return redirect("login")
            else:
                pass
        else:
            # messages.error(request,f"{form.errors}")
            for error in list(form.errors.values()):
                messages.error(request, error)
            context['form'] = form

    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'auth_files/student_register.html', context)




def tutor_register(request):
    context = {
    "title": "Register"
    }


    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))

    # print(f"Session key before loggingin {request.session.session_key}")

    user = request.user
    if user.is_authenticated:
        return redirect("profile")

    form = TutorRegistrationForm(request.POST or None)
    if request.POST:
        form = TutorRegistrationForm(request.POST)
        p_form = TutorAccRegistrationForm(request.POST, request.FILES)
        # if form.is_valid():
        if form.is_valid() and p_form.is_valid():
            p = form.save()


            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account is not None:
                auth_login(request, account)
                user = get_object_or_404(NewUser, email=email)
                # print(user)
                p_form = TutorAccRegistrationForm(request.POST, request.FILES, instance=request.user.profile)
                p_form.save()
                profile = Profile.objects.get(user=request.user)
                profile.occupation = "Applicant Tutor"
                profile.save()
                email = user.email
                
                send_verification_email(request, user)
                auth_logout(request)
                # auth_login(request, account)
                user.is_active = False
                user.save()
                
                """
                SEND VERIFICATION EMAIL
                """
                messages.success(request,f"Your registration was successful, You are now saved as an applicant tutor!")
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return redirect(next_url)
                else:
                    return redirect("login")
            else:
                pass
        else:
            # messages.error(request,f"{form.errors}")
            # print(form.errors)
            for error in list(form.errors.values()):
                messages.error(request, error)
            context['form'] = form
            context['p_form'] = p_form

    else:
        form = TutorRegistrationForm()
        p_form = TutorAccRegistrationForm()
        context['form'] = form
        context['p_form'] = p_form
    return render(request, 'auth_files/tutor_register.html', context)





@login_required(login_url="login")
def profile(request):
    
    if request.method == "POST":
        u_form = AccountUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid():# and p_form.is_valid():
            u_form.save()
            messages.success(request,f"Your account has been updated")
            return redirect("profile")
        else:
            for error in list(u_form.errors.values()):
                messages.error(request, error)

    else:
        u_form = AccountUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "form": u_form,
        # "p_form": p_form,
        "title":"Profile",
    }
    
	
    return render(request,"auth_files/profile.html",context)



def login_view(request):
    context = {
    "title": "Sign In"
    }
    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))
    user = request.user
    if user.is_authenticated:
        return redirect("profile")
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)         
            auth_login(request, user)
            messages.success(request,f"You are now logged in to your account!")

            next_url = cache.get('next')
            if next_url:
                cache.delete('next')
                return redirect(next_url)
            else:
                return redirect("profile")

        else:
            messages.error(request, f"Invalid login credentials.")
            for error in list(form.errors.values()):
                messages.error(request, error)
            context['login_form'] = form

    else:
        form = AccountAuthenticationForm()
        context['login_form'] = form
    return render(request, "auth_files/login.html", context)



def form_submitted(request):
    title="Form Submitted"
    return render(request,"auth_files/form-submitted.html",{"title":title})
