import telebot
from telebot import types
from telethon import TelegramClient
from settings import entity, api_id, api_fash, bot_user_name

client = TelegramClient(entity, api_id, api_fash)

async def main(files):
	path = files
	async with client.action(bot_user_name, "document") as action:
		await client.send_file(bot_user_name, path, progress_callback=action.progress)
with client:
	client.loop.run_until_complete(main(r"C:\Users\kulemzin_i\Desktop\Code\09nov.zip"))