from django.db import migrations, models


def use_programmed_chatbot_when_api_is_empty(apps, schema_editor):
    ChatbotConfig = apps.get_model("core", "ChatbotConfig")
    ChatbotConfig.objects.filter(api_key="").update(provider="programado")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_siteconfig_texto_parceiros_siteconfig_texto_valores_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatbotconfig",
            name="provider",
            field=models.CharField(
                choices=[
                    ("programado", "Respostas programadas"),
                    ("llama", "Llama API"),
                    ("openai", "OpenAI"),
                    ("gemini", "Gemini"),
                    ("openai_compat", "API compativel com OpenAI"),
                ],
                default="programado",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="chatbotconfig",
            name="resposta_padrao",
            field=models.TextField(
                default=(
                    "Obrigado pela sua mensagem. Neste momento respondo apenas com informacoes programadas sobre "
                    "a ACSOL Angola, voluntariado, doacoes, projetos, eventos, direitos humanos e contactos. "
                    "Pode reformular a pergunta ou contactar a equipa da ACSOL."
                ),
                help_text="Resposta usada quando o chatbot esta em modo programado e nenhuma pergunta frequente corresponde.",
            ),
        ),
        migrations.RunPython(use_programmed_chatbot_when_api_is_empty, migrations.RunPython.noop),
    ]
