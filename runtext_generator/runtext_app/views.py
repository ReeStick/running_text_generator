from django.http import HttpResponse
import cv2
import numpy as np
import os
from django.views.decorators.http import require_http_methods
import json
from .models import RequestLog  # Импортируем созданную модель

def generate_running_text_video(request):
    runtext = request.GET.get('runtext', '')  # Получаем текст из параметра runtext, если он передан, иначе пустая строка

    # Сохранение запроса в базе данных
    request_log = RequestLog.objects.create(
        method=request.method,
        path=request.path,
        body=request.body.decode('utf-8') if request.body else None
    )

    # Настройки видео
    width = 100
    height = 100
    fps = 24
    seconds = 3

    # Шрифт и его параметры
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 1
    font_thickness = 2

    # Рассчитываем ширину текста и положение начальной точки
    text_width, _ = cv2.getTextSize(runtext, font, font_scale, font_thickness)[0]
    text_x = width

    # Создание кадров для видео
    frames = []
    for i in range(fps * seconds):
        # Создаем пустой кадр
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame.fill(255)  # Заливаем его белым цветом
        
        # Определяем текущую позицию текста
        text_x -= int(text_width / (fps * seconds / 1.25)) # Видео немного ускорено для корректного отображения текста
        
        # Если текст вышел за пределы кадра, возвращаем его в начало
        if text_x < -text_width:
            text_x = width
        
        # Рисуем текст на кадре
        cv2.putText(frame, runtext, (text_x, int(height/2)), font, font_scale, (0, 0, 0), font_thickness)
        
        # Добавляем кадр в список
        frames.append(frame)

    # Создаем временное видео
    temp_video_path = 'temp_video.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()

    # Открываем временное видео и считываем его в бинарном режиме
    with open(temp_video_path, 'rb') as video_file:
        video_content = video_file.read()

    # Удаляем временное видео
    os.remove(temp_video_path)

    # Отправляем видео как HTTP-ответ с заголовком Content-Disposition
    response = HttpResponse(video_content, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename="running_text_video.mp4"'
    return response

@require_http_methods(["GET"])  # Ограничиваем этот представление только для GET запросов
def log_request(request):
    # Получаем аргументы GET запроса
    get_arguments = dict(request.GET)

    # Сохраняем лог запроса
    log_entry = RequestLog.objects.create(
        method=request.method,
        path=request.path,
        get_arguments=json.dumps(get_arguments),  # Преобразуем аргументы GET в строку JSON для сохранения в базе данных
        # Другие поля, которые вы хотите сохранить, например, IP адрес, заголовки и т.д.
    )

    # Отправляем ответ клиенту
    return HttpResponse("Request logged successfully")