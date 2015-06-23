from django.forms import forms, CharField, DateField, EmailField, ImageField


class EditProfileForm(forms.Form):
    firstname = CharField()
    lastname = CharField()
    birthdate = DateField()
    bio = CharField()
    email = EmailField()
    jabber = CharField()
    skype = CharField()
    contacts = CharField()
    photo = ImageField()
