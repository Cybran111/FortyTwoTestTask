from django.forms import forms, CharField, DateField, \
    EmailField, ImageField, Textarea


class EditProfileForm(forms.Form):
    first_name = CharField()
    last_name = CharField()
    birth_date = DateField()
    bio = CharField(widget=Textarea)
    email = EmailField()
    jabber = CharField()
    skype = CharField()
    contacts = CharField(widget=Textarea)
    photo = ImageField()
