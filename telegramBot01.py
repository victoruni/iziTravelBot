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
from iziTravel01 import *

print("syspath=",sys.path)


# Bot IZItravelbot01
#  https://www.youtube.com/watch?v=g4TcZVoV6eE
BOT_TOKEN="5396756594:AAF9VTxYGy3za1WLejCtFVVC3bjEuD5no6w"
admin_id = 489136424

# создаем экземпляр класс api izitavel
izi=iziTRAVEL()
result=[]
page=0
step=1
city_uuid=""
city_name={}
object_uuid=""
object_name={}
collection_uuid=""
collection_name={}
#instance_uuid=""
#instance_name={}

# Кнопка back
buttonBack = KeyboardButton('/Back')
buttonMain = KeyboardButton('/Main')
kbMain = ReplyKeyboardMarkup(resize_keyboard=True).add(buttonMain)
# Кнопка Info, Objects, Photos, Audio
buttonInfo = KeyboardButton('/Info')
buttonObjects = KeyboardButton('/Objects')
buttonPhotos = KeyboardButton('/Photos')
buttonAudios = KeyboardButton('/Audio')
buttonCollection = KeyboardButton('/Collection')
kbInfo1 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonObjects).add(buttonBack).insert(buttonMain)
kbInfo2 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonAudios).add(buttonCollection).add(buttonBack).insert(buttonMain)
kbInfo3 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonAudios).add(buttonBack).insert(buttonMain)
#
keyboard1 = [[],[]]
#print(izi.search_city("Петер"))
#title,desc,images=izi.get_city_info("88472653-ad65-4d0d-9a65-7dc56860950c")
#print(images)
#obj=izi.get_city_objects_list("88472653-ad65-4d0d-9a65-7dc56860950c")
#print(obj)
#title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum("ad3427d1-3f2c-4b17-9fc2-bd20b0d673bc")
#print(images)

# Запуск бота
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

###### handler-ы для получения сообщений
@dp.message_handler(commands=['start','help'])
async def command_start(message: types.Message):
    global step
    step=1
    await message.reply("Бот IZItravel\n Здесь Вы можете получить информацию \n О музеях и турах\nВведите город посещения")

@dp.message_handler(commands=['Main'])
async def command_start(message: types.Message):
    global step
    step=1
    await message.reply("Введите город посещения"+str(step),reply_markup=ReplyKeyboardRemove())
    #await message.reply("Введите город посещения")   

@dp.message_handler(commands=['Back'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global city_name
    global object_uuid
    global object_name
    global collection_name

    #await message.answer("BACK"+str(step), reply_markup=ReplyKeyboardRemove())
    await message.answer("BACK", reply_markup=ReplyKeyboardRemove())
    #### collection
    if step==5:    
      keyboard1 = types.InlineKeyboardMarkup(); # клавиатура
      collection_name.clear()
      key_1=[]
      collections=izi.get_children_museum(object_uuid)
      i=0
      for collection in collections:
        collectionlist=collection.split(";")
        collection_name[collectionlist[1]]=collectionlist[0]
			  #кнопка
        key_1.append(types.InlineKeyboardButton(collectionlist[0], callback_data="step4;"+collectionlist[1])) 
			  #добавляем кнопку в клавиатуру
        keyboard1.add(key_1[i]);
        i=i+1   
      step=4  
      await message.answer("Выберите объект", reply_markup=keyboard1)
      title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum(object_uuid)
      kbInfo2 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonAudios).add(buttonCollection).add(buttonBack).insert(buttonMain)
      buttonTitle = KeyboardButton(object_name[object_uuid])
      kbInfo2.add(buttonTitle)
      await message.answer("Выбран объект <b>"+title+"</b>", reply_markup=kbInfo2)
    #### objects
    elif step==4:
      keyboard1 = types.InlineKeyboardMarkup(); # клавиатура
      object_name.clear()
      key_1=[]
      objs=izi.get_city_objects_list(city_uuid)
      #print(objs)
      i=0
      for obj in objs:
        objlist=obj.split(";")
        object_name[objlist[2]]=objlist[0]
			  #кнопка
        #key_1.append(types.InlineKeyboardButton(objlist[0], callback_data="step3;"+objlist[1]+";"+objlist[2])) 
        key_1.append(types.InlineKeyboardButton(objlist[0], callback_data="step3;"+objlist[2])) 
			  #добавляем кнопку в клавиатуру
        keyboard1.add(key_1[i]);
        i=i+1   
      step=3
      title,desc,images=izi.get_city_info(city_uuid)
      kbInfo1 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonObjects).add(buttonBack).insert(buttonMain)
      buttonTitle = KeyboardButton(city_name[city_uuid])
      kbInfo1.add(buttonTitle)
      await message.answer("Выбран город <b>"+title+"</b>", reply_markup=kbInfo1)
    #####
    else:
      step=1
      await message.reply("Введите город посещения"+str(step),reply_markup=ReplyKeyboardRemove())
    #await message.reply("Введите город посещения")   

@dp.message_handler(commands=['Collection'])
async def command_start(message: types.Message):
    global step
    global object_uuid
    global collection_name
    keyboard1 = types.InlineKeyboardMarkup(); # клавиатура
    step=4
    collection_name.clear()
    key_1=[]
    collections=izi.get_children_museum(object_uuid)
    i=0
    for collection in collections:
      collectionlist=collection.split(";")
      collection_name[collectionlist[1]]=collectionlist[0]
			#кнопка
      key_1.append(types.InlineKeyboardButton(collectionlist[0], callback_data="step4;"+collectionlist[1])) 
			#добавляем кнопку в клавиатуру
      keyboard1.add(key_1[i]);
      i=i+1   
    await message.answer("Выберите объект", reply_markup=keyboard1)

@dp.message_handler(commands=['Objects'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global object_name
    #if step==3:
    keyboard1 = types.InlineKeyboardMarkup(); # клавиатура
    step=3
    object_name.clear()
    key_1=[]
    objs=izi.get_city_objects_list(city_uuid)
    print(objs)
    i=0
    for obj in objs:
      objlist=obj.split(";")
      object_name[objlist[2]]=objlist[0]
			#кнопка
      #key_1.append(types.InlineKeyboardButton(objlist[0], callback_data="step3;"+objlist[1]+";"+objlist[2])) 
      key_1.append(types.InlineKeyboardButton(objlist[0], callback_data="step3;"+objlist[2])) 
			#добавляем кнопку в клавиатуру
      keyboard1.add(key_1[i]);
      i=i+1   
    await message.answer("Выберите объект", reply_markup=keyboard1)

@dp.message_handler(commands=['Photos'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global object_uuid
    global collection_uuid
    if step==3:
      title,desc,images=izi.get_city_info(city_uuid)
      if len(images)<1:
        await message.answer("Фото отсутствует")
      else:
        for img in images:
          fimg = open(img, 'rb')
          await bot.send_photo(message.chat.id,photo=fimg)
    elif step==4:
      title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum(object_uuid)
      if len(images)<1:
        await message.answer("Фото отсутствует")
      else:
        for img in images:
          fimg = open(img, 'rb')
          await bot.send_photo(message.chat.id,photo=fimg)
    elif step==5:
      desc,content_provider_uuid,audio,video,images=izi.get_children(collection_uuid)
      if len(images)<1:
        await message.answer("Фото отсутствует")
      else:
        for img in images:
          fimg = open(img, 'rb')
          await bot.send_photo(message.chat.id,photo=fimg)

@dp.message_handler(commands=['Audio'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global object_uuid
    global collection_uuid
    if step==4:
      title,desc,content_provider_uuid,audios,video,images=izi.get_objects_museum(object_uuid)
      print(audios)
      if len(audios)<1:
        await message.answer("Аудио отсутствует")
      else:
        for audio in audios:
          faudio = open(audio, 'rb')
          await bot.send_audio(message.chat.id,audio=faudio)
    if step==5:
      desc,content_provider_uuid,audios,video,images=izi.get_children(collection_uuid)
      print(audios)
      if len(audios)<1:
        await message.answer("Аудио отсутствует")
      else:
        for audio in audios:
          faudio = open(audio, 'rb')
          await bot.send_audio(message.chat.id,audio=faudio)

@dp.message_handler(commands=['Info'])
async def command_start(message: types.Message):
    global step
    global city_uuid
    global object_uuid
    global collection_uuid
    if step==3:
      title,desc,images=izi.get_city_info(city_uuid)
      if desc=="":
        await message.answer("Описание отсутствует")
      else:
        desc1=bleach.clean(desc,tags=['a'],strip=True)
        desc2=re.sub("&[a-z]{2,8};"," ",desc1)
        await message.answer(desc2)
    elif step==4:
      title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum(object_uuid)
      if desc=="":
        await message.answer("Описание отсутствует")
      else:
        desc1=bleach.clean(desc,tags=['a'],strip=True)
        desc2=re.sub("&[a-z]{2,8};"," ",desc1)
        await message.answer(desc2)
    elif step==5:
      desc,content_provider_uuid,audio,video,images=izi.get_children(collection_uuid)
      if desc=="":
        await message.answer("Описание отсутствует")
      else:
        desc1=bleach.clean(desc,tags=['a'],strip=True)
        desc2=re.sub("&[a-z]{2,8};"," ",desc1)
        await message.answer(desc2)

@dp.message_handler()
async def echo(message: types.Message):
  global step
  global city_name
  ### search cities 
  print("message.text",message.text)
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
        city_name.clear()
        #cities=""
        key_1=[]
        i=0
        for city in res:
          #cities=cities+city[0]+str(step)
          city_name[city[1]]=city[0]
			    #кнопка
          #key_1.append(types.InlineKeyboardButton(city[0], callback_data="step2;"+city[1]+";"+city[0])) 
          key_1.append(types.InlineKeyboardButton(city[0], callback_data="step2;"+city[1])) 
			    #добавляем кнопку в клавиатуру
          keyboard1.add(key_1[i]);
          i=i+1   
        print(city_name)
        await message.answer("Выбери город", reply_markup=keyboard1)
  #elif step==2:
  #  await message.answer("Вернись на выбор города", reply_markup=kbMain)
  #elif step==3:
  #  await message.answer("Вернись на выбор города", reply_markup=kbMain)
  #elif step==4:
  #  await message.answer("Вернись на выбор города", reply_markup=kbMain)
  else:
    step=1
    await message.reply("Введите город посещения",reply_markup=ReplyKeyboardRemove())    

###################### callback-и
@dp.callback_query_handler(Text(startswith='step2'))
async def process_callback_kbstep2(callback: types.CallbackQuery):
    global step
    global city_uuid
    global city_name
    #global name_uuid
    step=3
    datalist = callback.data.split(";")
    uuid=datalist[1]
    city_uuid=uuid
    step=3
    title,desc,images=izi.get_city_info(city_uuid)
    #desc1=bleach.clean(desc,tags=['a'],strip=True)
    kbInfo1 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonObjects).add(buttonBack).insert(buttonMain)
    buttonTitle = KeyboardButton(city_name[city_uuid])
    kbInfo1.add(buttonTitle)
    await callback.message.answer("Выбран город <b>"+title+"</b>", reply_markup=kbInfo1)

@dp.callback_query_handler(Text(startswith='step3'))
async def process_callback_kbstep2(callback: types.CallbackQuery):
    global step
    global object_uuid
    global object_name
    datalist = callback.data.split(";")
    #uuid=datalist[2]
    uuid=datalist[1]
    object_uuid=uuid
    step=4
    title,desc,content_provider_uuid,audio,video,images=izi.get_objects_museum(object_uuid)
    #desc1=bleach.clean(desc,tags=['a'],strip=True)
    kbInfo2 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonAudios).add(buttonCollection).add(buttonBack).insert(buttonMain)
    buttonTitle = KeyboardButton(object_name[object_uuid])
    #buttonPrev = KeyboardButton("<")
    #buttonNext = KeyboardButton(">")
    #kbInfo2.row(buttonPrev,buttonTitle,buttonNext)
    kbInfo2.add(buttonTitle)
    await callback.message.answer("Выбран объект <b>"+title+"</b>", reply_markup=kbInfo2)

@dp.callback_query_handler(Text(startswith='step4'))
async def process_callback_kbstep2(callback: types.CallbackQuery):
    global step
    global collection_uuid
    global collection_name
    datalist = callback.data.split(";")
    #uuid=datalist[2]
    uuid=datalist[1]
    collection_uuid=uuid
    step=5
    title=collection_name[collection_uuid]
    desc,content_provider_uuid,audio,video,images=izi.get_children(collection_uuid)
    #desc1=bleach.clean(desc,tags=['a'],strip=True)
    kbInfo2 = ReplyKeyboardMarkup(resize_keyboard=True).row(buttonInfo,buttonPhotos,buttonAudios).add(buttonBack).insert(buttonMain)
    buttonTitle = KeyboardButton(collection_name[collection_uuid])
    #buttonPrev = KeyboardButton("<")
    #buttonNext = KeyboardButton(">")
    #kbInfo2.row(buttonPrev,buttonTitle,buttonNext)
    kbInfo2.add(buttonTitle)
    await callback.message.answer("Выбран объект <b>"+title+"</b>", reply_markup=kbInfo2)

########### запуск

async def on_startup(dp):
    print("Бот запущен!")

executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
#await dp.start_polling(bot)

