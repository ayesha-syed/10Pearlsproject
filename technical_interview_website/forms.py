from django import forms
from .models import *
class Video_form(forms.ModelForm):
    class Meta:
        model=Interview
        fields=('interview_video',)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields=('feedback',)
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['feedback'].widget.attrs.update({'class': 'form-style','placeholder':"Your Feedback"})

class candidate_login_form(forms.ModelForm):
    class Meta:
        model=Candidate
        fields=('username','password',)
        widgets = {
            "password": forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password'})
        }
    def __init__(self, *args, **kwargs):
        super(candidate_login_form, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-style','placeholder':"Your Username"})
        self.fields['password'].widget.attrs.update({'class': 'form-style','placeholder':"Your Password"})

class admin_login_form(forms.ModelForm):
    class Meta:
        model=Admin
        fields=('email','password',)
        widgets = {
            "password": forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password'})
        }
    def __init__(self, *args, **kwargs):
        super(admin_login_form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-style','placeholder':"Your Email"})
        self.fields['password'].widget.attrs.update({'class': 'form-style','placeholder':"Your Password"})

class admin_signup_form(forms.ModelForm):
    class Meta:
        model=Admin
        fields='__all__'
        widgets = {
            "password": forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password'})
        }
    def __init__(self, *args, **kwargs):
            super(admin_signup_form, self).__init__(*args, **kwargs)
            self.fields['first_Name'].widget.attrs.update({'class': 'form-style','placeholder':"Your First Name"})
            self.fields['last_Name'].widget.attrs.update({'class': 'form-style','placeholder':"Your Last Name"})
            self.fields['email'].widget.attrs.update({'class': 'form-style','placeholder':"Your Email"})
            self.fields['password'].widget.attrs.update({'class': 'form-style','placeholder':"Your Password"})

class admin_editprofile_form(forms.ModelForm):
    class Meta:
        model=Admin
        fields='__all__'
        # confirm_password=forms.CharField(widget=forms.PasswordInput())
        # widgets = {
        #     "password": forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password'})
        # }
        widgets={
        'password':forms.TextInput(attrs={'type':'password','data-toggle': 'password','autocomplete': 'off'})
    }
    def __init__(self, *args, **kwargs):
            super(admin_editprofile_form, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['first_Name'].widget.attrs.update({'class': 'form-style','placeholder':"Your First Name"})
            self.fields['last_Name'].widget.attrs.update({'class': 'form-style','placeholder':"Your Last Name"})
            self.fields['email'].widget.attrs.update({'class': 'form-style','placeholder':"Your Email"})
            self.fields['password'].widget.attrs.update({'class': 'form-style','placeholder':"Your Password"}) 

class complete_candidate_form(forms.ModelForm):
    class Meta:
        model=Candidate
        fields='__all__'
        # widgets = {
        #     "password": forms.PasswordInput(attrs={'autocomplete': 'off','data-toggle': 'password'})
        # }
        widgets={
        'password':forms.TextInput(attrs={'type':'password','data-toggle': 'password','autocomplete': 'off'})
    }
    def __init__(self, *args, **kwargs):
        super(complete_candidate_form, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['Position'].disabled = True
        self.fields['first_Name'].widget.attrs.update({'class': 'form-style','placeholder':"Your First Name"})
        self.fields['last_Name'].widget.attrs.update({'class': 'form-style','placeholder':"Your Last Name"})
        self.fields['username'].widget.attrs.update({'class': 'form-style','placeholder':"Your Username"})
        self.fields['email'].widget.attrs.update({'class': 'form-style','placeholder':"Your Email"})
        self.fields['password'].widget.attrs.update({'class': 'form-style ','placeholder':"Your Password"})
        self.fields['Position'].widget.attrs.update({'class': 'form-style','placeholder':"Your Position"})

class candidate_signup_form(forms.ModelForm):
    class Meta:
        model=Candidate
        fields=('username','email','password','Position')
        widgets = {
            "password": forms.PasswordInput(attrs={'placeholder':'Password','autocomplete': 'off','data-toggle': 'password'})
        }
    def __init__(self, *args, **kwargs):
        super(candidate_signup_form, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-style','placeholder':"Username"})
        self.fields['email'].widget.attrs.update({'class': 'form-style','placeholder':"Email"})
        self.fields['password'].widget.attrs.update({'class': 'form-style'})
        self.fields['Position'].widget.attrs.update({'class': 'form-style','placeholder':"Position"})


class create_questionnaire_form(forms.ModelForm):
    class Meta:
        model=Questionnaire
        fields=('Questionnaire_name',)
    def __init__(self, *args, **kwargs):
        super(create_questionnaire_form, self).__init__(*args, **kwargs)
        self.fields['Questionnaire_name'].widget.attrs.update({'class': 'form-style','placeholder':"Questionnaire Name"})


class add_questions_form(forms.ModelForm):
    class Meta:
        model=ActualQuestion
        fields=('Actual_Question',)
    def __init__(self, *args, **kwargs):
        super(add_questions_form, self).__init__(*args, **kwargs)
        self.fields['Actual_Question'].widget.attrs.update({'class': 'form-style','placeholder':"Enter a question"})
        self.fields['Actual_Question'].help_text=None
        self.fields['Actual_Question'].label=None

class create_interview_form(forms.ModelForm):
    class Meta:
        model=Interview
        fields=('candidate_id','interview_deadline','interview_email','Questionnaire')

class formm(forms.Form):
    candidate_name=forms.CharField(max_length=40)
    Questionnaire_name=forms.CharField(max_length=50)
    email=forms.CharField(max_length=40)
    deadline=forms.DateField()
 
    # def __init__(self, *args, **kwargs):
    #     super(create_interview_form, self).__init__(*args, **kwargs)
    #     # self.fields['candidate_id'].widget.attrs.update({'class': 'form-style','placeholder':"Candidate Email"})
    #     # self.fields['admin_id'].widget.attrs.update({'class': 'form-style','placeholder':"Admin Email"})
    #     # self.fields['Questionnaire'].widget.attrs.update({'class': 'form-style','placeholder':"Questionnaire Set"})
    #     self.fields['interview_deadline'].widget=forms.widgets.DateInput(attrs={'type': 'date'})
