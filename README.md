# iziTravelBot

DAY 08 – Введение в анализ данных REST API
Задание

Найти любой бесплатный API в сети.
Написать класс взаимодействия с API, а в рамках класса методы взаимодействия с ним.
После реализации и проверки функциональности создать небольшой сервис на Flask или FastAPI, или Телеграм-бота. Нужно, чтобы каждый мог пользоваться функциональностью, которая заложена в сервис.
Запустить сервис на любом бесплатном веб-хостинге (например, Heroku).

Команда:

Виктор Петин – theodanl – Team lead
Сергей Москалев – hitmonch - Developer
Наталья Северенчук –moranhoo - Developer
Галина Климова - leonialu – Developer

GitHub location:
https://t.me/iziTavel01Bot
Краткое описание принципа работы:
Сервис выполнен в виде интерпретируемого .py файла, работающего в среде Python 3.10 VPS хостинга Heroku. 
Взаимодействие с основным интерфейсным сервисом Telegram, 
а также вспомогательными сервисами осуществляется с помощью публичного API izi.travelI https://api-docs.izi.travel/#apps-featured-content 
и библиотек Python - aiogram, requests, bleach, re.
Сервис предлагает пользователю ввести название города, который он хотел бы посетить (как в России, так и за ее пределами). 
Возможные варианты ввода предлагаются после введения первых трех букв. 
После выбора города сервис присылает фото основных видов города и его краткое описание. 
В дальнейшем предлагается возможность выбрать экскурсионный тур по городу или посещение музея, 
расположенного в выбранном городе (из списка). 
Выбранные туры снабжены описанием, фотографиями, а также звуковыми информационными треками, 
записанными на русском языке гостями и жителями выбранного города. 
После завершения выбранного тура сервис предлагает заново выбрать город для посещения.
