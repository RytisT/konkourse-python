from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from account.models import UserProfile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import extras

class AccountInitialForm(forms.ModelForm):
    password_repeat = forms.CharField(widget=forms.PasswordInput(render_value=False,
        attrs={'style':"width:94%; margin-top:4px; margin-bottom:4px;",
        'placeholder':"Re-enter Password"}))

    def save(self, commit=True):
        user = super(AccountInitialForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'style':"width:94%; margin-top:4px; margin-bottom:4px;",'class':"", 'placeholder':"First Name"}),
            'last_name': forms.TextInput(attrs={'style':"width:94%; margin-top:4px; margin-bottom:4px;", 'placeholder':"Last Name"}),
            'email': forms.TextInput(attrs={'style':"width:94%; margin-top:4px; margin-bottom:4px;", 'placeholder':"Email"}),
            'username': forms.TextInput(attrs={'style':"width:94%; margin-top:4px; margin-bottom:4px;", 'placeholder':"Username"}),
            'password': forms.PasswordInput(render_value=False, attrs={'style':"width:94%; margin-top:4px; margin-bottom:4px;", 'placeholder':"Password"})
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == '':
            raise forms.ValidationError("Invalid email address.")
        try:
            User.objects.get(email=email)
        except:
            parts = email.split('@')
            valid_emails = ('vt.edu', 'dukes.jmu.edu', 'jmu.edu', 'virginia.edu', 'konkourse.com')
            if parts[1] not in valid_emails:
                raise forms.ValidationError("Email address not permitted.")
            else:
                return email
        raise forms.ValidationError("Email already exists")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except:
            return username
        return forms.ValidationError('Username has been taken')

    def clean_password_repeat(self):
        password = self.cleaned_data['password']
        data = self.cleaned_data
        password_repeat = self.cleaned_data['password_repeat']
        if password == password_repeat:
            return password
        else:
            raise forms.ValidationError("Passwords do not match")

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name =='':
            raise forms.ValidationError('Please input a first name.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name == '':
            raise forms.ValidationError('Please input a last name.')
        return last_name


class AccountForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'major', 'tagline', 'phone_number', 'about', 'interests', 'sex', 'birthday')
        widgets = {
            'major': forms.TextInput(attrs={'class':"input-xlarge span5", 'placeholder':"Type your Major"}),
            'tagline': forms.TextInput(attrs={'class':"input-xlarge span5", 'placeholder':"Type your tagline"}),
            'phone_number': forms.TextInput(attrs={'placeholder':"Optional"}),
            'about': forms.Textarea(attrs={'class':"input-xlarge span5", 'rows':"5", 'placeholder':"Type something about yourself."}),
            'interests': forms.Textarea(attrs={'class':"input-xlarge span5", 'rows':"5", 'placeholder':"What interests you?"}),
            'birthday': forms.TextInput(attrs={'class':"span3", 'date-date-format':"yyyy-mm-dd", 'style':"float:left",
                "placeholder":"Date", "id":"id_birthday"}),
        }

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'style':"vertical-align:top;"}))


    def clean_image(self):
        image = self.cleaned_data['image']
        if image is not None:

            if isinstance(image, InMemoryUploadedFile) and image._size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size is too big.")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return image

class AccountNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'placeholder':"Type Your First Name"}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'placeholder':"Type Your Last Name"}))

# model form for email preferences on settings page
class EmailPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('connection_request_email', 'endorsement_email', 'profile_post_email', 'course_post_email', 'new_course_member_email')

