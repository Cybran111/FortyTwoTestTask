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
    jabber = EmailField(error_messages={"invalid": u"Enter a valid jabber address."})
    skype = CharField()
    contacts = CharField(widget=Textarea)
    photo = ImageField(widget=PhotoInput)