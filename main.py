#Документация по использованию фреймворка aiogram - https://docs.aiogram.dev/en/latest/
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import token
from dbase import User
from functions import SearchPhoto, RecordVoiceMsg, VideoSearch, commands

bot = Bot(token=token)#Токен бота
dp = Dispatcher(bot)

@dp.message_handler(commands="reg")
async def reg_handler(message: types.Message):
	userID = message.from_user.id
	username = message.from_user.first_name
	reg = await User.Reg(userID,username)
	await message.reply(reg)

@dp.message_handler(commands="del")
async def del_handler(message: types.Message):
	userID = message.from_user.id
	username = message.from_user.first_name
	reg = await User.Del(userID,username)
	await message.reply(reg)

@dp.message_handler(commands="info")
async def info_handler(message: types.Message):
	userID = message.from_user.id
	info = await User.Info(userID)
	await bot.send_message(userID,info)

@dp.message_handler(commands='help')
async def help_handler(message:types.Message):
	await bot.send_message(message.from_user.id,commands,parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands='фото')
async def send_handler(message : types.Message):
	response = await SearchPhoto(message.get_args())
	try:
		await bot.send_photo(message.from_user.id,types.InputFile.from_url(f'https:{response}'),
			f'🔍 Вот что нашлось по запросу: <b>{message.get_args()}</b>',parse_mode=types.ParseMode.HTML)#Отправка фото по ссылке
	except Exception:
		await message.reply('❌Укажите запрос (/фото <запрос>)')

@dp.message_handler(commands='гс')
async def send_voice(message:types.Message):
	text = message.get_args()
	
	try:
		if len(text) > 50:
			await message.reply('❌Максимальная длина текста не должна превышать 50 символов')
		else:
			voiceMsg = await RecordVoiceMsg(text,message.from_user.id)
			await bot.send_voice(message.from_user.id,types.InputFile(voiceMsg),f'🎤 {message.from_user.first_name}, вот ваш озвученный текст')#Отправка голосового сообщения
	except Exception:
		await message.reply('❌Укажите текст для озвучки (/гс <текст>)')

@dp.message_handler(commands='видео')
async def send_video(message:types.Message):
	req = message.get_args()
	video = await VideoSearch(req)
	await bot.send_message(message.from_user.id,f'Вот что удалось найти по запросу: {req}\n{video}')

if __name__ == "__main__":
    # Запуск бота
    print('[+] Bot is running!')
    executor.start_polling(dp, skip_updates=False)