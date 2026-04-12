import os
import pytest
import allure
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

from Diplom.Pages.api_vk_page import ApiVkPage


load_dotenv()
api = ApiVkPage()


@allure.title(
    "Тест глобального поиска через search.getHints (позитивный сценарий)")
@allure.description(
    "Проверяет успешный глобальный поиск по запросу через API ВКонтакте")
@allure.feature("Глобальный поиск")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
def test_get_global_search() -> None:
    with allure.step("Подготовка параметров запроса"):
        q: Optional[str] = os.getenv("NAME")
        access_token: Optional[str] = os.getenv("ACCESS_TOKEN")

    with allure.step(f"Выполнение глобального поиска с запросом: {q}"):
        resp: Dict[str, Any]
        status_code: int
        resp, status_code = api.global_search(q, access_token)

    with allure.step("Проверка HTTP-статуса 200"):
        assert status_code == 200, \
            f"Ожидался код 200, получен {status_code}"

    with allure.step("Проверка наличия ключа 'response' в ответе"):
        assert 'response' in resp, \
            "В ответе отсутствует ключ 'response'"
        response: Dict[str, Any] = resp['response']

    with allure.step("Проверка наличия и значения поля 'count'"):
        assert 'count' in response, \
            "В 'response' отсутствует ключ 'count'"
        count: int = response['count']
        assert count > 0, f"Не найдено элементов, count = {count}"

    with allure.step("Проверка наличия поля 'items' и его типа"):
        assert 'items' in response, \
            "В 'response' отсутствует ключ 'items'"
        items: List[Any] = response['items']
        assert isinstance(items, list), \
            "Поле 'items' должно быть списком (массивом)"

    with allure.step(
            "Проверка соответствия длины списка 'items' значению 'count'"):
        assert len(items) == count, \
            (f"Длина списка 'items' ("
             f"{len(items)}) не совпадает с count ({count})")


@allure.title("Тест глобального поиска с неверным"
              "токеном (негативный сценарий)")
@allure.description(
    "Проверяет обработку ошибки авторизации"
    "при использовании неверного токена доступа")
@allure.feature("Глобальный поиск")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
def test_get_global_search_negative() -> None:
    with allure.step("Подготовка параметров с некорректным токеном"):
        q: Optional[str] = os.getenv("NAME")
        access_token: Optional[str] = os.getenv("MISS_ACCESS_TOKEN")

    with allure.step(
            f"Выполнение поиска с некорректным токеном: {access_token}"):
        resp: Dict[str, Any]
        status_code: int
        resp, status_code = api.global_search(q, access_token)

    with allure.step(
            "Проверка HTTP-статуса 200 ("
            "API возвращает 200 даже при ошибках авторизации)"):
        assert status_code == 200, \
            f"Ожидался код 200, получен {status_code}"

    with allure.step("Парсинг ответа и извлечение данных об ошибке"):
        response_data: Dict[str, Any] = resp
        error_msg: str = response_data.get("error", {}).get("error_msg", "")
        error_code: int = response_data.get("error", {}).get("error_code", 0)

    with allure.step("Проверка наличия секции 'error' в ответе"):
        assert "error" in response_data, \
            "В ответе отсутствует секция 'error'"

    with allure.step("Проверка кода ошибки 5 (неверная авторизация)"):
        assert error_code == 5, \
            f"Ожидался код ошибки 5, но получен: {error_code}"

    with allure.step("Проверка сообщения об ошибке авторизации"):
        assert "User authorization failed" in error_msg, \
            f"Неверная ошибка: {error_msg}"
        assert "invalid access_token" in error_msg, \
            "В сообщении об ошибке отсутствует указание на неверный токен"


@allure.title("Тест поиска друзей и получения ID указанного пользователя")
@allure.description(
    "Проверяет поиск друзей по запросу и корректное"
    "извлечение ID пользователя из результатов")
@allure.feature("Поиск друзей")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
def test_get_list_id_friend_search() -> None:
    with allure.step("Чтение номера пользователя из .env (FRIEND_NUM)"):
        friend_num_str: str = os.getenv("FRIEND_NUM", "6")
        friend_num: int = int(friend_num_str)

    with allure.step("Подготовка параметров запроса (поиск всех друзей)"):
        q: Optional[str] = None

    with allure.step("Выполнение поиска друзей"):
        resp: Dict[str, Any]
        status_code: int
        us_id: int
        resp, status_code, us_id = api.list_id_friend_search(q)

    with allure.step("Проверка HTTP-статуса 200"):
        assert status_code == 200, \
            f"Ожидался код 200, получен {status_code}"

    with allure.step("Проверка наличия ключа 'response' в ответе"):
        assert 'response' in resp, \
            "В ответе отсутствует ключ 'response'"
        response: Dict[str, Any] = resp['response']

    with allure.step("Проверка наличия и значения поля 'count'"):
        assert 'count' in response, \
            "В 'response' отсутствует ключ 'count'"
        count: int = response['count']
        assert count > 0, \
            f"Не найдено элементов, count = {count}"

    with allure.step("Проверка наличия поля 'items' и его типа"):
        assert 'items' in response, \
            "В 'response' отсутствует ключ 'items'"
        items: List[Dict[str, Any]] = response['items']
        assert isinstance(items, list), \
            "Поле 'items' должно быть списком (массивом)"

    with allure.step(
            f"Проверка наличия минимум {friend_num + 1} элементов в списке"):
        assert len(items) >= friend_num + 1, \
            (f"В списке меньше {friend_num + 1} элементов, "
             f"невозможно получить элемент с индексом {friend_num}")

    with allure.step(
            f"Извлечение данных пользователя №"
            f"{friend_num + 1} (индекс {friend_num})"):
        item_by_index: Dict[str, Any] = items[friend_num]
        user_id: int = item_by_index['id']
        first_name: str = item_by_index['first_name']
        last_name: str = item_by_index['last_name']

    with allure.step(
            "Проверка совпадения ID пользователя из ответа и сохранённого ID"):
        assert us_id == user_id

    with allure.step("Вывод данных найденного пользователя"):
        print(f"ID: {user_id}, Имя: {first_name}, Фамилия: {last_name}")


@allure.title("Тест создания чата с найденным пользователем")
@allure.description(
    "Проверяет создание нового чата через API"
    "ВКонтакте и корректность возвращаемых данных")
@allure.feature("Управление чатами")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
def test_get_create_chat_friend() -> None:
    with allure.step("Подготовка названия чата"):
        title: Optional[str] = os.getenv("CHAT_NAME")

    with allure.step(f"Создание чата с названием: {title}"):
        resp: Dict[str, Any]
        status_code: int
        chat_id: int
        peer_id: int
        resp, status_code, chat_id, peer_id = api.create_chat_friend(title)

    with allure.step("Проверка HTTP‑статуса 200"):
        assert status_code == 200, \
            f"Ожидался код 200, получен {status_code}"

    with allure.step("Проверка наличия ключа 'response' в ответе"):
        assert 'response' in resp, \
            "В ответе отсутствует ключ 'response'"
        response: Dict[str, Any] = resp['response']

    with allure.step("Проверка типа ответа 'response' — должен быть словарем"):
        assert isinstance(response, dict), \
            "Значение по ключу 'response' не является словарем"

    with allure.step(
            "Проверка наличия параметров"
            "'chat_id' и 'peer_ids' в теле ответа"):
        assert 'chat_id' in response, \
            "В ответе отсутствует параметр 'chat_id'"
        assert 'peer_ids' in response, \
            "В ответе отсутствует параметр 'peer_ids'"

    with allure.step("Сохранение значений chat_id и peer_ids в переменные"):
        chat_id: int = response['chat_id']
        peer_ids_list: List[int] = response['peer_ids']

    with allure.step("Проверка корректности chat_id (тип и значение)"):
        assert isinstance(chat_id, int), \
            "chat_id должен быть целым числом"
        assert chat_id > 0, \
            "chat_id должен быть положительным числом"

    with allure.step("Проверка корректности peer_ids (тип и не пустота)"):
        assert isinstance(peer_ids_list, list), \
            "peer_ids должен быть списком"
        assert len(peer_ids_list) > 0, \
            "peer_ids не должен быть пустым списком"

    with allure.step("Извлечение первого peer_id из списка"):
        peer_id: int = peer_ids_list[0]

    with allure.step("Проверка корректности первого peer_id (тип и значение)"):
        assert isinstance(peer_id, int), \
            "peer_id должен быть целым числом"
        assert peer_id > 0, \
            "peer_id должен быть положительным числом"

    with allure.step("Вывод полученных данных для отладки"):
        print(f"Получен chat_id: {chat_id}")
        print(f"Получен peer_id: {peer_id}")


@allure.title("Тест удаления чата для всех участников")
@allure.description(
    "Проверяет удаление чата через API ВКонтакте и успешность операции")
@allure.feature("Управление чатами")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
def test_get_delete_chat() -> None:
    with allure.step("Инициирование удаления чата"):
        status_code: int
        resp: Dict[str, Any]
        status_code, resp = api.delete_chat()  # Распаковываем кортеж

    with allure.step("Проверка HTTP‑статуса 200"):
        assert status_code == 200, \
            f"HTTP статус не 200: {status_code}"

    with allure.step("Проверка успешного выполнения операции (response == 1)"):
        assert resp['response'] == 1, \
            f"API вернул ошибку: {resp}"

    with allure.step("Подтверждение успешного удаления чата"):
        print("Чат успешно удалён!")
