from django import forms
from courses.models import Course
from django.core.files.uploadedfile import InMemoryUploadedFile


class CourseInitialForm(forms.Form):
    course_number = forms.CharField(max_length='10',
                                    widget=forms.TextInput(attrs={'placeholder': ''}))
    course_id = forms.CharField(max_length='10',
                                widget=forms.TextInput(attrs={'placeholder': ''}))


class CourseForm(forms.ModelForm):
    CREDIT_OPTIONS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    SEMESTER_OPTIONS = (
        ('S013', 'Spring 2013'),
        ('M113', 'Summer I 2013'),
        ('M213', 'Summer II 2013'),
        ('F013', 'Fall 2013'),
        ('S014', 'Spring 2014'),
    )
    time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']

    class Meta:
        model = Course

        exclude = ('tag',
                   'number',
                   'course_id',
                   'course_users',
                   'institution',
                   'events',
                   'wall')

    image = forms.ImageField(required=False, widget=forms.FileInput)
    name = forms.CharField(max_length=42,
                           required=False)
    name.widget.attrs['class'] = 'span4'
    professor = forms.CharField(max_length=52,
                                required=False)
    professor.widget.attrs['class'] = 'span4'
    semester = forms.ChoiceField(choices=SEMESTER_OPTIONS,
                                 required=False)
    semester.widget.attrs['class'] = 'span4'
    time = forms.TimeField(input_formats=time_formats,
                           required=False,
                           widget=forms.TimeInput(format='%I:%M %p'))
    time.widget.attrs['class'] = ''
    credits = forms.ChoiceField(choices=CREDIT_OPTIONS,
                                required=False)
    credits.widget.attrs['class'] = 'span4'
    about = forms.CharField(max_length=125, widget=forms.Textarea,
                            help_text='125 characters max, try something short and sweet.',
                            required=False)
    about.widget.attrs['class'] = 'span4'

    def clean_image(self):
        image = self.cleaned_data['image']
        if image is not None:
            if isinstance(image, InMemoryUploadedFile) and image._size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size is too big.")
        # Always return the cleaned data, whether you have changed it or
        # not.
        return image
