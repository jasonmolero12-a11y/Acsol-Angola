from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStampedModel):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("gerente", "Gerente"),
    ]
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="gerente")
    foto = models.ImageField(upload_to="perfis/", blank=True, null=True)
    telefone = models.CharField(max_length=60, blank=True)
    bloqueado_observacao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Perfil de utilizador"
        verbose_name_plural = "Perfis de utilizadores"

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ManagerNotification(TimeStampedModel):
    gerente = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=180)
    modelo = models.CharField(max_length=120, blank=True)
    objeto = models.CharField(max_length=180, blank=True)
    detalhe = models.TextField(blank=True)
    lida = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notificacao de gerente"
        verbose_name_plural = "Notificacoes de gerentes"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.gerente} - {self.acao}"


class AdminActionSnapshot(TimeStampedModel):
    ACTION_CHOICES = [
        ("add", "Criacao"),
        ("change", "Alteracao"),
        ("delete", "Eliminacao"),
    ]
    gerente = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.ForeignKey("contenttypes.ContentType", on_delete=models.CASCADE)
    object_id = models.CharField(max_length=80, blank=True)
    object_label = models.CharField(max_length=180, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    before_data = models.JSONField(blank=True, null=True)
    after_data = models.JSONField(blank=True, null=True)
    reverted = models.BooleanField(default=False)
    reverted_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="reverted_snapshots")
    reverted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Historico reversivel"
        verbose_name_plural = "Historico reversivel"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.get_action_display()} - {self.object_label}"


class SiteConfig(TimeStampedModel):
    nome = models.CharField(max_length=160, default="ACSOL - Acao de Solidariedade em Angola")
    slogan = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    imagem_sobre = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        verbose_name="Imagem da secao Quem Somos",
        help_text="Foto institucional usada na secao Quem Somos. Use uma imagem horizontal e bem enquadrada.",
    )
    hero_titulo = models.CharField(max_length=255, blank=True)
    hero_subtitulo = models.TextField(blank=True)
    missao = models.TextField(blank=True)
    visao = models.TextField(blank=True)
    valores = models.TextField(blank=True)
    titulo_valores = models.CharField(max_length=160, default="Os Nossos Valores")
    texto_valores = models.TextField(
        blank=True,
        default="",
        help_text="Texto introdutor opcional para a secao de valores.",
    )
    valores_lista = models.TextField(
        blank=True,
        default="Solidariedade\nIntegridade\nInclusao\nInovacao\nResponsabilidade\nSustentabilidade",
        help_text="Um valor por linha. Exemplo: Solidariedade",
    )
    titulo_voluntariado = models.CharField(max_length=160, default="Porque Ser Voluntario?")
    texto_voluntariado = models.TextField(
        blank=True,
        default="O voluntariado na ACSOL e uma experiencia transformadora. Contribui com as suas competencias, tempo e coracao para construir uma Angola melhor para todos.",
    )
    titulo_parceiros = models.CharField(max_length=160, default="Os Nossos Parceiros")
    texto_parceiros = models.TextField(
        blank=True,
        default="A ACSOL trabalha em parceria com organizacoes governamentais, internacionais e do setor privado para maximizar o impacto das suas intervencoes.",
    )
    telefone = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    whatsapp = models.CharField(max_length=60, blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    class Meta:
        verbose_name = "Configuracao do site"
        verbose_name_plural = "Configuracoes do site"

    def __str__(self):
        return self.nome

    @property
    def whatsapp_url(self):
        value = (self.whatsapp or "").strip()
        if not value:
            return ""
        if value.startswith(("http://", "https://")):
            return value
        digits = "".join(char for char in value if char.isdigit())
        if not digits:
            return ""
        return f"https://wa.me/{digits}"


class Category(TimeStampedModel):
    TIPO_CHOICES = [
        ("projeto", "Projeto"),
        ("noticia", "Noticia"),
        ("evento", "Evento"),
        ("galeria", "Galeria"),
        ("faq", "FAQ"),
    ]
    nome = models.CharField(max_length=120)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    slug = models.SlugField(max_length=140, blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        unique_together = ("tipo", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Project(TimeStampedModel):
    ESTADO_CHOICES = [
        ("planeado", "Planeado"),
        ("andamento", "Em andamento"),
        ("concluido", "Concluido"),
        ("suspenso", "Suspenso"),
    ]
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={"tipo": "projeto"})
    descricao = models.TextField()
    objetivos = models.TextField(blank=True)
    beneficiarios = models.PositiveIntegerField(default=0)
    localizacao = models.CharField(max_length=180, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="andamento")
    data_inicio = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    imagem = models.ImageField(upload_to="projetos/", blank=True, null=True)
    progresso = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    destaque = models.BooleanField(default=False)
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ["-destaque", "-criado_em"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class CompletedProject(Project):
    class Meta:
        proxy = True
        verbose_name = "Projeto feito"
        verbose_name_plural = "Projetos feitos"


class Article(TimeStampedModel):
    TIPO_CHOICES = [("noticia", "Noticia"), ("evento", "Evento")]
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="noticia")
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    resumo = models.TextField()
    conteudo = models.TextField(blank=True)
    imagem = models.ImageField(upload_to="noticias/", blank=True, null=True)
    data_publicacao = models.DateField(null=True, blank=True)
    destaque = models.BooleanField(default=False)
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Noticia ou evento"
        verbose_name_plural = "Noticias e eventos"
        ordering = ["-data_publicacao", "-criado_em"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class GalleryItem(TimeStampedModel):
    TIPO_CHOICES = [("imagem", "Imagem"), ("youtube", "YouTube"), ("video", "Video")]
    CATEGORIA_CHOICES = [
        ("projetos", "Projetos"),
        ("eventos", "Eventos"),
        ("voluntarios", "Voluntarios"),
        ("comunidades", "Comunidades"),
        ("outros", "Outros"),
    ]
    titulo = models.CharField(max_length=160)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="imagem")
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES, default="outros")
    imagem = models.ImageField(
        upload_to="galeria/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )
    video = models.FileField(
        upload_to="videos/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["mp4", "webm", "mov"])],
    )
    youtube_url = models.URLField(blank=True)
    legenda = models.CharField(max_length=255, blank=True)
    destaque = models.BooleanField(default=False)
    publicado = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Item da galeria"
        verbose_name_plural = "Galeria"
        ordering = ["-destaque", "-criado_em"]

    def __str__(self):
        return self.titulo

    @property
    def youtube_embed_url(self):
        if not self.youtube_url:
            return ""
        url = self.youtube_url
        if "youtu.be/" in url:
            video_id = url.rsplit("/", 1)[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if "watch?v=" in url:
            video_id = url.split("watch?v=", 1)[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if "/embed/" in url:
            return url
        return url


class TeamMember(TimeStampedModel):
    nome = models.CharField(max_length=140)
    cargo = models.CharField(max_length=140)
    biografia = models.TextField(blank=True)
    foto = models.ImageField(upload_to="equipa/", blank=True, null=True)
    ordem = models.PositiveSmallIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Membro da equipa"
        verbose_name_plural = "Equipa"
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome


class SiteFlyer(TimeStampedModel):
    POSICAO_CHOICES = [
        ("home", "Inicio"),
        ("doacoes", "Doacoes"),
        ("eventos", "Eventos"),
        ("galeria", "Galeria"),
    ]
    titulo = models.CharField(max_length=160)
    subtitulo = models.CharField(max_length=255, blank=True)
    imagem = models.ImageField(upload_to="flyers/", blank=True, null=True)
    posicao = models.CharField(max_length=30, choices=POSICAO_CHOICES, default="home")
    link_texto = models.CharField(max_length=80, blank=True)
    link_url = models.CharField(max_length=180, blank=True)
    ordem = models.PositiveSmallIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Flyer/banner"
        verbose_name_plural = "Flyers e banners"
        ordering = ["posicao", "ordem", "titulo"]

    def __str__(self):
        return self.titulo


class ProvinceOffice(TimeStampedModel):
    provincia = models.CharField(max_length=120)
    municipio = models.CharField(max_length=120, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    descricao = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ordem = models.PositiveSmallIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Divisao provincial"
        verbose_name_plural = "Divisoes provinciais"
        ordering = ["ordem", "provincia"]

    def __str__(self):
        return self.provincia

    @property
    def maps_url(self):
        if self.latitude is not None and self.longitude is not None:
            return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
        query = "+".join(filter(None, [self.endereco, self.municipio, self.provincia, "Angola"]))
        return f"https://www.google.com/maps/search/{query}"


class Partner(TimeStampedModel):
    nome = models.CharField(max_length=140)
    logo = models.ImageField(upload_to="parceiros/", blank=True, null=True)
    website = models.URLField(blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Parceiro"
        verbose_name_plural = "Parceiros"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Statistic(TimeStampedModel):
    titulo = models.CharField(max_length=120)
    valor = models.PositiveIntegerField(default=0)
    sufixo = models.CharField(max_length=20, blank=True)
    icone = models.CharField(max_length=80, blank=True, help_text="Classe Bootstrap Icons. Ex: bi-people-fill")
    ordem = models.PositiveSmallIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Estatistica"
        verbose_name_plural = "Estatisticas"
        ordering = ["ordem", "titulo"]

    def __str__(self):
        return self.titulo


class FAQ(TimeStampedModel):
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={"tipo": "faq"})
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    ordem = models.PositiveSmallIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["ordem", "pergunta"]

    def __str__(self):
        return self.pergunta


class VolunteerApplication(TimeStampedModel):
    ESTADO_CHOICES = [("novo", "Novo"), ("analise", "Em analise"), ("aprovado", "Aprovado"), ("rejeitado", "Rejeitado")]
    nome = models.CharField(max_length=160)
    telefone = models.CharField(max_length=60)
    email = models.EmailField()
    morada = models.CharField(max_length=255, blank=True)
    profissao = models.CharField(max_length=120, blank=True)
    area_interesse = models.CharField(max_length=160)
    curriculo = models.FileField(upload_to="curriculos/", blank=True, null=True)
    mensagem = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="novo")

    class Meta:
        verbose_name = "Candidatura de voluntario"
        verbose_name_plural = "Candidaturas de voluntarios"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome


class Donation(TimeStampedModel):
    ESTADO_CHOICES = [
        ("intencao", "Intencao recebida"),
        ("instrucoes", "Instrucoes enviadas"),
        ("comprovativo", "Comprovativo recebido"),
        ("confirmada", "Confirmada"),
        ("recibo", "Recibo emitido"),
        ("cancelada", "Cancelada"),
    ]
    TIPO_CHOICES = [
        ("nacional", "Nacional"),
        ("internacional", "Internacional"),
        ("multicaixa", "Multicaixa Express"),
        ("gateway", "Gateway online"),
        ("especie", "Doacao em especie"),
    ]
    nome = models.CharField(max_length=160, blank=True)
    telefone = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="nacional")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="intencao")
    referencia = models.CharField(max_length=120, blank=True)
    comprovativo = models.FileField(
        upload_to="doacoes/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["pdf", "jpg", "jpeg", "png", "webp"])],
    )
    observacao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Doacao"
        verbose_name_plural = "Doacoes"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome or f"Doacao #{self.pk}"


class InKindDonation(TimeStampedModel):
    ESTADO_CHOICES = [
        ("pendente", "Pendente"),
        ("aprovada", "Aprovada"),
        ("recebida", "Recebida"),
        ("distribuida", "Distribuida"),
        ("rejeitada", "Rejeitada"),
    ]
    ESTADO_ITEM_CHOICES = [
        ("novo", "Novo"),
        ("usado_bom", "Usado em bom estado"),
        ("usado_regular", "Usado em estado regular"),
    ]
    nome = models.CharField(max_length=160)
    email = models.EmailField()
    telefone = models.CharField(max_length=60)
    tipo_item = models.CharField(max_length=140)
    quantidade = models.CharField(max_length=80)
    estado_item = models.CharField(max_length=30, choices=ESTADO_ITEM_CHOICES, default="novo")
    descricao = models.TextField()
    localizacao_entrega = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="doacoes_especie/", blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendente")
    familia_ou_projeto = models.CharField(max_length=180, blank=True)
    observacao_admin = models.TextField(blank=True)

    class Meta:
        verbose_name = "Doacao em especie"
        verbose_name_plural = "Doacoes em especie"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.tipo_item} - {self.nome}"


class DonationSettings(TimeStampedModel):
    titulo = models.CharField(max_length=160, default="Como ajudar a ACSOL")
    texto_publico = models.TextField(
        default="Escolha um valor, envie a sua intencao de doacao e recebera instrucoes seguras de pagamento."
    )
    doacoes_monetarias_ativas = models.BooleanField(
        default=False,
        verbose_name="Ativar Quero Doar",
        help_text="Ligue apenas quando os dados bancarios e instrucoes oficiais estiverem confirmados.",
    )
    mensagem_doacoes_indisponiveis = models.TextField(
        blank=True,
        default=(
            "A opcao Quero Doar esta temporariamente indisponivel enquanto a ACSOL confirma "
            "os dados bancarios oficiais. Para apoiar agora, contacte a equipa da ACSOL."
        ),
        verbose_name="Mensagem quando Quero Doar estiver indisponivel",
    )
    contacto_doacoes = models.EmailField(default="doacoes@acsol.ao")
    telefone_doacoes = models.CharField(max_length=60, blank=True)
    instrucoes_nacionais = models.TextField(blank=True)
    instrucoes_internacionais = models.TextField(blank=True)
    instrucoes_multicaixa = models.TextField(blank=True)
    instrucoes_gateway = models.TextField(blank=True)
    instrucoes_especie = models.TextField(blank=True)
    gateway_url = models.URLField(blank=True)
    mostrar_dados_bancarios_publicamente = models.BooleanField(
        default=False,
        help_text="Manter desligado para nao expor dados bancarios na pagina principal.",
    )

    class Meta:
        verbose_name = "Configuracao de doacoes"
        verbose_name_plural = "Configuracao de doacoes"

    def __str__(self):
        return self.titulo


class ContactMessage(TimeStampedModel):
    nome = models.CharField(max_length=160)
    telefone = models.CharField(max_length=60, blank=True)
    email = models.EmailField()
    assunto = models.CharField(max_length=160)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensagem de contacto"
        verbose_name_plural = "Mensagens de contacto"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome} - {self.assunto}"


class NewsletterSubscriber(TimeStampedModel):
    email = models.EmailField(unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Subscritor da newsletter"
        verbose_name_plural = "Newsletter"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.email


class ActivityLog(TimeStampedModel):
    usuario = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=180)
    detalhe = models.TextField(blank=True)

    class Meta:
        verbose_name = "Log de atividade"
        verbose_name_plural = "Logs de atividade"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.acao


class ChatbotConfig(TimeStampedModel):
    PROVIDER_CHOICES = [
        ("programado", "Respostas programadas"),
        ("llama", "Llama API"),
        ("openai", "OpenAI"),
        ("gemini", "Gemini"),
        ("openai_compat", "API compativel com OpenAI"),
    ]
    MODE_CHOICES = [
        ("restrito", "Restrito a ACSOL e direitos humanos"),
        ("livre", "Livre"),
    ]
    nome = models.CharField(max_length=120, default="Chatbot IA ACSOL")
    ativo = models.BooleanField(default=True)
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default="programado")
    api_key = models.CharField(max_length=255, blank=True, help_text="Chave da API usada pelo chatbot.")
    api_url = models.URLField(default="https://api.llama-api.com/chat/completions")
    modelo = models.CharField(max_length=120, default="llama-3.1-8b-instruct")
    modo = models.CharField(max_length=20, choices=MODE_CHOICES, default="restrito")
    assuntos_permitidos = models.TextField(
        default="ACSOL Angola, direitos humanos, projetos sociais, voluntariado, eventos, doacoes, contactos, protecao de criancas, familia, inclusao social",
        help_text="Usado quando o chatbot esta em modo restrito.",
    )
    voz_ativa = models.BooleanField(default=True)
    idioma_voz = models.CharField(max_length=20, default="pt-PT")
    mensagem_inicial = models.TextField(
        default="Ola! Sou o assistente virtual da ACSOL. Posso ajudar com projetos, voluntariado, eventos, doacoes e contactos."
    )
    prompt_sistema = models.TextField(
        default=(
            "Responde apenas sobre a ACSOL Angola, projetos, voluntariado, eventos, doacoes e contactos. "
            "Se a pergunta fugir destes temas, explica educadamente que so podes responder sobre a ACSOL."
        )
    )
    resposta_padrao = models.TextField(
        default=(
            "Obrigado pela sua mensagem. Neste momento respondo apenas com informacoes programadas sobre "
            "a ACSOL Angola, voluntariado, doacoes, projetos, eventos, direitos humanos e contactos. "
            "Pode reformular a pergunta ou contactar a equipa da ACSOL."
        ),
        help_text="Resposta usada quando o chatbot esta em modo programado e nenhuma pergunta frequente corresponde.",
    )

    class Meta:
        verbose_name = "Chatbot IA"
        verbose_name_plural = "Chatbot IA"

    def __str__(self):
        return self.nome


class ChatbotFAQ(TimeStampedModel):
    config = models.ForeignKey(ChatbotConfig, on_delete=models.CASCADE, related_name="perguntas")
    pergunta = models.CharField(max_length=255)
    resposta = models.TextField()
    ordem = models.PositiveSmallIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Pergunta frequente do chatbot"
        verbose_name_plural = "Perguntas frequentes do chatbot"
        ordering = ["ordem", "pergunta"]

    def __str__(self):
        return self.pergunta
