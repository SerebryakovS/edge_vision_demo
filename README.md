# edge_vision_demo


### sensor.py
###### Компонент, генерирующий данные, на основе которых контроллер принимает решение. Всего 8 сенсоров, каждый генерирует 300 сообщений в секунду.
В конфигурационном файле(файл config, в корне проекта), задается частота(раз в секунду) опроса псевдо-сенсоров - SENSOR_FREQUENCY(согласно заданию равна 300), а также количество сенсоров - SENSORS_NUMBER(согласно заданию равно 8). Чтение/запись организованы через файлы(так больше на чтение с устройства походит), директория для хранения которых определена переменной SENSORS_FOLDER конфигурационного файла. Для проверки работоспособности, из первого терминала:
```
$ ./sensor.py seconds_to_run
```
где seconds_to_run - это рабочее время от начала считывания. Далее, из второго терминала(начинаем читать):
```
$ while [[ 1 ]]; do cat SENSORS_FOLDER/sensor_[1..SENSORS_NUMBER];done
```
### manipulator.py
###### Компонент, который принимает сигналы по TCP соединению и выводит их в консоль/логи для демонстрации.
В конигурационном файле задается TCP порт - MANIPULATOR_PORT, на котором открывается сокет для принятия управляющих сообщений от controller-a. Принятые данные выводятся в терминал и лог-файл(manipulator.log). Для проверки работоспособности, из первого терминала:
```
$ ./manipulator.py 
```
Далее, из второго терминала(отправляем TCP сообщение по заданному в конфиге порту):
```
$ sudo apt-get install socat
$ echo "very important information" | socat - TCP:localhost:MANIPULATOR_PORT
```
### third_party_server.py
###### Веб-сервер с простым веб-интерфейсом (кнопка и окно вывода), который по нажатию кнопки отображает текущий статус контроллера.
В конигурационном файле задается порт, на котором будет запущен веб-сервер - WEB_SERVISE_PORT. Для проверки работоспособности, из первого терминала:
```
$ ./third_party_server.py
```
Далее, в адресной строке браузера получаем веб-страницу:
```
localhost:WEB_SERVISE_PORT
```
По нажанию кнопки CHECK, сервер высылает текущее состояние контроллера и отображает его в текстовое поле выше. 
### controller.py
###### Компонент, который по TCP соединению управляет манипулятором, на базе данных от сенсоров. Обработка данных с сенсоров происходит параллельно/асинхронно, однако важно обрабатывать сообщения в 5 сек интервалы. Т.е. каждые 5 секунд принимается решение об управляющем сигнале для манипулятора. Outdated информация не должна приниматься во внимание при принятии решения. Дополнительно контроллер должен иметь API для передачи статуса на внешний сервер.
Outdated информация исключена по-умолчанию(любая считанная информация актуальна). Считывание с датчиков производится асинхронно. В конфигурационном файле определена переменная DECISION_TIME(равная 5 сек, согласно заданию), которая отвечает за интервалы принятия решения и отправки последнего к манипулятору и веб-серверу. Для проверки работоспособности достаточно запустить скрит, отвечающий за запуск всего вышеописанного.
```
$ ./run.sh
```
Форматы передаваемых сообщений составлены согласно представленным в задании шаблонам. Для сборки/запуска Docker-контейнера:
```
$ docker build -t ev_demo .
$ docker run --rm --name ev_demo_dock --network="host" ev_demo
```


