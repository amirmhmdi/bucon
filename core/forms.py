from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    # Honeypot field — real visitors never fill this in; bots often do.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
