# -*- coding: utf-8 -*-
# подключение библиотек
import asyncio
from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import bleach
import re
import sys
sys.path.append('c:\BOOKS\Telegram_bot\iziTravelBot')
from iziTravel import *

print("syspath=",sys.path)
# Bot IZItravelbot01
#  https://www.youtube.com/watch?v=g4TcZVoV6eE
BOT_TOKEN="5396756594:AAF9VTxYGy3za1WLejCtFVVC3bjEuD5no6w"
admin_id = 489136424

# подключение библиотек
from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import bleach
import re

# создаем экземпляр класс api izitavel
izi=iziTRAVEL()
result=[]
page=0
step=1
city_uuid=""
object_uuid=""
# Кнопка back
buttonBack = KeyboardButton('/Главная')
kbBack = ReplyKeyboardMarkup(resize_keyboard=True).add(buttonBack)
# Кнопка Info, Objects, Photos, Audio
buttonInfo = KeyboardButton('/Инфо')
buttonObjects = KeyboardButton('/Объекты')
buttonPhotos = KeyboardButton('/Фото')
buttonAudios = KeyboardButton('/Аудио')
kbInfo1 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonObjects,buttonBack)
kbInfo2 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonAudios,buttonBack)
#
keyboard1 = [[],[]]
#print(izi.search_city("Петерйййй"))
#title,desc,images=izi.get_city_info("88472653-ad65-4d0d-9a65-7dc56860950c")
#print(images)
#obj=izi.get_city_objects_list("88472653-ad65-4d0d-9a65-7dc56860950c")
#print(obj)
#title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum("ad3427d1-3f2c-4b17-9fc2-bd20b0d673bc")
#print(images)

# Запуск бота
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

####################################################################################
@dp.message_handler(commands=['start','help'])
async def command_start(message: types.Message):
    global step
    step=1
    await message.reply("Бот IZItravel\n Здесь Вы можете получить информацию \n О музеях и турах\nВведите город посещения")

@dp.message_handler(commands=['Главная'])
async def command_start(message: types.Message):
    global step
    step=1
    await message.reply("Введите город посещения",reply_markup=ReplyKeyboardRemove())
    #await message.reply("Введите город посещения")

@dp.message_handler(commands=['Объекты'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    #if step==3:
    keyboard1 = types.InlineKeyboardMarkup(); # клавиатура
    step=3
    cities=""
    key_1=[]
    objs=izi.get_city_objects_list(city_uuid)
    i=0
    for obj in objs:
      objlist=obj.split(";")
			#кнопка
      key_1.append(types.InlineKeyboardButton(objlist[0], callback_data="step3;"+objlist[1]+";"+objlist[2])) 
			#добавляем кнопку в клавиатуру
      keyboard1.add(key_1[i]);
      i=i+1   
    await message.answer("Выберите объект", reply_markup=keyboard1)
    
@dp.message_handler(commands=['Фото'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global object_uuid
    if step==3:
      title,desc,images=izi.get_city_info(city_uuid)
      for img in images:
        fimg = open(img, 'rb')
        #await bot.send_photo(chat_id=admin_id,photo=fimg)
        await bot.send_photo(message.chat.id,photo=fimg)
    elif step==4:
      title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum(object_uuid)
      for img in images:
        fimg = open(img, 'rb')
        #await bot.send_photo(chat_id=admin_id,photo=fimg)
        await bot.send_photo(message.chat.id,photo=fimg)
        
@dp.message_handler(commands=['Аудио'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global object_uuid
    if step==4:
      title,desc,content_provider_uuid,audios,video,images=izi.get_objects_museum(object_uuid)
      print(audios)
      for audio in audios:
        faudio = open(audio, 'rb')
        #await bot.send_audio(chat_id=admin_id,audio=faudio)
        await bot.send_audio(message.chat.id,audio=faudio)
        
@dp.message_handler(commands=['Инфо'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global object_uuid
    if step==3:
      title,desc,images=izi.get_city_info(city_uuid)
      desc1=bleach.clean(desc,tags=['a'],strip=True)
      desc2=re.sub("&[a-z]{2,8};"," ",desc1)
      await message.answer(desc2)
    elif step==4:
      title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum(object_uuid)
      desc1=bleach.clean(desc,tags=['a'],strip=True)
      desc2=re.sub("&[a-z]{2,8};"," ",desc1)
      await message.answer(desc2)
      
@dp.message_handler()
async def echo(message: types.Message):
  global step
  ### search cities 
  if step==1:
    if len(message.text)<3 :
      await message.answer('В запросе поиска не менее 3 символов')
    else:
      res=izi.search_city(message.text)
      if res==[]:
        await message.reply("Объектов не обнаружено\nВведите город посещения")
      else:
        keyboard1 = types.InlineKeyboardMarkup(); # клавиатура
        step=2
        cities=""
        key_1=[]
        i=0
        for city in res:
          cities=cities+city[0]+str(step)
			    #кнопка
          key_1.append(types.InlineKeyboardButton(city[0], callback_data="step2;"+city[1])) 
			    #добавляем кнопку в клавиатуру
          keyboard1.add(key_1[i]);
          i=i+1   
        await message.answer("Выбери город", reply_markup=keyboard1)
  elif step==2:
    await message.answer("Вернись на выбор города", reply_markup=kbBack)
  elif step==3:
    await message.answer("Вернись на выбор города", reply_markup=kbBack)
  elif step==4:
    await message.answer("Вернись на выбор города", reply_markup=kbBack)

################################################################################################

@dp.callback_query_handler(Text(startswith='step2'))
async def process_callback_kbstep2(callback: types.CallbackQuery):
    global step
    global city_uuid
    step=3
    datalist = callback.data.split(";")
    uuid=datalist[1]
    city_uuid=uuid
    step=3
    title,desc,images=izi.get_city_info(uuid)
    desc1=bleach.clean(desc,tags=['a'],strip=True)
    await callback.message.answer("Выбран город <b>"+title+"</b>", reply_markup=kbInfo1)
    
@dp.callback_query_handler(Text(startswith='step3'))
async def process_callback_kbstep2(callback: types.CallbackQuery):
    global step
    global object_uuid
    datalist = callback.data.split(";")
    uuid=datalist[2]
    object_uuid=uuid
    step=4
    title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum(object_uuid)
    #desc1=bleach.clean(desc,tags=['a'],strip=True)
    await callback.message.answer("Выбран объект <b>"+title+"</b>", reply_markup=kbInfo2)

#####################################################################################################

async def on_startup(dp):

    print("Бот запущен!")

executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
#await dp.start_polling(bot)

