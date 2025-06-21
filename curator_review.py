#curator_review.py

import discord
from discord.ui import View, Button

class CuratorDecisionView(View):
    def __init__(self, user: discord.Member, role_type: str, country_name: str):
        super().__init__(timeout=None)
        self.user = user
        self.role_type = role_type
        self.country_name = country_name

    @discord.ui.button(label="✅ Одобрить", style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, button: Button):
        roles_to_give = []

        # Получаем все роли
        license_role = discord.utils.get(interaction.guild.roles, name=f"Лицензия: {self.country_name}")
        economy_role = discord.utils.get(interaction.guild.roles, name=" Ужасная экономика")
        main_role = discord.utils.get(interaction.guild.roles, name=f"{self.role_type} | {self.country_name}")

        # Добавляем найденные роли
        for role in [license_role, economy_role, main_role]:
            if role:
                roles_to_give.append(role)

        if roles_to_give:
            await self.user.add_roles(*roles_to_give)

        # Уведомляем
        try:
            await self.user.send(f"✅ Ваша заявка за {self.country_name} одобрена!")
        except discord.Forbidden:
            await interaction.followup.send("Не удалось отправить сообщение в личку пользователю.", ephemeral=True)

        await interaction.response.send_message(" Заявка одобрена!", ephemeral=True)
        self.stop()

    @discord.ui.button(label="❌ Отклонить", style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("✍️ Введите причину отказа:", ephemeral=True)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await interaction.client.wait_for("message", timeout=60.0, check=check)
            reason = msg.content
            try:
                await self.user.send(f"❌ Ваша заявка за {self.country_name} отклонена.\nПричина: {reason}")
            except discord.Forbidden:
                await interaction.followup.send("Не удалось отправить сообщение в личку пользователю.", ephemeral=True)
            await interaction.followup.send("✅ Отказ отправлен.", ephemeral=True)
        except Exception:
            await interaction.followup.send("⏱️ Время ожидания истекло.", ephemeral=True)
        self.stop()