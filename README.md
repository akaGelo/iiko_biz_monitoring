

aws lambda функция для управленяи картинками

на вход принимает номер ревизии, id интеграции, id продукта, ссылку на кратинку

номер ревизии должен быть инкрементный, старые ревизии удаляются переодически отдельной функцией

##создание окружения
$ python3 -m venv env

##переключение
source env/bin/activate


##пример добавления зависимостей
pip install Pillow


##список функций
yc --folder-id=b1g3u49b145tps8pp86j  serverless function list 

# iiko_biz_monitoring
