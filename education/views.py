# Create your views here.
from django.template import RequestContext
from django.core.mail import EmailMessage
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


def results(request):
    form = SearchForm()
    query = request.GET.get("search")
    q_list = Education.objects.all().values('name', 'work', 'skills').order_by('name')
    if query:
        q_list = q_list.filter(Q(work = query)).order_by('name')
    return render (request, 'education/results.html', {'query': query,'q_list':q_list,  'form': form})


@login_required
def home(request):
    #name = request.user.username
    return HttpResponseRedirect(reverse(edu_new, args=[request.user.username]))


# def profile(request):
#     name = request.user.username
#    # return HttpResponseRedirect(reverse(edu_new, args=[request.user.username]))
#     return redirect('education/' + name + '/')

def company_no_edit(request, id=id):
    queryset = Company.objects.filter(Q(id=id))
    return(request, 'education/company_non_edit.html', {'queryset': queryset})



def non_edit(request, id=id):

    queryset = Education.objects.all()
    queryset = queryset.filter(Q(id=id))

    return render(request, 'education/non_editable.html', {'queryset': queryset})


def profile(request, name):
    user = get_object_or_404(User, username=name)
    return render(request, 'education/edu_edit.html', {'profile': user})


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
            t = Education.objects.get(user_id= id)
            t_form= SecondaryEducationForm(request.POST, instance= t)
            t_form.save()
            t.save()
            return redirect('/login/education/unedit/%s/' %id)
            # t.user_id = request.user
            # t.created_date = timezone.now()
            # t.save()
    else:
        t = Education.objects.get(user_id = id)
        t_form = SecondaryEducationForm(instance= t)

        return render(request, 'education/edu_edit.html', {'form': t_form})





# def emailSection(request, id):
#         queryset = Education.objects.filter(Q(id=id))
#         for q in queryset:
#             email = EmailMessage('Subject: Hii', 'Body: abcd', to=[q.email_id])
#             email.send()
#         return render(request, 'education/mail_confirm.html')
#
#                   )

# def edu_new(request):
#     if request.method == "POST":
#         form = SecondaryEducationForm(request.POST)
#         if form.is_valid():
#             Education = form.save(commit=False)
#             Education.user_id = request.user
#             Education.created_date = timezone.now()
#             Education.save()
#     else:
#         form = SecondaryEducationForm()
#     return render(request, 'education/edu_edit.html', {'form': form, })

#
# def edu_editable(request, name):
#     # user = get_object_or_404(User, userid=name)
#   #  entry = Education.objects.get(Q(id=id))
#     if request.method == "POST":
#         form = SecondaryEducationForm(request.POST)
#         if form.is_valid():
#             Education = form.save(commit=False)
#             Education.userID = request.user
#             Education.created_date = timezone.now()
#             Education.save()
#     else:
#         form = SecondaryEducationForm()
#     return render(request, 'education/edu_edit.html', {'form': form, })

def company_new(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            Education = form.save(commit=False)
            # Education.userID = request.user
            Education.created_date = timezone.now()
            Education.save()
    else:
        form = CompanyForm()
    return render(request, 'education/company_form.html', {'form': form, })

