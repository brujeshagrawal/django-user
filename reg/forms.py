from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("email",)

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(ProfileForm, self).__init__(*args, **kwargs)
       for field in self.fields:
           self.fields[field].widget.attrs['readonly'] = True
    class Meta:
        model = get_user_model()
        fields = ('profile_pic','first_name','last_name','email','mobile_number','gender','dob')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name','mobile_number','gender','dob')
        labels = {'first_name':'First Name', 'last_name':'Last Name', 'mobile_number':'Mobile Number', 'gender':'Gender', 'dob':'Date of Birth'}
        help_texts = {'mobile_number':'Indian Number. Include +91-', 'dob':'mm/dd/YYYY'}
        GENDER_CHOICES = (
            ('','--select--'),
            ('M', 'Male'),
            ('F', 'Female'),
        )
        widgets = {
            'gender' : forms.Select(choices = GENDER_CHOICES),
        }

class ProfilePicForm(forms.Form):
    image_file = forms.ImageField()
