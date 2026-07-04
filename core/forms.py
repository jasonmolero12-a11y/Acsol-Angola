from django import forms

from .models import ContactMessage, Donation, InKindDonation, NewsletterSubscriber, VolunteerApplication


class VolunteerApplicationForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ["nome", "telefone", "email", "morada", "profissao", "area_interesse", "curriculo", "mensagem"]


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["nome", "telefone", "email", "assunto", "mensagem"]


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ["nome", "telefone", "email", "valor", "tipo", "comprovativo", "observacao"]


class InKindDonationForm(forms.ModelForm):
    class Meta:
        model = InKindDonation
        fields = [
            "nome",
            "email",
            "telefone",
            "tipo_item",
            "quantidade",
            "estado_item",
            "descricao",
            "localizacao_entrega",
            "foto",
        ]


class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
