from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST
import json
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .forms import ContactMessageForm, DonationForm, InKindDonationForm, NewsletterSubscriberForm, VolunteerApplicationForm
from .models import Article, ChatbotConfig, DonationSettings, FAQ, GalleryItem, Partner, Project, ProvinceOffice, SiteConfig, SiteFlyer, Statistic, TeamMember


def home(request):
    site_config = SiteConfig.objects.first()
    valores_source = ""
    if site_config:
        valores_source = site_config.valores_lista or site_config.valores
    site_values = [
        value.strip(" -\t")
        for value in valores_source.splitlines()
        if value.strip(" -\t")
    ]

    context = {
        "site_config": site_config,
        "site_values": site_values,
        "stats": Statistic.objects.filter(ativo=True)[:8],
        "featured_projects": Project.objects.filter(publicado=True, destaque=True)[:6],
        "completed_projects": Project.objects.filter(publicado=True, estado="concluido")[:6],
        "recent_articles": Article.objects.filter(publicado=True)[:6],
        "news_items": Article.objects.filter(publicado=True, tipo="noticia")[:6],
        "event_items": Article.objects.filter(publicado=True, tipo="evento")[:6],
        "gallery_items": GalleryItem.objects.filter(publicado=True)[:18],
        "gallery_photos": GalleryItem.objects.filter(publicado=True, tipo="imagem")[:18],
        "gallery_videos": GalleryItem.objects.filter(publicado=True, tipo__in=["video", "youtube"])[:12],
        "home_flyers": SiteFlyer.objects.filter(ativo=True, posicao="home")[:3],
        "team_members": TeamMember.objects.filter(ativo=True)[:12],
        "province_offices": ProvinceOffice.objects.filter(ativo=True)[:12],
        "partners": Partner.objects.filter(ativo=True)[:12],
        "faqs": FAQ.objects.filter(ativo=True)[:20],
        "donation_settings": DonationSettings.objects.first(),
        "chatbot_config": ChatbotConfig.objects.filter(ativo=True).first(),
    }
    return render(request, "core/home.html", context)


@require_POST
def volunteer_application(request):
    form = VolunteerApplicationForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Candidatura enviada com sucesso.")
        return _ok(request, "Candidatura enviada com sucesso.")
    return _bad_request(request, form)


@require_POST
def contact_message(request):
    form = ContactMessageForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Mensagem enviada com sucesso.")
        return _ok(request, "Mensagem enviada com sucesso.")
    return _bad_request(request, form)


@require_POST
def donation_interest(request):
    settings = DonationSettings.objects.first()
    if not settings or not settings.doacoes_monetarias_ativas:
        message = _donations_unavailable_message(settings)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "message": message}, status=403)
        messages.warning(request, message)
        return redirect("core:home")

    form = DonationForm(request.POST, request.FILES)
    if form.is_valid():
        donation = form.save()
        instructions = _donation_instructions(settings, donation.tipo)
        return _ok(
            request,
            "Interesse de doacao registado. As instrucoes foram preparadas para este pedido.",
            {"instructions": instructions, "reference": f"ACSOL-DOA-{donation.pk:05d}"},
        )
    return _bad_request(request, form)


@require_POST
def in_kind_donation(request):
    form = InKindDonationForm(request.POST, request.FILES)
    if form.is_valid():
        donation = form.save()
        return _ok(
            request,
            "Doacao em especie registada. A equipa da ACSOL vai analisar e entrar em contacto.",
            {"reference": f"ACSOL-ESP-{donation.pk:05d}"},
        )
    return _bad_request(request, form)


@require_GET
def donation_instructions(request):
    donation_type = request.GET.get("tipo", "nacional")
    settings = DonationSettings.objects.first()
    if donation_type != "especie" and (not settings or not settings.doacoes_monetarias_ativas):
        return JsonResponse(
            {
                "ok": False,
                "available": False,
                "instructions": _donations_unavailable_message(settings),
            }
        )
    return JsonResponse({"ok": True, "instructions": _donation_instructions(settings, donation_type)})


@require_POST
def newsletter_subscribe(request):
    form = NewsletterSubscriberForm(request.POST)
    if form.is_valid():
        form.save()
        return _ok(request, "Subscricao realizada com sucesso.")
    return _bad_request(request, form)


@require_POST
def chatbot_message(request):
    question = request.POST.get("message", "").strip()
    if not question:
        return JsonResponse({"ok": False, "message": "Escreva uma pergunta."}, status=400)

    config = ChatbotConfig.objects.filter(ativo=True).first()
    if not config:
        return JsonResponse({"ok": True, "answer": "O chatbot ainda nao foi configurado no painel administrativo."})

    faq_answer = _faq_answer(config, question)
    if faq_answer:
        return JsonResponse({"ok": True, "answer": faq_answer, "voice": config.voz_ativa, "voice_lang": config.idioma_voz})

    if config.provider == "programado":
        return JsonResponse(
            {
                "ok": True,
                "answer": config.resposta_padrao,
                "voice": config.voz_ativa,
                "voice_lang": config.idioma_voz,
            }
        )

    if not config.api_key:
        return JsonResponse(
            {
                "ok": True,
                "answer": config.resposta_padrao,
                "voice": config.voz_ativa,
                "voice_lang": config.idioma_voz,
            }
        )

    try:
        answer = chatbot_completion(config, question)
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
        answer = "A API do chatbot esta temporariamente indisponivel. Tente novamente dentro de alguns instantes."

    return JsonResponse({"ok": True, "answer": answer, "voice": config.voz_ativa, "voice_lang": config.idioma_voz})


def _ok(request, message, extra=None):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        payload = {"ok": True, "message": message}
        if extra:
            payload.update(extra)
        return JsonResponse(payload)
    return redirect("core:home")


def _bad_request(request, form):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)
    messages.error(request, "Verifique os dados enviados.")
    return redirect("core:home")


def _donation_instructions(settings, donation_type):
    if not settings:
        return "A equipa da ACSOL entrara em contacto para enviar as instrucoes de pagamento."
    instructions_by_type = {
        "nacional": settings.instrucoes_nacionais,
        "internacional": settings.instrucoes_internacionais,
        "multicaixa": settings.instrucoes_multicaixa,
        "gateway": settings.instrucoes_gateway or settings.gateway_url,
        "especie": settings.instrucoes_especie,
    }
    instructions = instructions_by_type.get(donation_type, "").strip()
    if instructions:
        return instructions
    return f"Contacte a equipa de doacoes: {settings.contacto_doacoes} {settings.telefone_doacoes}".strip()


def _donations_unavailable_message(settings):
    if settings and settings.mensagem_doacoes_indisponiveis.strip():
        return settings.mensagem_doacoes_indisponiveis.strip()
    return (
        "A opcao Quero Doar esta temporariamente indisponivel enquanto a ACSOL confirma "
        "os dados bancarios oficiais."
    )


def _faq_answer(config, question):
    normalized = question.casefold()
    for faq in config.perguntas.filter(ativo=True):
        if faq.pergunta.casefold() in normalized or normalized in faq.pergunta.casefold():
            return faq.resposta
    return ""


def _system_prompt(config):
    if config.modo == "livre":
        return config.prompt_sistema
    return (
        f"{config.prompt_sistema}\n\n"
        f"Modo restrito ativo. Responde apenas sobre estes assuntos: {config.assuntos_permitidos}. "
        "Se a pergunta sair destes temas, explica de forma curta que o chatbot esta limitado aos temas da ACSOL e direitos humanos."
    )


def chatbot_completion(config, question):
    last_error = None
    for attempt in range(2):
        try:
            if config.provider == "gemini":
                return _gemini_completion(config, question)
            return _chat_completions_request(config, question)
        except HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 1:
                raise
            time.sleep(1)
        except (URLError, TimeoutError) as exc:
            last_error = exc
            if attempt == 1:
                raise
            time.sleep(1)
    raise last_error


def test_chatbot_provider(config, question):
    if config.provider == "programado":
        return True, "modo programado ativo; nao usa API paga."
    if not config.api_key:
        return False, "faltou preencher a chave da API."
    try:
        answer = chatbot_completion(config, question)
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
        return False, f"falhou ({exc}). Verifique chave, modelo e URL."
    return True, f"respondeu: {answer[:120]}"


def _chat_completions_request(config, question):
    payload = {
        "model": config.modelo,
        "messages": [
            {"role": "system", "content": _system_prompt(config)},
            {"role": "assistant", "content": config.mensagem_inicial},
            {"role": "user", "content": question},
        ],
        "temperature": 0.2,
    }
    request = Request(
        config.api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def _gemini_completion(config, question):
    endpoint = config.api_url
    if not endpoint or "generativelanguage.googleapis.com" not in endpoint:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{config.modelo}:generateContent?key={config.api_key}"
    elif ":generateContent" not in endpoint:
        endpoint = endpoint.rstrip("/")
        if endpoint.endswith("/models"):
            endpoint = f"{endpoint}/{config.modelo}:generateContent"
        elif f"/{config.modelo}" not in endpoint:
            endpoint = f"{endpoint}/models/{config.modelo}:generateContent"
        else:
            endpoint = f"{endpoint}:generateContent"
    separator = "&" if "?" in endpoint else "?"
    if "key=" not in endpoint:
        endpoint = f"{endpoint}{separator}key={config.api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{_system_prompt(config)}\n\nPergunta: {question}"},
                ]
            }
        ],
        "generationConfig": {"temperature": 0.2},
    }
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["candidates"][0]["content"]["parts"][0]["text"]
