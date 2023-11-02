Решение тестового задания на вакансию "Интегратор" в GreenData.
### dadata.ru
Вызов API-сервиса dadata.ru по стандартизации адреса и JMESPath запрос были реализованы двумя способами: 
* Использование Python и библиотеки [dadata-py](https://github.com/hflabs/dadata-py)
* прямой cURL-запрос + [JMESPath Playground](https://play.jmespath.org/)
##### Python
В dadataru.py реализован вызов API сайта для стандартизации адреса - функция `clean()`.
Далее из полученного json извлекается почтовый индекс адреса при помощи функции `search()` модуля jmespath. 
Значения токенов, адреса, проверяемого почтового индекса хранятся в .env
Далее проверяем на соответствие полученный почтовый индекс с индексом "614002" при помощи следующего условия (в случае совпадения выводим содержимое json): 
```
if postal_code != POSTAL_CODE_FILTER:  
    print("Запрос не прошёл по почтовому индексу!")  
else:  
    print(dadata_source)
```
##### cURL
Пример вызова API dadata.ru по стандартизации адреса (токены выдаются при регистрации на dadata.ru):
```
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Token 40e746cf35a6289a36bc348c84aa33b5c5548392" \
  -H "X-Secret: d98ff882a6b8acfb3c1a35e45591ea61f42e2a88" \
  -d '[ "мск сухонска 11/-89" ]' \
  https://cleaner.dadata.ru/api/v1/clean/address
```
Чтобы отфильтровать полученный результат по почтовому индексу "614002", воспользуемся сервисом JMESPath Playground. 
Для начала узнаем, какие адреса относятся к данному почтовому индексу. Один из таких примеров - г. Пермь, ул. Чернышевского, д 19. Получим json из cURL запроса (см. пример запроса выше) населённого пункта с пермским адресом и отфильтруем его по параметру `postal_code=='614002'`  - результат `true`. 
Если мы введём адрес, например, с другим городом, то результат будет `false`. Подробнее json и параметр фильтрации для Перми можно посмотреть [тут](https://play.jmespath.org/?u=9c83ce4a-05b6-4611-a650-bae2eae1ff08), для другого города [тут](https://play.jmespath.org/?u=18f9866d-3684-4506-ad73-8c8035298756).
Чтобы при совпадении почтового индекса выводить сами данные, необходимо прописать следующий фильтр: `to_array(@)[?postal_code== '614002'] | [0]`. Если индексы не совпадут, то будет выведен `null`, иначе получим следующий [результат](https://play.jmespath.org/?u=8b633f03-f12b-48e6-8758-36da2827f39e).
### Яндекс.Карты
Аналогично первому заданию реализовано два способа вызова API Яндекс.Карт: скрипт на python и прямой cURL-запрос. 
____
Для того, чтобы делать вызовы API Яндекс.Карт, необходимо получить токен сервиса [geocoder](https://yandex.ru/maps-api/products/geocoder-api?from=mapsapi%3F).
##### Python
Основной скрипт - yandex.py. Сначала из .evn/settings.py получаем значения API-токена и адреса, по которому будет осуществляться поиск (в нашем случае адрес - "Белинского, 31"), и далее по `https://geocode-maps.yandex.ru/1.x/` делаем запрос с этими параметрами:
```
response = requests.get(base_url, params={  
    "geocode": YANDEX_ADDRESS,  
    "apikey": YANDEX_API_KEY,  
    "format": "json",  
})
```
Выгрузка json/xml на python делается практически идентично - необходимо лишь в теле запроса поменять параметр `"format"` (`"json"` или `"xml"`).
Результат запроса в формате json получаем следующим образом - `response.json()`. В формате xml: парсим полученный xml и для читабельного вида приводим его к виду словаря с помощью библиотеки [xmltodict](https://pypi.org/project/xmltodict/) - `dict_data = xmltodict.parse(response.content)`.
##### cURL
cURL вызов API Яндекс.Карт с выгрузкой json:
```
curl --location 'https://geocode-maps.yandex.ru/1.x/?apikey=b8c1d9b0-966f-4142-9682-4762c32d0cc1&geocode=%D0%91%D0%B5%D0%BB%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE%2C%2031&format=json' \
--header 'Cookie: _yasc=PTcMdzsI8H9IbQxZd+LzMCKrYBz6gE31dJ5ESBT2r9Ef1k8E2XrPOXX57vYQp6gTXA==; i=3925pwuXBQgd7RjZng9FgoUKT7ZBcxOElj2T0nOebcks4EmzAqD3OQUMAfpcuv/XLAn0WDLbcJaWyssxfuUKU9ECitg=; yandexuid=1520248341698764173'
```
Далее в JMESPath Playground загружаем полученный json и отфильтруем его по городу Пермь. Код фильтра: 
```
response.GeoObjectCollection.featureMember[*].GeoObject.*.GeocoderMetaData[?AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName=='Пермь'] | [0]
```
Посмотреть результат фильтрации и json можно [тут](https://play.jmespath.org/?u=711ef1a9-98cd-4e53-b16a-96c50515ceb0).
___
cURL вызов API Яндекс.Карт с выгрузкой xml:
```
curl --location 'https://geocode-maps.yandex.ru/1.x/?apikey=b8c1d9b0-966f-4142-9682-4762c32d0cc1&geocode=%D0%91%D0%B5%D0%BB%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B3%D0%BE%2C%2031&format=xml' \
--header 'Cookie: _yasc=PTcMdzsI8H9IbQxZd+LzMCKrYBz6gE31dJ5ESBT2r9Ef1k8E2XrPOXX57vYQp6gTXA==; i=3925pwuXBQgd7RjZng9FgoUKT7ZBcxOElj2T0nOebcks4EmzAqD3OQUMAfpcuv/XLAn0WDLbcJaWyssxfuUKU9ECitg=; yandexuid=1520248341698764173'
```
Далее с помощью [Fonto XPath Playground](https://xpath.playground.fontoxml.com/) пропишем XQuery запрос, который вернет массив всех найденных адресов в формате «Страна, Город, Улица, Дом». XQuery запрос:
```
for $geoObject in /ymaps/GeoObjectCollection/*:featureMember/GeoObject/*:metaDataProperty/*:GeocoderMetaData
let $country := $geoObject/*:Address/*:Component[*:kind='country']/*:name
let $city := $geoObject/*:Address/*:Component[*:kind='locality']/*:name
let $street := $geoObject/*:Address/*:Component[*:kind='street']/*:name
let $house := $geoObject/*:Address/*:Component[*:kind='house']/*:name
return string-join(($country, $city, $street, $house), ', ')
```
Результат форматирования xml можно посмотреть [тут](https://t.ly/_S5U3).
### SQL
С помощью [Erwin](https://www.erwin.com/) была спроектирована БД по методологии IDEF1X для задачи ведения расписания занятий в школе. 
Схему можно посмотреть во вложенном в репозиторий png-файле (school_table.png).
___
##### Какие таблицы были созданы?
1. **Класс** - хранит информацию о классе. Атрибуты: 
   * class_id (PK) - уникальный идентификатор класса
   * class_name - название класса (например, "1А")
   * class_type - предметный "уклон" класса (например, физмат и т.п.)
   * classroom_teacher (FK) - id классного руководителя данного класса
     
2. **Преподаватель** - хранит информацию о преподавателе. Атрибуты: 
   * teacher_id (PK) - уникальный идентификатор преподавателя
   * last_name - фамилия преподавателя
   * first_name - имя преподавателя
     
3. **Ученик** - хранит информации об ученике. Атрибуты: 
   * student_id (PK) - уникальный идентификатор ученика
   * class_id (FK) - id класса, в котором учится данный ученик
   *  last_name - фамилия ученика
   * first_name - имя ученика
   * birt_date - дата рождения ученика
     
4. **Предмет** - хранит информацию об учебной дисциплине. Атрибуты:
   * subjet_id (PK) - уникальный идентификатор учебной дисциплины
   * subjet_name - название предмета
     
5. **Дата/время урока** - хранит информацию о времени проведения занятий. Атрибуты:
   * dateTime_id (PK) - уникальный идентификатор объекта времени
   * lesson_date - дата урока
   * weekday_name - наименование дня недели
   * lesson_start_time - время начала урока
   * lesson_start_time - время окончания урока
     
6. **Расписание** - хранит информацию о школьном расписании. Атрибуты:
   * timetable_id (PK) - уникальный идентификатор расписания
   * class_id (FK) - id класса, у которого назначено занятие
   * teacher_id (FK) - id учителя, у которого назначено проведение занятия
   * subjet_id - id проводимого занятия (учебной дисциплины)
   * dateTime_id - id временного отрезка/даты, в которое проводится занятие
##### Типы данных атрибутов 
Для атрибутов-id использовался тип *INTEGER*.
Для атрибута lesson_date использовался тип *DATA*, для lesson_start_time и lesson_start_time - *TIMESTAMP* (он очень удобен для представления времени в формате ЧЧ:ММ).
Все остальные атрибуты содержали в себе текстовую информацию, выбранный тип данных - *NVARCHAR*.
___
Далее физическая модель БД была выгружена из Erwin в Access для дальнейшего заполнения данными и написания запросов.
##### Запрос №1
Таблица "Дата/время урока" была переименована в "Время".
SQL-запрос, который вернет все занятия «1А» класса по математике в понедельник, в порядке следования предметов по времени:
```
SELECT Класс.class_name, Предмет.subject_name, Время.lesson_start_time, Время.lesson_finish_time
FROM (((Расписание
INNER JOIN Класс ON Класс.class_id = Расписание.class_id)
INNER JOIN Предмет ON Предмет.subject_id = Расписание.subject_id)
INNER JOIN Время ON Время.dateTime_id = Расписание.dateTime_id)
WHERE Класс.class_name = "1А" AND Предмет.subject_name = "Математика" AND Время.weekday_name = "Понедельник"
ORDER BY Время.lesson_start_time;
```
##### Запрос №2
SQL-запрос, подсчитывающий количество уроков для каждого класса в каждый день недели, в порядке уменьшения кол-ва уроков:
```
SELECT Класс.class_name, Время.weekday_name, COUNT(*) as lesson_count
FROM ((Расписание
INNER JOIN Класс ON Класс.class_id = Расписание.class_id)
INNER JOIN Время ON Время.dateTime_id = Расписание.dateTime_id)
GROUP BY Класс.class_name, Время.weekday_name
ORDER BY lesson_count DESC;
```
