# Create your views here.
import logging
from .forms import (
    CompanyForm,
    SecondaryEducationForm,
    SignUpForm
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponseRedirect
)
from django.core.urlresolvers import reverse
from django.utils import timezone
from .models import Education
from django.db.models import Q
from .forms import SearchForm, LoginForm
from django.contrib.auth.models import User

logger = logging.getLogger()


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile')
    else:
        ctx = {}
        ctx['form'] = LoginForm()
        return render(request, 'login.html', ctx)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def authuser(request):
    authdata = LoginForm(request.POST or None)
    if request.method == 'POST':
        if authdata.is_valid():
            logger.debug('in views')
            user = User.objects.get(
                email=authdata.cleaned_data["email"],
                username=authdata.cleaned_data["username"])
            username = user.get_username()
            user = authenticate(
                username=username,
                password=authdata.cleaned_data["password"]
            )
            logger.debug(user, 'authenticated')
            if user is not None:
                logger.debug(user)
                if user.is_active:
                    logger.debug(user, 'here')
                    auth_login(request, user)

                    return HttpResponseRedirect('/profile')
        else:
            c = {'form': authdata}
            return render(request, 'login.html', c)
    else:
        authdata = LoginForm()
        c = {'form': authdata}
        return render(request, 'login.html', c)


def results(request):
    form = SearchForm()
    query = request.GET.get("search")
    q_list = Education.objects.all().values('name', 'work', 'skills').order_by('name')
    if query:
        q_list = q_list.filter(Q(work = query)).order_by('name')
    return render (request, 'education/results.html', {'query': query ,'q_list':q_list,  'form' : form })


@login_required
def home(request):
    #name = request.user.username
    return HttpResponseRedirect(reverse(edu_new, args=[request.user.username]))


# def profile(request):
#     name = request.user.username
#    # return HttpResponseRedirect(reverse(edu_new, args=[request.user.username]))
#     return redirect('education/' + name + '/')


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
            login(request)
            return HttpResponseRedirect('/profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



@login_required(login_url='/login/')
def profile(request):
    ctx = {}
    return render(request, 'education/first_page_after_login.html', ctx)

def edu_new(request):
    if request.method == "POST":
        form = SecondaryEducationForm(request.POST)
        if form.is_valid():
            Education = form.save(commit=False)
            Education.userID = request.user
            Education.created_date = timezone.now()
            Education.save()
    else:
        form= SecondaryEducationForm()
    return render(request, 'education/edu_edit.html', {'form': form, })


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
    return render(request, 'education/edu_edit2.html', {'form': form, })

