from django.forms import forms, CharField, DateField, \
    EmailField, ImageField, Textarea, ClearableFileInput


class PhotoInput(ClearableFileInput):
    template_with_initial = '%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    url_markup_template = '<img src="{0}" alt="{1}" class="img-thumbnail"/>'


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
