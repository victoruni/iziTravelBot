# -*- coding: utf-8 -*-
import requests
import json
import os
from ast import Not

MEDIA_BASE_URL="https://media.izi.travel"
URL_SEARCH_CITY="https://api.izi.travel/mtg/objects/search/"
URL_CITY_INFO="https://api.izi.travel/cities/"
URL_CITY_OBJECTS_LIST="https://api.izi.travel/cities/"
URL_CITY_OBJECTS_COUNT="https://api.izi.travel/cities/"
URL_MUSEUM_OBJECT="https://api.izi.travel/mtgobjects/"
URL_MUSEUM_CHILDREN="https://api.izi.travel/mtgobjects/"
URL_MUSEUM_CHILDREN_INSTANCE="https://api.izi.travel/mtgobjects/"
KEY_IZITRAVEL="e3c72fd2-32c8-4550-b915-bd55f266c9dc"
IMAGE_SIZE="480x360"        # 1600x1200, 800x600, 480x360, 240x180, 120x90

#############################################################################
#####################  class iziTRAVEL() ####################################
#############################################################################
class iziTRAVEL():
 
  ######################### получить имя файла audio #########################
  def get_path_audio(self,dir,name):  # {MEDIA_BASE_URL}/{CONTENT_PROVIDER_UUID}/{AUDIO_UUID}.m4a
    filename=MEDIA_BASE_URL+"/"+dir+"/"+name+".m4a"
    ext="m4a" 
    return filename,ext

  ####################### получить имя файла video ###########################
  def get_path_video(self,dir,name):  # {MEDIA_BASE_URL}/{CONTENT_PROVIDER_UUID}/{VIDEO_UUID}.mp4
    filename=MEDIA_BASE_URL+"/"+dir+"/"+name+".mp4"
    ext="mp4"  
    return filename,ext

  ############################### получить имя файла img  #################### 
  #######(type - city, story, map and brand_cover, brand_logo, sponsor_logo) #####
  def get_path_image(self,dir,name,type):
    filename=""
    if type=='city':  # {MEDIA_BASE_URL}/cities/{CITY_UUID}/{CITY_IMAGE_UUID}.jpg
      filename=MEDIA_BASE_URL+"/"+dir+"/"+name+".jpg"
      ext="jpg"
    elif type=='story': # {MEDIA_BASE_URL}/{CONTENT_PROVIDER_UUID}/{IMAGE_UUID}_{IMAGE_SIZE}.jpg
      filename=MEDIA_BASE_URL+"/"+dir+"/"+name+"_"+IMAGE_SIZE+".jpg"
      ext="jpg"
    elif type=='map':    # {MEDIA_BASE_URL}/{CONTENT_PROVIDER_UUID}/{IMAGE_UUID}.jpg
      filename=MEDIA_BASE_URL+"/"+dir+"/"+name+".jpg"
      ext="jpg"
    elif type=='brand_cover': # {MEDIA_BASE_URL}/{CONTENT_PROVIDER_UUID}/{IMAGE_UUID}.jpg
      filename=MEDIA_BASE_URL+"/"+dir+"/"+name+".jpg"     
      ext="jpg"
    elif type=='sponsor_logo': # {MEDIA_BASE_URL}/{CONTENT_PROVIDER_UUID}/{IMAGE_UUID}.png
      filename=MEDIA_BASE_URL+"/"+dir+"/"+name+".png"
      ext="png"
    return filename,ext

  ####################### сохранить файл media на диске #####################
  def save_file_media(self,dir,name,imgurl,ext):
    if not os.path.exists(dir):
      os.mkdir(dir)
    #filename="cities/"+data1['uuid']+"/"+img['uuid']+".jpg"
    filename=dir+"/"+name+"."+ext
    print(filename," ",imgurl)
    r = requests.get(imgurl, allow_redirects=True)
    open(filename, 'wb').write(r.content) 
    return filename

  
  ################### поиск города по названию  ##############################
  ################ https://api.izi.travel/mtg/objects/search/ ################
  def search_city(self,name):
    result=[]     
    url=URL_SEARCH_CITY;
    #querystring = {"languages":"ru","languages":"en,ru","includes":"translations","type":"city","query":name}
    querystring = {"languages":"ru","languages":"ru","type":"city","query":name}  
    headers = {
	    "X-IZI-API-KEY": KEY_IZITRAVEL,    
	    "Accept":"application/izi-api-v1.8+json"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #print(response.text) 
    data1=json.loads(response.text)
    #print(data1)
    #print(data1['content'])
    for data2 in data1:
      print(data2['title'])
      print(data2['uuid']) 
      result.append((data2['title'],data2['uuid']))
    return result  

  #########################  информация о городе ############################
  ############### https://api.izi.travel/cities/ ############################
  def get_city_info(self,city_uuid):
    imgs=[]     
    url=URL_CITY_INFO;
    querystring = {"languages":"ru"}
    headers = {
	    "X-IZI-API-KEY": KEY_IZITRAVEL,    
	    "Accept":"application/izi-api-v1.8+json"
    }
    response = requests.request("GET", url+city_uuid, headers=headers, params=querystring)
    #print(response.text) 
    data1=json.loads(response.text)
    #print(data1)
    #print(data1['content'])
    for data2 in data1['content']:
      #print(data2['title'])
      #print(data2['desc'])
      #print("IMAGES:")
      try:
        for img in data2['images']:
          #{MEDIA_BASE_URL}/cities/{CITY_UUID}/{CITY_IMAGE_UUID}.jpg
          # https://media.izi.travel/
          #print(img['type']," ",img['uuid'])
          imgurl,ext=self.get_path_image("cities/"+data1['uuid'], img['uuid'], img['type'])
          #imgurl="https://media.izi.travel/cities/"+data1['uuid']+"/"+img['uuid']+".jpg"
          #print(imgurl) 
          dir="cities"
          if not os.path.exists(dir):
            os.mkdir("cities")        
          dir="cities/"+data1['uuid']
          print(dir)
          filename=self.save_file_media(dir,img['uuid'],imgurl,ext)
          #if not os.path.exists(dir):
          #  os.mkdir("cities/"+data1['uuid'])
          #filename="cities/"+data1['uuid']+"/"+img['uuid']+".jpg"
          #r = requests.get(imgurl, allow_redirects=True)
          #open(filename, 'wb').write(r.content) 
          imgs.append(filename)
      except:
        pass  
    return data2['title'],data2['desc'],imgs

  #####################   список объектов города  #############################
  ##########  https://api.izi.travel/cities/:uuid/children ####################
  def get_city_objects_list(self,city_uuid):
    objects=[]
    url=URL_CITY_OBJECTS_LIST
    querystring = {"languages":"ru"}
    headers = {
	    "X-IZI-API-KEY": KEY_IZITRAVEL,    
	    "Accept":"application/izi-api-v1.8+json"
    }
    response = requests.request("GET", url+city_uuid+"/children", headers=headers, params=querystring)
    #print(response.text) 
    data1=json.loads(response.text)
    for data in data1:
      #print(data['title'],"   ",data['type']," uuid",data['uuid'])
      obj_info=data['title']+";"+data['type']+";"+data['uuid']
      objects.append(obj_info)
    return objects    

  #################### кол-во объектов города ################################
  ########### https://api.izi.travel/cities/:uuid/children/count #############
  def get_city_objects_count(self,city_uuid):
    objects=[]
    url=URL_CITY_OBJECTS_COUNT
    querystring = {"languages":"ru"}
    headers = {
	    "X-IZI-API-KEY": KEY_IZITRAVEL,    
	    "Accept":"application/izi-api-v1.8+json"
    }
    response = requests.request("GET", url+city_uuid+"/children/count", headers=headers, params=querystring)
    #print(response.text) 
    data1=json.loads(response.text)
    return  response.text   

  ############# Информация об объекте (тип музей museum) #####################
  ######### https://api.izi.travel/mtgobjects/:uuid  #########################
  def get_objects_museum(self,object_uuid):
    audio=[]
    video=[]
    images=[]
    url=URL_MUSEUM_OBJECT
    querystring = {"languages":"ru","includes":"all","except":"translations,publisher,download,reviews,city,location,sponsors,route"}
    headers = {
	    "X-IZI-API-KEY": KEY_IZITRAVEL,    
	    "Accept":"application/izi-api-v1.8+json"
    }
    response = requests.request("GET", url+object_uuid, headers=headers, params=querystring)
    #print(response.text) 
    #data1=response.text
    data1=json.loads(response.text)
    for data2 in data1:
      content_provider_uuid=data2['content_provider']['uuid']
      for data3 in data2['content']:
        title=data3['title']
        desc=data3['desc']
        # audio
        try:
          print("data4['audio']=",data3['audio'])
          for data4 in data3['audio']:
            #print("data4['uuid']=",data4['uuid'])
            audiourl,ext=self.get_path_audio(content_provider_uuid,data4['uuid'])
            filename=self.save_file_media(content_provider_uuid,data4['uuid'],audiourl,ext)
            audio.append(filename)
        except:
          pass 
        # video
        try:
          for data4 in data3['video']:
            #print("data4['uuid']=",data4['uuid'])
            if data4['type']=='youtube':
              video.append(data4['URL'])
            elif data4['type']=='story':  
              videourl,ext=self.get_path_audio(content_provider_uuid,data4['uuid'])
              filename=self.save_file_media(content_provider_uuid,data4['uuid'],videourl,ext)
              video.append(filename)
        except:
          pass 
        # images
        try:
          for data4 in data3['images']:
            #print("data4['uuid']=",data4['uuid'])
            imgurl,ext=self.get_path_image(content_provider_uuid,data4['uuid'],data4['type'])
            filename=self.save_file_media(content_provider_uuid,data4['uuid'],imgurl,ext)
            images.append(filename)
        except:
          pass 
    #  #print(data['title'],"   ",data['type']," uuid",data['uuid'])
    #  obj_info=data['title']+";"+data['type']+";"+data['uuid']
    #  objects.append(obj_info)
    return title,desc,content_provider_uuid,audio,video,images    

  ############## Получить дочерние элементы #####################
  ###### https://api.izi.travel/mtgobjects/:uuid/children ######3
  def get_children_museum(self,object_uuid):      
      objects=[]
      url=URL_MUSEUM_CHILDREN
      querystring = {"languages":"ru","includes":"all","except":"translations,publisher,download,reviews,city,location,sponsors,route"}
      headers = {
	      "X-IZI-API-KEY": KEY_IZITRAVEL,    
	      "Accept":"application/izi-api-v1.8+json"
      }
      response = requests.request("GET", url+object_uuid+"/children", headers=headers, params=querystring)
      #print(response.text) 
      #print("ok")
      #data1=response.text
      data1=json.loads(response.text)
      for data2 in data1:
        obj_info=data2['title']+";"+data2['uuid']
        objects.append(obj_info) 
      return objects

  ###############  Получить дочерний элемент музея или тура #############
  ######### https://api.izi.travel/mtgobjects/:uuid  ####################
  def get_children(self,object_uuid):
    audio=[]
    video=[]
    images=[]
    url=URL_MUSEUM_CHILDREN_INSTANCE
    querystring = {"languages":"ru","includes":"all","except":"translations,publisher,download,reviews,city,location,sponsors,route"}
    headers = {
	    "X-IZI-API-KEY": KEY_IZITRAVEL,    
	    "Accept":"application/izi-api-v1.8+json"
    }
    response = requests.request("GET", url+object_uuid, headers=headers, params=querystring)
    #print(response.text) 
    #print("ok")
    data1=json.loads(response.text)
    for data2 in data1:
      content_provider_uuid=data2['content_provider']['uuid']
      for data3 in data2['content']:
        desc=data3['desc']
        # audio
        try:
          #print("data4['audio']=",data3['audio'])
          for data4 in data3['audio']:
            #print("data4['uuid']=",data4['uuid'])
            audiourl,ext=self.get_path_audio(content_provider_uuid,data4['uuid'])
            #print("audiourl=",audiourl)
            filename=self.save_file_media(content_provider_uuid,data4['uuid'],audiourl,ext)
            audio.append(filename)
        except:
          pass 
        # video
        try:
          for data4 in data3['video']:
            #print("data4['uuid']=",data4['uuid'])
            if data4['type']=='youtube':
               video.append(data4['URL'])
            elif data4['type']=='story':  
              videourl,ext=self.get_path_audio(content_provider_uuid,data4['uuid'])
              filename=self.save_file_media(content_provider_uuid,data4['uuid'],videourl,ext)
              video.append(filename)
        except:
          pass 
        # images
        try:
          #print("data4['images']=",data3['images'])
          for data4 in data3['images']:
            print("data4['uuid']=",data4['uuid'])
            imgurl,ext=self.get_path_image(content_provider_uuid,data4['uuid'],data4['type'])
            print("imgurl=",imgurl)
            filename=self.save_file_media(content_provider_uuid,data4['uuid'],imgurl,ext)
            images.append(filename)
        except:
          pass 
  
    return desc,content_provider_uuid,audio,video,images

    ############################### END #######################################