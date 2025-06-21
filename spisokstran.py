import discord
import json
import os

from discord.ext import commands

# Укажи ID канала и ID сообщения, где должен обновляться список
LIST_CHANNEL_ID = 1382442067086544896  # <-- замени на ID своего канала
LIST_MESSAGE_ID = 1385520772222681190  # <-- замени на ID сообщения, которое бот будет редактировать
JSON_PATH = "spisokstran.json"  # путь к json-файлу со списком стран

# Функция обновления embed со списком занятых стран
async def update_country_list(bot):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    taken = data.get("taken_countries", [])
    if not taken:
        description = "Пока ни одна страна не занята."
    else:
        taken.sort()
        description = "\n".join([f"🌐 {c}" for c in taken])

    embed = discord.Embed(
        title="📋 Занятые страны",
        description=description,
        color=discord.Color.dark_blue()
    )

    channel = bot.get_channel(LIST_CHANNEL_ID)
    if channel is None:
        print("❌ Канал не найден!")
        return

    try:
        message = await channel.fetch_message(LIST_MESSAGE_ID)
        await message.edit(embed=embed)
    except discord.NotFound:
        print("❌ Сообщение не найдено!")
    except Exception as e:
        print(f"⚠️ Ошибка при обновлении списка: {e}")

# Функция регистрации страны
async def register_country(bot, country_name: str):
    if not os.path.exists(JSON_PATH):
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if country_name not in data["all_countries"]:
        print("❌ Такой страны нет в списке!")
        return

    if country_name in data["taken_countries"]:
        print("⚠️ Страна уже занята!")
        return

    data["taken_countries"].append(country_name)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    await update_country_list(bot)
    print(f"✅ Зарегистрирована страна: {country_name}")