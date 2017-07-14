from .models import Education
from .models import Company
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


#   FOR APPLICANT PROFILE
class SignUpForm(UserCreationForm):
    Options = (('0', 'Applicant'),
               ('1', 'Company'),)
    first_name = forms.ChoiceField(choices=Options, required=True, label="Type of User")
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2', )
        labels = {
            'first_name': 'Type of User',
        }


# For Company Profile
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        widgets = {'about': forms.Textarea(attrs={'size': 1000})}
        fields = ('name', 'about', 'website',)


CATEGORIES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )


class SecondaryEducationForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=CATEGORIES, required=True)
    dob = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    duration = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'in months'}))
    duration2 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'in months'}))

    class Meta:
        model = Education
        widgets = {'description_p': forms.Textarea(attrs={'size': 1000}), 'skills': forms.Textarea(attrs={'size': 1000})}
        fields = ('name', 'homeadd', 'dob', 'contact','gender', 'yoc1', 'board1', 'percentage1', 'yoc2', 'board2', 'percentage2',
                  'yoc3', 'percentage3','college','course',
                  'company_i', 'duration', 'profile_i', 'company_i2', 'duration2', 'profile_i2',
                  'title_p','description_p','skills', 'work', 'git_hub', 'linked_in',)


class SearchForm(forms.Form):
    search= forms.CharField(label="Search by post",max_length=250,widget=forms.TextInput(attrs={'placeholder': 'Enter the interns post required'}))
