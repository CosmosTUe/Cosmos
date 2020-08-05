from django import forms


CONTACTS = [
    ("cosmos@tue.nl", "Board/General information"),
    ("chair.cosmos@tue.nl", "Chairperson"),
    ("secretary.cosmos@tue.nl", "Secretary"),
    ("treasurer.cosmos@tue.nl", "Treasurer/Invoices"),
    ("internal.cosmos@tue.nl", "Internal Affairs/Questions"),
    ("external.cosmos.tue.nl", "External Affairs/Companies"),
]


class ContactForm(forms.Form):
    from_name = forms.CharField(label="Name", required=True, max_length=64)
    from_email = forms.EmailField(label="Email", required=True)
    recipient = forms.ChoiceField(required=True, choices=CONTACTS)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
