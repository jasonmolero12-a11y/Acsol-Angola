from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("voluntariado/candidatura/", views.volunteer_application, name="volunteer_application"),
    path("doacoes/interesse/", views.donation_interest, name="donation_interest"),
    path("doacoes/especie/", views.in_kind_donation, name="in_kind_donation"),
    path("doacoes/instrucoes/", views.donation_instructions, name="donation_instructions"),
    path("contacto/", views.contact_message, name="contact_message"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("chatbot/mensagem/", views.chatbot_message, name="chatbot_message"),
]
