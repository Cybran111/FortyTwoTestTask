from datetime import date
from django.forms import forms, CharField, DateField, \
    EmailField, ImageField, Textarea, ClearableFileInput


class PhotoInput(ClearableFileInput):
    template_with_initial = u'%(initial)s %(clear_template)s' \
                            u'<br />%(input_text)s: %(input)s'
    url_markup_template = u'<img src="{0}" alt="{1}" class="img-thumbnail"/>'


class EditProfileForm(forms.Form):
    first_name = CharField()
    last_name = CharField()
    birth_date = DateField()
    bio = CharField(widget=Textarea)
    email = EmailField()
    jabber = CharField()
    skype = CharField()
    contacts = CharField(widget=Textarea)
    photo = ImageField(widget=PhotoInput)

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']

        if not date(1900, 1, 1) < birth_date < date.today():
            raise forms.ValidationError(
                "Enter a date between 1900 year and today's day.")

        return birth_date
