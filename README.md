# Дипломный проект: Автоматизация тестирования VK API и UI

## Описание проекта

### Проект по автоматизации тестирования социальной сети VK с использованием:

- Python — язык программирования;
- PyTest — фреймворк для тестирования;
- Selenium WebDriver — для UI‑тестов;
- Requests — для API‑тестов;
- Allure — для отчётов.

## Требования

- Python 3.14+;
- Google Chrome (последняя версия);
- Git.

## Ссылка на финальный проект

### GitHub репозиторий:

 - Ссылка : https://github.com/CJIOBOCJIAB/Diplom
   - Ветка с дипломным проектом: main

### Установка и настройка

##### Клонирование репозитория

    ```bash
    git clone <URL-репозитория>
    cd Diplom.

##### Создание виртуального окружения

    ```bash
    python -m venv venv

##### Активация виртуального окружения
    Windows:

    ```bash
    venv\Scripts\activate

##### Установка зависимостей
    ```bash
    pip install -r requirements.txt
* Рекомендуемые
  - allure-pytest==2.15.3
  - allure-python-commons==2.15.3
  - python-dotenv==1.2.1
  - requests==2.32.5
  - selenium==4.40.0
  - typing_extensions==4.15.0
  - pytest==9.0.2

## Структура проекта
    Diplom/
    ├── .venv/                  # Bиртуальноe окружениe
    ├── allure-results/         # Файлы allure
    ├── Pages/
    │   ├── __init__.py         # Инициализация пакета тестов
    │   ├── api_vk_page.py      # Класс для работы с API VK
    │   └── ui_vk_page.py       # Класс для работы с UI VK
    ├── Tests/
    │   ├── __init__.py         # Инициализация пакета тестов
    │   ├── test_api.py         # API‑тесты (5 шт.)
    │   └──  test_ui.py         # UI‑тесты (5 шт.)
    ├── .env                    # Пример переменных окружения
    ├── .gitignore              # Игнорируемые файлы
    ├── __init__.py             # Инициализация пакета тестов
    ├── conftest.py             # Фикстуры для тестов 
    ├── pytest.ini              # Конфигурация pytest
    ├── README.md               # Документация
    └── requirements.txt        # Зависимости проекта


## Что автоматизировано

### API‑тесты (5 тестов):

- `test_get_global_search` — выполнение глобального поиска в VK;
- `test_get_global_search_negative` — проверка глобального поиска с негативными сценариями;
- `test_get_list_id_friend_search` — поиск друга по ID и получение данных (ID, имя, фамилия);
- `test_get_create_chat_friend` — создание чата с другом, получение `chat_id` и `peer_id`;
- `test_get_delete_chat` — удаление созданного чата.

### UI‑тесты (5 тестов):

- `test_ui_audio` — взаимодействие с разделом аудиозаписей (переход в раздел, выбор новых песен, проверка количества аудиозаписей);
- `test_ui_video` — взаимодействие с разделом видео (переход в раздел видео, выбор подкатегории);
- `test_ui_groups` — работа с разделами групп (переход в группы, выбор категории «спорт», ввод поискового запроса, выполнение поиска);
- `test_ui_apps` — проверка раздела приложений (переход в приложения, верификация корректности URL: `https://vk.com/services`);
- `test_ui_games` — проверка раздела игр (переход в игры, верификация корректности URL: `https://vk.com/games`).

## Настройка переменных окружения
#### Скопируйте .env.example в .env.

 - Поиск app_id и access_token:
   * Зайдите в свой аккаунт в VK
   * Выйдите из аккаунта (на страницу аутентификации)
   * Откройте devtools(F12)
   * Очистите Network log
   * Нажмите войти в аккаунт
   * Из запросов ( {!}?act=connect_auth_saved_users ) и ( {!}?act=web_token ).
          Fetch/XHR — Payload — From Data — app_id  и access_token (копируем значения).
   

- Перед запуском заполните необходимые значения:

  * 
          .env
          - CLIENT_ID=ваш_app_id
          - NAME=имя_и_фамилия_пользователя
          - CHAT_NAME=название_чата
          - ACCESS_TOKEN=ваш_access_token
          - FRIEND_NUM=номер_друга_в_списке(на странице "Друзья")
          - UI_BASE_URL=https://vk.com/профиль_пользователя
          - GROUPS_NAME=наименование группы

## Команды для запуска тестов
##### Все тесты (UI + API)

    ```bash
    pytest -v

##### Только API‑тесты
    
    ```bash
    pytest -m api -v

##### Только UI‑тесты
    
    ```bash
    pytest -m ui -v

##### Запуск с Allure‑отчётом
    
    ```bash
    pytest --alluredir=allure-results -v
    allure serve allure-results

##### Параллельный запуск тестов
    
    ```bash
    pytest -n auto -v

##### Запуск конкретного тестового файла
    
    ```bash
    pytest Tests/test_api.py -v
    pytest Tests/test_ui.py -v

##### Запуск конкретного теста по имени
    
    ```bash
    pytest -k "test_vk_api_request" -v

## Результаты выполнения тестов

### API‑тесты

- `test_api.py::test_get_global_search` — **PASSED**
- `test_api.py::test_get_global_search_negative` — **PASSED**
- `test_api.py::test_get_list_id_friend_search`
  - Результат: ID: 267329400, Имя: Радианец, Фамилия: Борски
  - Статус: **PASSED**
- `test_api.py::test_get_create_chat_friend`
  - Получен `chat_id`: 184
  - Получен `peer_id`: 12517647
  - Статус: **PASSED**
- `test_api.py::test_get_delete_chat`
  - Сообщение: Чат успешно удалён!
  - Статус: **PASSED**

### UI‑тесты

- `test_ui.py::test_ui_audio`
  - Клик `audio` выполнен
  - Клик `new_songs` выполнен
  - Найдено 12 аудиозаписей
  - Статус: **PASSED**
- `test_ui.py::test_ui_video`
  - Клик `video` выполнен
  - Клик `child` выполнен
  - Статус: **PASSED**
- `test_ui.py::test_ui_groups`
  - Клик `groups` выполнен
  - Клик `sport` выполнен
  - Текст введён в поле поиска
  - Клик `button` выполнен
  - Статус: **PASSED**
- `test_ui.py::test_ui_apps`
  - Клик `apps` выполнен
  - URL соответствует ожидаемому: `https://vk.com/services`
  - Статус: **PASSED**
- `test_ui.py::test_ui_games`
  - Клик `games` выполнен
  - URL соответствует ожидаемому: `https://vk.com/games`
  - Статус: **PASSED**

---

## Итоговая статистика

| Тип тестов | Количество тестов | Успешно выполнено |
|----------|----------------|----------------|
| API‑тесты | 5 | 5 (100 %) |
| UI‑тесты | 5 | 5 (100 %) |
| **Всего** | **10** | **10 (100 %)** |
Все тесты успешно пройдены.

### Пример отчёта Allure
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8c18dfac-5f53-418d-bf5b-9f366fdc6380" />
На скриншоте видно:
- Круговая диаграмма **STATUS** с 100% успешных тестов.
- График **SEVERITY**, показывающий распределение по критичности.
- Статистика по длительности выполнения (**DURATION**).

## Отчёты
 - После запуска тестов с Allure отчёт будет доступен по адресу: http://localhost:63342

## Автор
### Борисов Илья Васильевич
 - Дипломный проект по автоматизации тестирования VK
 - тел. +7 921 912 43 73
 - email: 6orisov.i@gmail.com

## Дата
 - 9 Апреля 2026 г.
