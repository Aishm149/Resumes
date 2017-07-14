from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView
from django.utils.encoding import force_bytes
from because import settings
from because.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from .forms import CompanyForm
from .forms import SecondaryEducationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .forms import SignUpForm
from django.contrib import messages
from .models import Education, Company
from django.db.models import Q
from .forms import SearchForm, SetPasswordForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .forms import PasswordResetRequestForm
from django.utils.encoding import force_text
from .tokens import account_activation_token
from django.template.loader import render_to_string


class PasswordResetConfirmView(FormView):
    template_name = "registration/test_template.html"
    success_url = '/login/'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)


class ResetPasswordRequestView(FormView):
    template_name = "registration/test_template.html"  # code for template is given below the view's code
    success_url = '/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:  # uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            associated_users = User.objects.filter(Q(email=data) | Q(username=data))
            current_site= get_current_site(request)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'registration/password_reset_subject.txt'
                    # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                    email_template_name = 'registration/password_reset_email.html'
                    # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request,
                                 'An email has been sent to ' + data + ". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users = User.objects.filter(username=data)
            current_site = get_current_site(request)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': current_site,
                        # 'domain': 'example.com',  # or your domain
                        # 'site_name': 'example',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'registration/password_reset_subject.txt'
                    email_template_name = 'registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request,
                                 'Email has been sent to ' + data + "'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


def emailSection(request,id=id):
    user_name = request.user.username
    c_email = request.user.email
    id1 = User.objects.filter(Q(username= user_name)).values('id')
    c_name = Company.objects.get(user_id = id1).name

    c_about = Company.objects.get(user_id = id1).about
    c_website = Company.objects.get(user_id = id1).website

    user = User.objects.get(id= id)
    user_email = user.email
    plaintext = get_template('email_text.txt')
    htmly = get_template('email_body.html')

    d = Context({'username': c_name,'about': c_about, 'website': c_website, 'email': c_email})
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives('All about resumes- Shortlisting', text_content, settings.DEFAULT_FROM_EMAIL, [user_email, ])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return render(request, 'education/mail_confirm.html')
# def emailSection(request, id= id):
#     # User = get_user_model()
#     email1 = request.user.email
#     # email1 = User.objects.filter(Q(id =id)).values('email')
#     # queryset = Education.objects.filter(Q(id = id))
#     # for q in queryset:
#     email = EmailMessage('Subject: All About Resumes Shortlisting', 'Body: Hello', to = [email1])
#     email.send()
#     return render(request, 'education/mail_confirm.html')


def results(request):
    form = SearchForm()
    query = request.GET.get("search")
    q_list = Education.objects.all().values('user_id','name', 'work', 'skills' ).order_by('name')
    if query:
        q_list = q_list.filter(Q(work = query)).order_by('name')
    return render (request, 'education/results.html', {'query': query, 'q_list':q_list,  'form': form})

@login_required
def home(request):
    #name = request.user.username
    return HttpResponseRedirect(reverse(edu_new, args=[request.user.username]))


def homepage(request):
    return render(request, 'education/index.html')


def company_no_edit(request, id=id):
    queryset = Company.objects.filter(Q(user_id=id))
    return render(request, 'education/company_uneditable.html', {'queryset': queryset})


def non_edit(request, id=id):
    queryset = Education.objects.filter(Q(user_id=id))
    return render(request, 'education/edu_uneditable.html', {'queryset': queryset})


def candidate_profile(request, id):
    queryset = Education.objects.filter(Q(user_id=id))
    return render(request, 'education/company_search_uneditable.html', {'queryset': queryset})


def profile(request, name):
    user = get_object_or_404(User, username=name)
    return render(request, 'education/edu_edit.html', {'profile': user})

# def login_success(request):
#     test = request.user.first_name
#     if test == '0':
#         return redirect('education/')
#     else:
#         return redirect('company/')
#
#
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('login/')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'account_activation_invalid.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = True

            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your All About Resumes Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_success(request):
    test = request.user.first_name
    test1 = request.user.profile.email_confirmed
    if test1 == True:
        if test == '0':
            return redirect('education/')
        else:
            return redirect('company/')
    #else:
    return render(request, 'education/login_fail.html')

def account_activation_sent(request):

    return render(request, 'education/activate_mail.html')



def edu_new(request, id=id):
    id = request.user.id
    # user = get_object_or_404(User, username = name)  #may be reques.id or id in function arguements
    if request.method == "POST":
        form = SecondaryEducationForm(request.POST)
        if form.is_valid():
            t, created = Education.objects.update_or_create(user_id = id)
            t_form= SecondaryEducationForm(request.POST, instance= t)
            t_form.save()
            t.save()
            return redirect('/unedit/%s/' %id)
            # t.user_id = request.user
            # t.created_date = timezone.now()
            # t.save()
    else:
        t, created = Education.objects.get_or_create(user_id = id)
        t_form = SecondaryEducationForm(instance= t)

        return render(request, 'education/edu_edit.html', {'form': t_form})


# def edu_new(request, id=id):
#     id = request.user.id
#     # user = get_object_or_404(User, username = name)  #may be reques.id or id in function arguements
#     if request.method == "POST":
#         form = SecondaryEducationForm(request.POST)
#         if form.is_valid():
#             t = Education.objects.get(user_id = id)
#             t_form= SecondaryEducationForm(request.POST, instance= t)
#             t_form.save()
#             t.save()
#             return redirect('/unedit/%s/' %id)
#             # t.user_id = request.user
#             # t.created_date = timezone.now()
#             # t.save()
#     else:
#         t = Education.objects.get(user_id = id)
#         t_form = SecondaryEducationForm(instance= t)
#
#         return render(request, 'education/edu_edit.html', {'form': t_form})


def company_new(request, id=id):
    id = request.user.id
    # p = Company.user_id
    # p.save()
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            t, created = Company.objects.update_or_create(user_id = id)
            # t = Company.objects.get(user_id=id)
            t_form = CompanyForm(request.POST, instance=t)
            t_form.save()
            t.save()
            return redirect('/edit/%s/' %id)  # CHECK
            # t.user_id = request.user
            # t.created_date = timezone.now()
            # t.save()
    else:
        t, created = Company.objects.get_or_create(user_id = id)
        t_form = CompanyForm(instance=t)

        return render(request, 'education/edu_edit2.html', {'form': t_form}) # edu_edit2 is HTML for company form

