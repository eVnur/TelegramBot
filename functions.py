from bs4 import BeautifulSoup
import json
import requests
import random
import gtts
from youtubesearchpython import VideosSearch

commands = f'📋 Список команд:\n\n<b>/reg</b> - Зарегистрироваться на боте\n<b>/del</b> - Удалить свой профиль на боте\
		\n<b>/info</b> - Личная информация\n<b>/фото [запрос]</b> - Поиск фото по запрсу\n<b>/гс [текст]</b> - Озвучить ваш текст\
		\n<b>/видео [запрос]</b> - Поиск видео по запрсу'

async def SearchPhoto(req):#Функция для поиска фотографии по запросу
	response = requests.get(f"https://yandex.ru/images/search?from=tabbar&text={req}")
	soup = BeautifulSoup(response.text, features="html.parser")
	images = []
	for img in soup.findAll('img'):
		images.append(img.get('src'))
	return random.choice(images)

async def RecordVoiceMsg(text,userID):#Функция для озвучки текста
	gs = gtts.gTTS(text, lang="ru")
	path = f"voice_messages/{userID}_VoiceMsg.wav"#Путь для сохранения озвучки
	gs.save(path)
	return path

async def VideoSearch(req):#Функция для поиска видео по запросу
	response = VideosSearch(req,limit=10)
	rand = random.randint(0,9)
	return response.result()['result'][rand]['link']