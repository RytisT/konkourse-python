from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.db.models import FileField
from documents import magic


class RestrictedFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size")
        self.content_types = kwargs.pop("content_types")
        super(RestrictedFileField, self).__init__(*args, **kwargs)


    def clean(self, *args, **kwargs):
        file = super(RestrictedFileField, self).clean(*args, **kwargs)
        content_type = file.content_type
        mimetype = magic.from_buffer(file.read(1024), mime=True)
        if mimetype in self.content_types:
            if file._size > self.max_upload_size:
                raise forms.ValidationError(_('File is larger then allowed filesize'))
        else:
            raise forms.ValidationError(_('File type is not supported'))

        return file
