# Проект YaMDb

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

Яндекс Практикум. Спринт 10. Итоговый проект. API для YaMDb.

## Описание

Проект YaMDb собирает отзывы `Review` пользователей на произведения `Title`. Произведения делятся на категории: `Книги`, `Фильмы`, `Музыка`. Список категорий `Category` может быть расширен. Сами произведения в YaMDb не хранятся. В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор. Пользователи оставляют к произведениям текстовые отзывы `Review` и выставляют произведению рейтинг.

## Установка

1. Клонировать репозиторий:

   ```python
   git clone https://github.com/egorcoders/api_yamdb.git
   ```

2. Перейти в папку с проектом:

   ```python
   cd api_yamdb/
   ```

3. Установить виртуальное окружение для проекта:

   ```python
   python -m venv venv
   ```

4. Активировать виртуальное окружение для проекта:

   ```python
   # для OS Lunix и MacOS
   source venv/bin/activate

   # для OS Windows
   source venv/Scripts/activate
   ```

5. Установить зависимости:

   ```python
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Выполнить миграции на уровне проекта:

   ```python
   cd yatube
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

7. Создать файл .env с переменными:

   - SOCIAL_AUTH_VK_OAUTH2_KEY
   - SOCIAL_AUTH_VK_OAUTH2_SECRET
   - EMAIL_HOST_USER
   - EMAIL_HOST_PASSWORD

8. Запустить проект:

   `python manage.py runserver`

## Документация

`http://127.0.0.1:8000/redoc/`
