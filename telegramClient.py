import telebot
from telebot import types
from telethon import TelegramClient

entity = "icool5520"
api_id = 19593818
api_fash = "1de8790c18365fc55545b31c9650a8d2"
phone = "+380997738386"
client = TelegramClient(entity, api_id, api_fash)
#client.connect()
#client.send_code_request(phone)


async def main(files):
	path = files
	async with client.action("@FatCatFartingBot", "document") as action:
		await client.send_file("@FatCatFartingBot", path, progress_callback=action.progress)
with client:
	client.loop.run_until_complete(main(r"C:\Users\kulemzin_i\Desktop\Code\09nov.zip"))