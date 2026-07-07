import json

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model, QuerySet
from django.forms.models import model_to_dict
from django.utils.html import format_html
from django.utils import timezone

from .views import test_chatbot_provider

from .models import (
    ActivityLog,
    AdminActionSnapshot,
    Article,
    Category,
    ChatbotConfig,
    ChatbotFAQ,
    CompletedProject,
    ContactMessage,
    Donation,
    DonationSettings,
    FAQ,
    GalleryItem,
    InKindDonation,
    ManagerNotification,
    NewsletterSubscriber,
    Partner,
    ProvinceOffice,
    Project,
    SiteConfig,
    SiteFlyer,
    Statistic,
    TeamMember,
    UserProfile,
    VolunteerApplication,
)


def is_manager(user):
    return user.is_authenticated and (
        user.groups.filter(name="Gerente").exists()
        or getattr(getattr(user, "profile", None), "role", "") == "gerente"
    )


def make_json_safe(value):
    if isinstance(value, Model):
        return {"id": value.pk, "label": str(value)}
    if isinstance(value, QuerySet):
        return [make_json_safe(item) for item in value]
    if isinstance(value, (list, tuple, set)):
        return [make_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): make_json_safe(item) for key, item in value.items()}
    if hasattr(value, "name") and not isinstance(value, str):
        return value.name
    return value


def serialize_instance(obj):
    data = model_to_dict(obj)
    return json.loads(json.dumps(make_json_safe(data), cls=DjangoJSONEncoder))


class TrackedAdminMixin:
    def save_model(self, request, obj, form, change):
        before_data = None
        if change and obj.pk:
            try:
                before_data = serialize_instance(obj.__class__.objects.get(pk=obj.pk))
            except obj.__class__.DoesNotExist:
                before_data = None
        super().save_model(request, obj, form, change)
        if is_manager(request.user):
            action = "change" if change else "add"
            snapshot = AdminActionSnapshot.objects.create(
                gerente=request.user,
                content_type=ContentType.objects.get_for_model(obj.__class__),
                object_id=str(obj.pk),
                object_label=str(obj),
                action=action,
                before_data=before_data,
                after_data=serialize_instance(obj),
            )
            ManagerNotification.objects.create(
                gerente=request.user,
                acao=snapshot.get_action_display(),
                modelo=obj._meta.verbose_name,
                objeto=str(obj),
                detalhe=f"Acao registada no historico reversivel #{snapshot.pk}.",
            )

    def delete_model(self, request, obj):
        before_data = serialize_instance(obj)
        label = str(obj)
        content_type = ContentType.objects.get_for_model(obj.__class__)
        object_id = str(obj.pk)
        super().delete_model(request, obj)
        if is_manager(request.user):
            snapshot = AdminActionSnapshot.objects.create(
                gerente=request.user,
                content_type=content_type,
                object_id=object_id,
                object_label=label,
                action="delete",
                before_data=before_data,
            )
            ManagerNotification.objects.create(
                gerente=request.user,
                acao=snapshot.get_action_display(),
                modelo=content_type.model_class()._meta.verbose_name,
                objeto=label,
                detalhe=f"Acao registada no historico reversivel #{snapshot.pk}.",
            )


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    fields = ("role", "foto", "telefone", "bloqueado_observacao")


@admin.register(UserProfile)
class UserProfileAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("user", "role", "telefone", "atualizado_em")
    list_filter = ("role",)
    search_fields = ("user__username", "user__first_name", "telefone")


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(TrackedAdminMixin, DjangoUserAdmin):
    inlines = [UserProfileInline]
    list_display = ("username", "first_name", "email", "is_staff", "is_active", "get_role")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "profile__role")
    actions = ("bloquear_usuarios", "desbloquear_usuarios")

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return super().get_inline_instances(request, obj)

    @admin.display(description="Funcao")
    def get_role(self, obj):
        return getattr(getattr(obj, "profile", None), "get_role_display", lambda: "")()

    @admin.action(description="Bloquear selecionados")
    def bloquear_usuarios(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} utilizador(es) bloqueado(s).", messages.WARNING)

    @admin.action(description="Desbloquear selecionados")
    def desbloquear_usuarios(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} utilizador(es) desbloqueado(s).", messages.SUCCESS)


@admin.register(SiteConfig)
class SiteConfigAdmin(TrackedAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ("Identidade", {"fields": ("nome", "slogan", "logo", "imagem_sobre")}),
        ("Hero", {"fields": ("hero_titulo", "hero_subtitulo")}),
        ("Institucional", {"fields": ("missao", "visao", "valores")}),
        ("Secao: Os Nossos Valores", {"fields": ("titulo_valores", "texto_valores", "valores_lista")}),
        ("Secao: Porque Ser Voluntario", {"fields": ("titulo_voluntariado", "texto_voluntariado")}),
        ("Secao: Os Nossos Parceiros", {"fields": ("titulo_parceiros", "texto_parceiros")}),
        ("Contactos", {"fields": ("telefone", "email", "endereco", "whatsapp")}),
        ("Redes sociais", {"fields": ("facebook", "instagram", "youtube", "linkedin")}),
    )


@admin.register(Category)
class CategoryAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("nome", "tipo", "slug")
    list_filter = ("tipo",)
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Project)
class ProjectAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("titulo", "categoria", "estado", "beneficiarios", "progresso", "destaque", "publicado")
    list_filter = ("estado", "destaque", "publicado", "categoria")
    search_fields = ("titulo", "descricao", "localizacao")
    prepopulated_fields = {"slug": ("titulo",)}
    fieldsets = (
        ("1. Identificacao", {"fields": ("titulo", "slug", "categoria", "imagem"), "description": "Preencha o nome do projeto, escolha a categoria e coloque uma foto quando existir."}),
        ("2. Conteudo", {"fields": ("descricao", "objetivos"), "description": "Escreva o resumo e os objetivos em linguagem simples para aparecer no site."}),
        ("3. Estado do projeto", {"fields": ("estado", "progresso", "beneficiarios", "localizacao", "data_inicio", "data_conclusao")}),
        ("4. Publicacao", {"fields": ("destaque", "publicado"), "description": "Marque publicado para aparecer no site. Marque destaque para aparecer com mais prioridade."}),
    )


@admin.register(CompletedProject)
class CompletedProjectAdmin(ProjectAdmin):
    list_display = ("titulo", "categoria", "data_conclusao", "beneficiarios", "destaque", "publicado")
    list_filter = ("destaque", "publicado", "categoria", "data_conclusao")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(estado="concluido")

    def save_model(self, request, obj, form, change):
        obj.estado = "concluido"
        obj.progresso = 100
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("titulo", "tipo", "categoria", "data_publicacao", "destaque", "publicado")
    list_filter = ("tipo", "categoria", "destaque", "publicado")
    search_fields = ("titulo", "resumo", "conteudo")
    prepopulated_fields = {"slug": ("titulo",)}
    fieldsets = (
        ("1. Tipo e titulo", {"fields": ("tipo", "titulo", "slug", "categoria"), "description": "Escolha Noticia ou Evento. Os eventos aparecem em Proximos Eventos."}),
        ("2. Texto e foto", {"fields": ("resumo", "conteudo", "imagem"), "description": "Coloque um resumo curto e uma foto para deixar o site mais profissional."}),
        ("3. Data e publicacao", {"fields": ("data_publicacao", "destaque", "publicado"), "description": "A data e usada para ordenar noticias e eventos no site."}),
    )


@admin.register(GalleryItem)
class GalleryItemAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("titulo", "tipo", "categoria", "destaque", "publicado")
    list_filter = ("tipo", "categoria", "destaque", "publicado")
    search_fields = ("titulo", "legenda")
    fieldsets = (
        ("1. Escolha o tipo", {"fields": ("tipo", "categoria", "titulo", "legenda"), "description": "Use Imagem para fotos da Galeria. Use Video ou YouTube para a secao Videos."}),
        ("2. Ficheiro ou link", {"fields": ("imagem", "video", "youtube_url"), "description": "Preencha apenas o campo que corresponde ao tipo escolhido."}),
        ("3. Publicacao", {"fields": ("destaque", "publicado"), "description": "Publicado aparece no site. Destaque fica com prioridade."}),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("nome", "cargo", "ordem", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome", "cargo")
    fieldsets = (
        ("1. Dados da pessoa", {"fields": ("nome", "cargo", "foto"), "description": "Coloque nome, cargo e foto da pessoa que vai aparecer em A Nossa Equipa."}),
        ("2. Texto e ordem", {"fields": ("biografia", "ordem", "ativo"), "description": "Use a ordem para controlar quem aparece primeiro. Desmarque ativo para esconder sem apagar."}),
    )


@admin.register(SiteFlyer)
class SiteFlyerAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("titulo", "posicao", "ordem", "ativo", "atualizado_em")
    list_filter = ("posicao", "ativo")
    search_fields = ("titulo", "subtitulo")
    fieldsets = (
        ("1. Texto do flyer", {"fields": ("titulo", "subtitulo"), "description": "Use texto curto. O flyer deve chamar atencao sem ficar carregado."}),
        ("2. Imagem e local", {"fields": ("imagem", "posicao", "ordem", "ativo"), "description": "Escolha onde o flyer aparece e envie uma imagem de boa qualidade."}),
        ("3. Botao opcional", {"fields": ("link_texto", "link_url"), "description": "Pode deixar vazio. Use links internos como #doacoes apenas quando necessario."}),
    )


@admin.register(Partner)
class PartnerAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("nome", "logo_preview", "website", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome",)
    readonly_fields = ("logo_preview",)
    fieldsets = (
        ("1. Dados do parceiro", {"fields": ("nome", "logo", "logo_preview"), "description": "Coloque o nome oficial e o logotipo do parceiro. O logotipo aparece no site."}),
        ("2. Link e publicacao", {"fields": ("website", "ativo"), "description": "Coloque o link completo, por exemplo https://exemplo.com. Marque ativo para aparecer no site."}),
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj and obj.logo:
            return format_html('<img src="{}" style="height:42px;max-width:90px;object-fit:contain;" />', obj.logo.url)
        return "Sem logo"


@admin.register(ProvinceOffice)
class ProvinceOfficeAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("provincia", "municipio", "telefone", "email", "ativo", "ordem")
    list_filter = ("ativo", "provincia")
    search_fields = ("provincia", "municipio", "endereco", "telefone", "email")


@admin.register(Statistic)
class StatisticAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("titulo", "valor", "sufixo", "icone", "ordem", "ativo")
    list_filter = ("ativo",)


@admin.register(FAQ)
class FAQAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("pergunta", "categoria", "ordem", "ativo")
    list_filter = ("categoria", "ativo")
    search_fields = ("pergunta", "resposta")


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "area_interesse", "estado", "criado_em")
    list_filter = ("estado", "area_interesse")
    search_fields = ("nome", "telefone", "email", "area_interesse")


@admin.register(Donation)
class DonationAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "valor", "tipo", "estado", "referencia", "criado_em")
    list_filter = ("tipo", "estado")
    search_fields = ("nome", "telefone", "email", "referencia")


@admin.register(InKindDonation)
class InKindDonationAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("nome", "telefone", "tipo_item", "quantidade", "estado_item", "estado", "familia_ou_projeto", "criado_em")
    list_filter = ("estado", "estado_item", "tipo_item")
    search_fields = ("nome", "telefone", "email", "tipo_item", "localizacao_entrega", "familia_ou_projeto")
    actions = ("aprovar", "rejeitar", "marcar_recebida", "marcar_distribuida")
    fieldsets = (
        ("1. Doador", {"fields": ("nome", "email", "telefone", "localizacao_entrega"), "description": "Dados para contactar e combinar a entrega."}),
        ("2. Item doado", {"fields": ("tipo_item", "quantidade", "estado_item", "descricao", "foto"), "description": "Confira se o item pode ser aceite pela ACSOL."}),
        ("3. Gestao interna", {"fields": ("estado", "familia_ou_projeto", "observacao_admin"), "description": "Use estes campos para aprovar, marcar como recebida e indicar a familia/projeto beneficiado."}),
    )

    @admin.action(description="Aprovar doacoes selecionadas")
    def aprovar(self, request, queryset):
        self.message_user(request, f"{queryset.update(estado='aprovada')} doacao(oes) aprovada(s).", messages.SUCCESS)

    @admin.action(description="Rejeitar doacoes selecionadas")
    def rejeitar(self, request, queryset):
        self.message_user(request, f"{queryset.update(estado='rejeitada')} doacao(oes) rejeitada(s).", messages.WARNING)

    @admin.action(description="Marcar como recebida")
    def marcar_recebida(self, request, queryset):
        self.message_user(request, f"{queryset.update(estado='recebida')} doacao(oes) marcada(s) como recebida(s).", messages.SUCCESS)

    @admin.action(description="Marcar como distribuida")
    def marcar_distribuida(self, request, queryset):
        self.message_user(request, f"{queryset.update(estado='distribuida')} doacao(oes) marcada(s) como distribuida(s).", messages.SUCCESS)


@admin.register(DonationSettings)
class DonationSettingsAdmin(TrackedAdminMixin, admin.ModelAdmin):
    change_form_template = "admin/core_help_change_form.html"
    list_display = ("titulo", "doacoes_monetarias_ativas", "contacto_doacoes", "telefone_doacoes", "atualizado_em")
    actions = ("ativar_quero_doar", "desativar_quero_doar")
    fieldsets = (
        ("Estado do Quero Doar", {"fields": ("doacoes_monetarias_ativas", "mensagem_doacoes_indisponiveis"), "description": "Mantenha desligado enquanto os dados bancarios oficiais nao estiverem confirmados."}),
        ("Texto publico", {"fields": ("titulo", "texto_publico", "contacto_doacoes", "telefone_doacoes"), "description": "Texto que explica como as pessoas podem ajudar."}),
        ("Instrucoes privadas", {"fields": ("instrucoes_nacionais", "instrucoes_internacionais", "instrucoes_multicaixa", "instrucoes_gateway", "instrucoes_especie", "gateway_url"), "description": "Estas instrucoes aparecem depois que a pessoa escolhe o tipo de doacao."}),
        ("Visibilidade", {"fields": ("mostrar_dados_bancarios_publicamente",)}),
    )

    @admin.action(description="Ativar Quero Doar")
    def ativar_quero_doar(self, request, queryset):
        updated = queryset.update(doacoes_monetarias_ativas=True)
        self.message_user(request, f"{updated} configuracao(oes) com Quero Doar ativado.", messages.SUCCESS)

    @admin.action(description="Desativar Quero Doar")
    def desativar_quero_doar(self, request, queryset):
        updated = queryset.update(doacoes_monetarias_ativas=False)
        self.message_user(request, f"{updated} configuracao(oes) com Quero Doar desativado.", messages.WARNING)


@admin.register(ContactMessage)
class ContactMessageAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("nome", "email", "assunto", "lida", "criado_em")
    list_filter = ("lida",)
    search_fields = ("nome", "email", "assunto", "mensagem")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("email", "ativo", "criado_em")
    list_filter = ("ativo",)
    search_fields = ("email",)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("usuario", "acao", "criado_em")
    search_fields = ("acao", "detalhe", "usuario__username")


class ChatbotFAQInline(admin.TabularInline):
    model = ChatbotFAQ
    extra = 1
    fields = ("pergunta", "resposta", "ordem", "ativo")


@admin.register(ChatbotConfig)
class ChatbotConfigAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("nome", "provider", "modelo", "modo", "voz_ativa", "ativo", "atualizado_em")
    list_filter = ("provider", "modo", "voz_ativa", "ativo")
    inlines = [ChatbotFAQInline]
    actions = ("testar_api",)
    fieldsets = (
        ("Estado", {"fields": ("nome", "ativo")}),
        ("API ou modo gratis", {"fields": ("provider", "api_key", "api_url", "modelo"), "description": "Use Respostas programadas para hospedar gratis sem depender de Llama, OpenAI ou Gemini."}),
        ("Restricao e voz", {"fields": ("modo", "assuntos_permitidos", "voz_ativa", "idioma_voz")}),
        ("Mensagens", {"fields": ("mensagem_inicial", "prompt_sistema", "resposta_padrao")}),
    )

    @admin.action(description="Testar API selecionada")
    def testar_api(self, request, queryset):
        for config in queryset:
            ok, result = test_chatbot_provider(config, "Responde apenas: teste ACSOL.")
            level = messages.SUCCESS if ok else messages.ERROR
            self.message_user(request, f"{config.nome}: {result}", level=level)


@admin.register(ChatbotFAQ)
class ChatbotFAQAdmin(TrackedAdminMixin, admin.ModelAdmin):
    list_display = ("pergunta", "config", "ordem", "ativo")
    list_filter = ("config", "ativo")
    search_fields = ("pergunta", "resposta")


@admin.register(ManagerNotification)
class ManagerNotificationAdmin(admin.ModelAdmin):
    list_display = ("gerente", "acao", "modelo", "objeto", "lida", "criado_em")
    list_filter = ("lida", "modelo", "gerente")
    search_fields = ("acao", "modelo", "objeto", "detalhe", "gerente__username")
    readonly_fields = ("gerente", "acao", "modelo", "objeto", "detalhe", "criado_em", "atualizado_em")
    actions = ("marcar_como_lida",)

    @admin.action(description="Marcar como lida")
    def marcar_como_lida(self, request, queryset):
        updated = queryset.update(lida=True)
        self.message_user(request, f"{updated} notificacao(oes) marcada(s) como lida(s).")


@admin.register(AdminActionSnapshot)
class AdminActionSnapshotAdmin(admin.ModelAdmin):
    list_display = ("gerente", "action", "content_type", "object_label", "reverted", "criado_em")
    list_filter = ("action", "reverted", "content_type", "gerente")
    search_fields = ("object_label", "object_id", "gerente__username")
    readonly_fields = (
        "gerente",
        "content_type",
        "object_id",
        "object_label",
        "action",
        "before_data",
        "after_data",
        "reverted",
        "reverted_by",
        "reverted_at",
        "criado_em",
        "atualizado_em",
    )
    actions = ("reverter_acoes",)

    @admin.action(description="Reverter acao selecionada")
    def reverter_acoes(self, request, queryset):
        total = 0
        for snapshot in queryset.filter(reverted=False):
            model = snapshot.content_type.model_class()
            if not model:
                continue
            if snapshot.action == "add":
                model.objects.filter(pk=snapshot.object_id).delete()
            elif snapshot.action in {"change", "delete"} and snapshot.before_data:
                obj, _ = model.objects.get_or_create(pk=snapshot.object_id)
                for field, value in snapshot.before_data.items():
                    if field == "id":
                        continue
                    try:
                        setattr(obj, field, value)
                    except Exception:
                        continue
                obj.save()
            snapshot.reverted = True
            snapshot.reverted_by = request.user
            snapshot.reverted_at = timezone.now()
            snapshot.save()
            total += 1
        self.message_user(request, f"{total} acao(oes) revertida(s).", messages.SUCCESS)


admin.site.site_header = "ACSOL Angola - Painel de Gestao"
admin.site.site_title = "ACSOL Admin"
admin.site.index_title = "Gestao institucional"
admin.site.index_template = "admin/index.html"
