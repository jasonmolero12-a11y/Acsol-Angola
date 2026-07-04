import os

from django.contrib.auth.models import Group, Permission, User

from django.core.management.base import BaseCommand

from core.models import (
    Category,
    Article,
    ChatbotConfig,
    ChatbotFAQ,
    DonationSettings,
    GalleryItem,
    Project,
    ProvinceOffice,
    SiteConfig,
    Statistic,
    TeamMember,
    UserProfile,
)


class Command(BaseCommand):
    help = "Cria dados iniciais para demonstracao do painel ACSOL."

    def handle(self, *args, **options):
        SiteConfig.objects.get_or_create(
            nome="ACSOL - Acao de Solidariedade em Angola",
            defaults={
                "slogan": "Unidos pela solidariedade, transformamos vidas.",
                "hero_titulo": "Transformando vidas em Angola",
                "hero_subtitulo": "Apoiamos comunidades por meio de educacao, saude, saneamento, seguranca alimentar e voluntariado.",
                "telefone": "+244 923 456 789",
                "email": "geral@acsol.ao",
                "endereco": "Rua da Solidariedade, Luanda - Angola",
                "whatsapp": "244923456789",
            },
        )

        categorias = {
            "educacao": Category.objects.get_or_create(nome="Educacao", tipo="projeto")[0],
            "saneamento": Category.objects.get_or_create(nome="Agua e Saneamento", tipo="projeto")[0],
            "alimentar": Category.objects.get_or_create(nome="Seguranca Alimentar", tipo="projeto")[0],
        }
        categoria_evento = Category.objects.get_or_create(nome="Evento Social", tipo="evento")[0]

        Project.objects.get_or_create(
            titulo="Escola para Todos",
            defaults={
                "categoria": categorias["educacao"],
                "descricao": "Apoio escolar e material didatico para criancas em situacao de vulnerabilidade.",
                "beneficiarios": 1200,
                "localizacao": "Luanda e Malanje",
                "estado": "andamento",
                "progresso": 78,
                "destaque": True,
            },
        )
        Project.objects.get_or_create(
            titulo="Agua Limpa Angola",
            defaults={
                "categoria": categorias["saneamento"],
                "descricao": "Instalacao de sistemas de abastecimento de agua potavel em comunidades rurais.",
                "beneficiarios": 850,
                "localizacao": "Huambo e Bie",
                "estado": "andamento",
                "progresso": 55,
                "destaque": True,
            },
        )
        Project.objects.get_or_create(
            titulo="Cestas Solidarias",
            defaults={
                "categoria": categorias["alimentar"],
                "descricao": "Distribuicao de cabazes alimentares a familias vulneraveis.",
                "beneficiarios": 3200,
                "localizacao": "Luanda, Benguela e Cabinda",
                "estado": "andamento",
                "progresso": 92,
                "destaque": True,
            },
        )

        stats = [
            ("Beneficiarios Diretos", 5248, "+", "bi-people-fill", 1),
            ("Projetos Realizados", 48, "", "bi-folder-fill", 2),
            ("Voluntarios Ativos", 213, "+", "bi-heart-fill", 3),
            ("Provincias Cobertas", 12, "", "bi-geo-alt-fill", 4),
        ]
        for titulo, valor, sufixo, icone, ordem in stats:
            Statistic.objects.get_or_create(
                titulo=titulo,
                defaults={"valor": valor, "sufixo": sufixo, "icone": icone, "ordem": ordem},
            )

        team_members = [
            ("Jason", "Administrador", "Responsavel pela gestao geral da plataforma e acompanhamento institucional.", 1),
            ("Francisco", "Gerente", "Acompanha dados, candidaturas, doacoes e atualizacoes operacionais da ACSOL.", 2),
            ("Zakaria", "Gerente", "Apoia a coordenacao de projetos sociais, voluntariado e informacoes publicas.", 3),
            ("Junias", "Gerente", "Apoia a organizacao de conteudos, relatorios e acompanhamento administrativo.", 4),
        ]
        for nome, cargo, biografia, ordem in team_members:
            TeamMember.objects.get_or_create(
                nome=nome,
                defaults={"cargo": cargo, "biografia": biografia, "ordem": ordem, "ativo": True},
            )

        province_offices = [
            ("Luanda", "Cazenga", "Sede e coordenacao nacional da ACSOL.", "-8.839988", "13.289437", 1),
            ("Benguela", "Benguela", "Acompanhamento de projetos comunitarios e voluntariado.", "-12.576262", "13.405470", 2),
            ("Huambo", "Huambo", "Apoio a projetos de educacao, familia e direitos humanos.", "-12.776110", "15.739170", 3),
            ("Malanje", "Malanje", "Atuacao comunitaria e mobilizacao local.", "-9.540150", "16.340960", 4),
            ("Cabinda", "Cabinda", "Ponto de contacto para iniciativas sociais.", "-5.550000", "12.200000", 5),
            ("Huila", "Lubango", "Divisao regional para projetos e parcerias.", "-14.917170", "13.492500", 6),
        ]
        for provincia, municipio, descricao, latitude, longitude, ordem in province_offices:
            ProvinceOffice.objects.get_or_create(
                provincia=provincia,
                defaults={
                    "municipio": municipio,
                    "descricao": descricao,
                    "latitude": latitude,
                    "longitude": longitude,
                    "telefone": "+244 923 456 789",
                    "email": "geral@acsol.ao",
                    "ordem": ordem,
                    "ativo": True,
                },
            )

        events = [
            ("Workshop de Voluntariado", "Formacao para novos voluntarios sobre intervencao social e apoio comunitario.", "2026-07-15"),
            ("Dia da Solidariedade", "Acao de recolha e entrega de alimentos, roupa e material escolar para familias vulneraveis.", "2026-08-28"),
            ("Forum Social ACSOL", "Encontro com parceiros e comunidades para debater direitos humanos e protecao social.", "2026-09-10"),
        ]
        for titulo, resumo, data in events:
            Article.objects.get_or_create(
                titulo=titulo,
                defaults={
                    "tipo": "evento",
                    "categoria": categoria_evento,
                    "resumo": resumo,
                    "conteudo": "Local e detalhes podem ser atualizados pelo administrador ou gerente no painel.",
                    "data_publicacao": data,
                    "publicado": True,
                    "destaque": False,
                },
            )

        donation_settings, created = DonationSettings.objects.get_or_create(
            titulo="Como ajudar a ACSOL",
            defaults={
                "texto_publico": "Envie a sua intencao de doacao para receber instrucoes seguras de pagamento.",
                "contacto_doacoes": "doacoes@acsol.ao",
                "telefone_doacoes": "+244 934 567 890",
                "instrucoes_nacionais": "Doacao nacional:\nBanco: Banco Angolano de Investimentos (BAI)\nTitular: ACSOL - Acao de Solidariedade em Angola\nIBAN: AO06 0040 0000 1234 5678 1012 3\nReferencia: ACSOL-DOA\nDepois do pagamento, envie o comprovativo neste formulario ou para doacoes@acsol.ao.",
                "instrucoes_internacionais": "Doacao internacional:\nBanco: Banco Angolano de Investimentos (BAI)\nTitular: ACSOL - Acao de Solidariedade em Angola\nIBAN: AO06 0040 0000 1234 5678 1012 3\nSWIFT/BIC: BAIPAOLU\nReferencia: ACSOL-INT\nConfirme os dados reais no admin antes da producao.",
                "instrucoes_multicaixa": "Multicaixa Express:\nNumero: +244 934 567 890\nReferencia: ACSOL-MCX\nDepois do pagamento, envie o comprovativo neste formulario ou para doacoes@acsol.ao.",
                "instrucoes_gateway": "Pagamento online:\nGateway ainda sera ativado na fase avancada. Por agora, submeta a intencao de doacao e a equipa enviara uma alternativa segura.",
                "instrucoes_especie": "Doacao em especie:\nPode doar alimentos, roupa, material escolar, medicamentos permitidos, equipamentos ou outros bens uteis.\nDepois de preencher o formulario, a equipa da ACSOL entrara em contacto para combinar local, data e comprovacao da entrega.",
            },
        )
        if not created and not donation_settings.instrucoes_nacionais:
            donation_settings.instrucoes_nacionais = "Doacao nacional:\nBanco: Banco Angolano de Investimentos (BAI)\nTitular: ACSOL - Acao de Solidariedade em Angola\nIBAN: AO06 0040 0000 1234 5678 1012 3\nReferencia: ACSOL-DOA"
        donation_settings.mostrar_dados_bancarios_publicamente = False
        if not donation_settings.instrucoes_especie:
            donation_settings.instrucoes_especie = "Doacao em especie:\nInforme no campo mensagem quais bens pretende doar. A equipa da ACSOL entrara em contacto para combinar a entrega."
        donation_settings.save()

        chatbot, _ = ChatbotConfig.objects.get_or_create(
            nome="Chatbot IA ACSOL",
            defaults={
                "provider": "llama",
                "api_url": "https://api.llama-api.com/chat/completions",
                "modelo": "llama-3.1-8b-instruct",
                "modo": "restrito",
                "voz_ativa": True,
                "idioma_voz": "pt-PT",
            },
        )
        chatbot.modo = chatbot.modo or "restrito"
        chatbot.assuntos_permitidos = chatbot.assuntos_permitidos or "ACSOL Angola, direitos humanos, projetos sociais, voluntariado, eventos, doacoes, contactos"
        chatbot.voz_ativa = True
        chatbot.save()
        faqs = [
            ("Como posso ser voluntario?", "Preencha o formulario de voluntariado no site. A equipa da ACSOL analisara a candidatura e entrara em contacto."),
            ("Como posso doar?", "Clique em Como Ajudar, escolha um valor e envie a intencao de doacao. As instrucoes de pagamento serao enviadas de forma segura."),
            ("Onde fica a ACSOL?", "A ACSOL tem sede em Luanda, Angola, e atua em varias provincias por meio de projetos sociais."),
        ]
        for ordem, (pergunta, resposta) in enumerate(faqs, start=1):
            ChatbotFAQ.objects.get_or_create(
                config=chatbot,
                pergunta=pergunta,
                defaults={"resposta": resposta, "ordem": ordem},
            )

        admin_user, _ = User.objects.get_or_create(
            username="jason",
            defaults={"first_name": "Jason", "email": "admin@acsol.ao", "is_staff": True, "is_superuser": True},
        )
        admin_user.first_name = "Jason"
        admin_user.last_name = ""
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password(os.getenv("ACSOL_ADMIN_PASSWORD", "change-me-admin"))
        admin_user.save()
        admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
        admin_profile.role = "admin"
        admin_profile.save()

        gerente_group, _ = Group.objects.get_or_create(name="Gerente")
        gerente_group.permissions.set(Permission.objects.all())

        managers = [
            ("francisco", "Francisco"),
            ("zakaria", "Zakaria"),
            ("junias", "Junias"),
        ]
        for username, first_name in managers:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first_name, "email": f"{username}@acsol.ao", "is_staff": True},
            )
            user.first_name = first_name
            user.last_name = ""
            user.is_staff = True
            user.is_superuser = False
            user.is_active = True
            user.set_password(os.getenv("ACSOL_MANAGER_DEFAULT_PASSWORD", "change-me-manager"))
            user.save()
            user.groups.add(gerente_group)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = "gerente"
            profile.save()

        self.stdout.write(self.style.SUCCESS("Dados iniciais criados/atualizados."))
