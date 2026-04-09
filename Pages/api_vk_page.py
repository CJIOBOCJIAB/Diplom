import os
import allure
import requests
from typing import Tuple, Dict, Optional

from dotenv import load_dotenv


load_dotenv()


class ApiVkPage:
    def __init__(self) -> None:
        """
        Инициализирует экземпляр класса,
        загружая параметры из переменных окружения.
        """
        self.access_token: Optional[str] = os.getenv("ACCESS_TOKEN")
        self.base_url: Optional[str] = os.getenv("API_BASE_URL")
        self.api_version: Optional[str] = os.getenv("V")
        self.client_id: Optional[str] = os.getenv("CLIENT_ID")
        self.permissions: Optional[str] = os.getenv("PERMISSIONS")
        self.device_id: Optional[str] = os.getenv("DEVICE_ID")
        self.user_id: Optional[int] = None
        self.chat_id: Optional[int] = None
        self.peer_id: Optional[int] = None

    @allure.step("Выполнение глобального поиска через search.getHints")
    def global_search(self, q: str, access_token: str) -> Tuple[Dict, int]:
        """
        Выполняет глобальный поиск по запросу
        через метод search.getHints API ВКонтакте.

        Args:
            q (str): поисковый запрос.
            access_token (str): токен доступа для выполнения запроса.

        Returns:
            Tuple[Dict, int]: кортеж из двух элементов:
                - dict: тело ответа API в формате JSON.
                - int: HTTP‑статус‑код ответа.
        """
        method = f"{self.base_url}search.getHints"

        params = {
            "q": q,
            "v": self.api_version,
            "access_token": access_token
        }

        with allure.step(f"Отправка GET‑запроса к "
                         f"{method} с параметрами: {params}"):
            response = requests.get(method, params=params)

        status_code = response.status_code
        response_body = response.json()

        with allure.step(f"Получен ответ: статус "
                         f"{status_code}, данные {response_body}"):
            pass

        return response_body, status_code

    @allure.step(
        "Поиск друзей по запросу и получение ID указанного пользователя")
    def list_id_friend_search(self, q: str) -> Tuple[Dict, int, int]:
        with allure.step("Чтение номера пользователя из .env (FRIEND_NUM)"):
            friend_num_str: str = os.getenv("FRIEND_NUM", "6")
            friend_num: int = int(friend_num_str)

        method = (f"{self.base_url}friends.search?v="
                  f"{self.api_version}&client_id="
                  f"{self.client_id}")

        params = {
            "q": q,
            "offset": "0",
            "count": "20",
            "fields": "id,first_name,last_name",
            "access_token": self.access_token
        }

        with allure.step(
                f"Отправка GET‑запроса для поиска друзей:"
                f"{method}, параметры: {params}"):
            response = requests.get(method, params=params)

        status_code = response.status_code
        response_body = response.json()

        with allure.step(
                "Парсинг ответа и извлечение ID указанного пользователя"):
            response_data = response_body['response']
            items = response_data['items']
            item_by_index = items[friend_num]
            user_id = item_by_index['id']
            self.user_id = user_id

        with allure.step(f"Найден ID пользователя №"
                         f"{friend_num + 1}: {self.user_id}"):
            pass

        return response_body, status_code, self.user_id

    @allure.step("Создание чата с найденным пользователем")
    def create_chat_friend(self, title: str) -> Tuple[Dict, int, int, int]:
        """
        Создаёт чат с найденным пользователем через
        метод messages.createChat API ВКонтакте.

        Args:
            title (str): название создаваемого чата.

        Returns:
            Tuple[Dict, int, int, int]: кортеж из четырёх элементов:
                - dict: тело ответа API в формате JSON.
                - int: HTTP‑статус‑код ответа.
                - int: ID созданного чата (сохраняется в self.chat_id).
                - int: peer_id первого собеседника в чате
                (сохраняется в self.peer_id).
        """
        method = (f"{self.base_url}messages.createChat?v="
                  f"{self.api_version}&client_id="
                  f"{self.client_id}")

        params = {
            "user_ids": self.user_id,
            "phone_numbers": None,
            "title": title,
            "permissions": self.permissions,
            "group_id": "0",
            "device_id": self.device_id,
            "is_disable_stickers_popup_autoplay": "0",
            "access_token": self.access_token
        }

        with allure.step(f"Отправка GET‑запроса на создание чата: {method}"):
            response = requests.get(method, params=params)

        status_code = response.status_code
        response_body = response.json()

        with allure.step("Парсинг данных о созданном чате"):
            response_data = response_body['response']
            chat_id = response_data['chat_id']
            peer_ids_list = response_data['peer_ids']
            peer_id = peer_ids_list[0]

            self.chat_id = chat_id
            self.peer_id = peer_id

        with allure.step(f"Чат создан: ID="
                         f"{self.chat_id}, peer_id={self.peer_id}"):
            pass

        return response_body, status_code, self.chat_id, self.peer_id

    @allure.step("Удаление чата для всех участников")
    def delete_chat(self) -> Tuple[int, Dict]:
        """
        Удаляет чат для всех участников через
        метод messages.dropChatForAll API ВКонтакте.

        Returns:
            Tuple[int, Dict]: кортеж из двух элементов:
                - int: HTTP‑статус‑код ответа.
                - dict: тело ответа API в формате JSON.
        """
        method = (f"{self.base_url}messages.dropChatForAll?v="
                  f"{self.api_version}&client_id="
                  f"{self.client_id}")

        params = {
            "chat_id": self.chat_id,
            "group_id": "0",
            "access_token": self.access_token
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }

        with allure.step(f"Отправка POST‑запроса на удаление чата: {method}"):
            response = requests.post(
                url=method, data=params, headers=headers)

        status_code = response.status_code
        response_body = response.json()

        with allure.step(f"Чат удалён. Статус:"
                         f"{status_code}, ответ: {response_body}"):
            pass

        return status_code, response_body
