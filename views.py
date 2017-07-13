from django.template import RequestContext, Context
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template

from .forms import CompanyForm
from .forms import SecondaryEducationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .forms import SignUpForm
from django.utils import timezone
from .models import Education, Company
from django.db.models import Q
from .forms import SearchForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from because import settings



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

def login_success(request):
    test = request.user.first_name
    if test == '0':
        return redirect('education/')
    else:
        return redirect('company/')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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

