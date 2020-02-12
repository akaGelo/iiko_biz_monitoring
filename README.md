## Мониторинг соединения iiko.biz и сервера iiko

### Принцип работы 
Каждый n секунд заупскается функция из main.py
 * авторизируется в iiko biz
 * получает номенклатуру
 * производит вызов метоа orders/checkCreate с заказом из одной позиции без модификаторов на доставку по адресу Ленина 1
    * если ответ содержит {'problems':null} проверка считается успешной и возвращает HTTP 200
    * если ответ **не** содержит {'problems':null} проверка считается неудачной и возвращает HTTP 500
    

Статус отображается в первой строке вывода:

**success:** - локальныйсервер iiko проверил заказ

**fail:** - неудалось проверить заказ. причина в поле  *server response*

 
    
### Проверка работы
Ответ адаптирован для отображения в браузере
    
Для примера фукнция развернута в яндекс облаке. В url установлены данные от публичной песочницы iiko 

https://functions.yandexcloud.net/d4ek8olulus9g8e6vcjg?login=demoDelivery&password=PI1yFaKFCGvvJKi&org_id=e464c693-4a57-11e5-80c1-d8d385655247

| Параметр  | Описание |
| ------------- | ------------- |
| login  | логин учетной записи iiko.biz с доступом к iiko delivery  api |
| password  | пароль учетной записи iiko.biz с доступом к iiko delivery  api|
| org_id | id организации, в которую будут отправляться проверки заказов |


### Использование
1) Развернуть функцию  в любом совместимом окружении (яндекс облако, aws lambda  и тд)
2) Обращатся по url функции из системы  мониторинга или отркыть в браузере  для наблюдения вручную

 




