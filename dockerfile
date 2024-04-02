# Используем базовый образ Python
FROM python:3.8

# Устанавливаем переменную среды PYTHONUNBUFFERED, чтобы вывод stdout и stderr немедленно отправлялся в поток вывода без буферизации
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в /code
WORKDIR /code

# Копируем файл requirements.txt в рабочую директорию контейнера
COPY requirements.txt /code/

# Устанавливаем зависимости Python из requirements.txt
RUN pip install -r requirements.txt

# Установка libgl для Linux
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Копируем все файлы из текущего каталога (то есть код проекта) в рабочую директорию контейнера
COPY . /code/

# Выполняем миграции и собираем статические файлы
RUN python ./runtext_generator/manage.py migrate
RUN python ./runtext_generator/manage.py collectstatic --noinput

# Открываем порт 7000
EXPOSE 7000

# Запускаем сервер Django при старте контейнера
CMD ["python", "./runtext_generator/manage.py", "runserver", "0.0.0.0:7000"]