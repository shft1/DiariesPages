# DiariesPages - Платформа для ведения дневников

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/4c4c038c-f092-41fc-af2e-ea4cde76161f" />


---

### Описание:  
Веб-приложение на Django с системой публикаций, комментариев и управлением контентом. Реализована аутентификация, пагинация, загрузка изображений к постам и отложенные публикации. Использует Django ORM для SQLite, Django шаблонизатор для страниц и view-функции для их обработки. Настроен бэкенд для «отправки» писем (сохранение в sent_emails/), CSRF-токен для безопасности, дамп (db.json) БД для наполнения сайта данными.

---

### Стек технологий:  
Python, Django, Django Templates, Django ORM, Django Test, SQLite

---

### Инструкция по развертыванию:
**Клонируйте репозиторий:**

```
git clone git@github.com:shft1/DiariesPages.git
```

**Cоздайте и активируйте виртуальное окружение:**

```
python3 -m venv venv
```

* _Если у вас Linux/macOS_

    ```
    source venv/bin/activate
    ```
* _Если у вас Windows_

    ```
    source venv/scripts/activate
    ```

**Установите зависимости из файла requirements.txt:**

```
pip install -r requirements.txt
```

**Запустите тесты, для проверки корректности работы приложения**
```
pytest
```
_Если 25 тестов успешно пройдены, то приложение работает_

<img width="1138" alt="image" src="https://github.com/user-attachments/assets/82f0d151-15be-4982-a119-ffde38e836b0" />


**В папке `blogicum` запустите приложение DiariesPages на локальном хосте**
```
python manage.py runserver
```

---

### Примеры использования:  

**_Создание поста_**

<img width="1092" alt="image" src="https://github.com/user-attachments/assets/2c351845-dd33-4989-8865-1b51b4073ec0" />

**_Профиль пользователя_**

<img width="1069" alt="image" src="https://github.com/user-attachments/assets/7d7c6e45-c8bd-40e4-b045-406b7690b474" />

**_Форма регистрации_**

<img width="1195" alt="image" src="https://github.com/user-attachments/assets/423d5ee3-aec8-4d0d-86d4-477106b9275f" />


