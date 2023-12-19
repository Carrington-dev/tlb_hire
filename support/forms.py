from django.forms import ModelForm

from support.models import Contact


class ContactForm(ModelForm):
    """Conatct definition."""

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message', )

