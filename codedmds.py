from curator_review import CuratorDecisionView
from spisokstran import register_country
import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TICKET_CHANNEL_ID = 1383431136344015000

# --- МОДАЛЫ ---

class CountryModal(Modal, title="Заявка на страну"):
    country_name = TextInput(label="Название страны", max_length=45)
    ideology = TextInput(label="Идеология страны", max_length=100)
    agreement = TextInput(label="Ознакомлен с правилами (да/нет)", max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📨 Новая заявка: Страна",
            description=(
                f"Пользователь: {interaction.user.mention}\n"
                f"Страна: {self.country_name}\n"
                f"Идеология: {self.ideology}\n"
                f"Ознакомлен: {self.agreement}"
            ),
            color=discord.Color.green()
        )

        channel = interaction.client.get_channel(TICKET_CHANNEL_ID)
        if channel:
            await channel.send(
                embed=embed,
                view=CuratorDecisionView(interaction.user, "🌍 Страна", str(self.country_name))
            )

        await interaction.response.send_message("✅ Заявка отправлена!", ephemeral=True)

class PMCModal(Modal, title="Заявка на ЧВК / Министра"):
    name = TextInput(label="Название ЧВК / Министра", max_length=45)
    target_country = TextInput(label="Целевая страна", max_length=45)
    permission = TextInput(label="Есть ли согласие от президента?", max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📨 Новая заявка: ЧВК / Министр",
            description=(
                f"**Пользователь:** {interaction.user.mention}\n"
                f"**Название:** {self.name}\n"
                f"**Страна:** {self.target_country}\n"
                f"**Согласие от президента:** {self.permission}"
            ),
            color=discord.Color.orange()
        )
        channel = interaction.client.get_channel(TICKET_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
        await interaction.response.send_message("✅ Заявка отправлена!", ephemeral=True)
        channel = bot.get_channel(1383431136344015000)  # ID твоего канала
        await channel.send(
        content=
                f"📝 Новая заявка от {interaction.user.mention}\nСтрана: {country_name}",
        view=CuratorDecisionView(interaction.user, "Страна", country_name)
)

# --- КНОПКИ ---
class RoleSelectView(View):
    @discord.ui.button(label="🌍 Страна", style=discord.ButtonStyle.success)
    async def country_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(CountryModal())

    @discord.ui.button(label="🕴 ЧВК", style=discord.ButtonStyle.primary)
    async def pmc_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(PMCModal())

    @discord.ui.button(label="🏛 Министр", style=discord.ButtonStyle.secondary)
    async def minister_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(PMCModal())

# --- КОМАНДА РЕГИСТРАЦИИ ---
@bot.command()
async def регистрация(ctx):
    embed = discord.Embed(
        title="📋 Регистрация",
        description=(
            "Добро пожаловать!\n\n"
            "Здесь вы можете пройти регистрацию в одном из трёх статусов:\n\n"
            "🌍 **Страна**\n"
            "🕴 **ЧВК**\n"
            "🏛 **Министр**\n\n"
            "**Важно:**\n"
            "- Если вы хотите занять роль ЧВК или Министра, вы обязаны получить одобрение от президента соответствующей страны.\n"
            "- Если вы хотите зарегистрироваться за страну, предварительно убедитесь, что она свободна. Ознакомьтесь с каналом #занятые-страны.\n"
            "- Выбор занятой страны приведёт к автоматическому отказу.\n"
        ),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=RoleSelectView())

# --- БАЗОВЫЕ КОМАНДЫ ---
@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")


# --- ЗАПУСК ---
bot.run("MTM4MzM2MTc4NTM0Mzc3NDg2Mg.GnE9CV.dZrcIrlK240W9s3zDpnGcLUnbCSDkysO84P11c")