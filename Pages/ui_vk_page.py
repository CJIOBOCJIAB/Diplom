import allure
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException
)
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class UiVkPage:
    def __init__(
            self,
            browser,
            base_url: str,
            timeout: int = 60,
            poll_frequency: float = 0.5
    ):
        """
        Инициализация класса.

        :param browser: Экземпляр WebDriver
        :param base_url: базовый URL для загрузки страницы
        :param timeout: время ожидания в секундах
        :param poll_frequency: частота проверки условий в секундах
        """
        self.browser = browser
        self.base_url: str = base_url
        self.timeout: int = timeout
        self.poll_frequency: float = poll_frequency
        self.wait: WebDriverWait = WebDriverWait(
            self.browser, self.timeout, self.poll_frequency)

    @allure.step("Переход на базовый URL")
    def navigate_to_base_url(self) -> None:
        """Вызов базового URL."""
        with allure.step("Установка неявного ожидания 10 с"):
            self.browser.implicitly_wait(10)
        with allure.step(f"Открытие URL: {self.base_url}"):
            self.browser.get(self.base_url)

    @allure.step("Получение текущего URL страницы")
    def get_current_url(self) -> str:
        """Возвращает текущий URL страницы."""
        current_url = self.browser.current_url
        with allure.step(f"Текущий URL: {current_url}"):
            pass
        return current_url

    @allure.step("Поиск элемента по CSS‑селектору: {css_selector}")
    def find_element_by_css(self, css_selector: str) -> WebElement:
        """
        Поиск элемента по CSS‑селектору.

        :param css_selector: CSS‑селектор для поиска элемента
        :return: найденный WebElement
        """
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css_selector))
        )

    @allure.step("Поиск элемента по XPath‑селектору: {xpath_selector}")
    def find_element_by_xpath(self, xpath_selector: str) -> WebElement:
        """
        Поиск элемента по XPath‑селектору.

        :param xpath_selector: XPath‑селектор для поиска элемента
        :return: найденный WebElement
        """
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, xpath_selector))
        )

    @allure.step("Поиск всех элементов по CSS‑селектору: {css_selector}")
    def find_elements_by_css(self, css_selector: str) -> List[WebElement]:
        """
        Поиск всех элементов по CSS‑селектору.

        :param css_selector: CSS‑селектор для поиска элементов
        :return: список найденных WebElement
        """
        elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
        with allure.step(f"Найдено элементов: {len(elements)}"):
            pass
        return elements

    @allure.step("Поиск всех элементов по XPath‑селектору: {xpath_selector}")
    def find_elements_by_xpath(self, xpath_selector: str) -> List[WebElement]:
        """
        Поиск всех элементов по XPath‑селектору.

        :param xpath_selector: XPath‑селектор для поиска элементов
        :return: список найденных WebElement
        """
        elements = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath_selector))
        )
        with allure.step(f"Найдено элементов: {len(elements)}"):
            pass
        return elements

    @allure.step("Ввод текста '{text}' в элемент"
                 "по селектору '{selector}' (тип: {by})")
    def send_keys(
            self,
            selector: str,
            text: str,
            max_attempts: int = 3,
            by: By = By.XPATH
    ) -> Optional[WebElement]:
        """
        Надёжно вводит текст в поле с повторными
        попытками при StaleElementReferenceException.

        :param selector: селектор для поиска элемента (XPath или CSS)
        :param text: текст для ввода
        :param max_attempts: максимальное количество попыток
        :param by: тип селектора (By.XPATH или By.CSS_SELECTOR)
        :return: WebElement при успешном вводе, иначе None
        """
        for attempt in range(1, max_attempts + 1):
            with allure.step(f"Попытка {attempt}/{max_attempts} ввода текста"):
                try:
                    with allure.step("Ожидание кликабельности элемента"):
                        element = self.wait.until(
                            EC.element_to_be_clickable((by, selector)))
                    with allure.step("Прокрутка к элементу"):
                        self.browser.execute_script(
                            "arguments[0].scrollIntoView(true);", element)

                    with allure.step("Очистка поля ввода"):
                        element.clear()

                    with allure.step(f"Ввод текста: '{text}'"):
                        element.send_keys(text)

                    return element  # Возвращаем элемент при успехе

                except StaleElementReferenceException:
                    if attempt == max_attempts:
                        with allure.step(
                                "Исчерпаны все попытки — пробрасываем"
                                "StaleElementReferenceException"):
                            raise
                    else:
                        with allure.step(
                                "Элемент устарел — повторяем попытку"):
                            continue  # Повторяем попытку

        # Явный возврат None после исчерпания попыток
        with allure.step(
                "Все попытки ввода текста провалились — возвращаем None"):
            return None

    @allure.step("Клик по элементу с селектором '{selector}' (тип: {by})")
    def click_element(
            self,
            selector: str,
            max_attempts: int = 3,
            by: By = By.XPATH
    ) -> WebElement:
        """
        Надёжно кликает по элементу с повторными попытками при ошибках.

        :param selector: Селектор для поиска элемента (XPath или CSS)
        :param max_attempts: максимальное количество попыток
        :param by: тип селектора (By.XPATH или By.CSS_SELECTOR)
        :return: WebElement при успешном клике
        :raises: Исключение, если все попытки провалились
        """
        for attempt in range(1, max_attempts + 1):
            with allure.step(
                    f"Попытка {attempt}/{max_attempts} клика по элементу"):
                try:
                    with allure.step(
                            "Поиск и ожидание кликабельности элемента"):
                        element = self.wait.until(
                            EC.element_to_be_clickable((by, selector))
                        )

                    with allure.step("Прокрутка к элементу (центрирование)"):
                        self.browser.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});",
                            element
                        )

                    with allure.step("Основной клик через JavaScript"):
                        self.browser.execute_script(
                            "arguments[0].click();", element)
                    return element  # Возвращаем элемент при успехе

                except StaleElementReferenceException:
                    if attempt == max_attempts:
                        with allure.step(
                                "Исчерпаны все попытки — пробрасываем "
                                "StaleElementReferenceException"):
                            raise
                    with allure.step("Элемент устарел — повторяем попытку"):
                        continue  # Повторяем попытку

                except (ElementNotInteractableException,
                        ElementClickInterceptedException) as e:
                    if attempt == max_attempts:
                        with allure.step(
                                "Исчерпаны все попытки"
                                "— пробрасываем исключение"):
                            raise e
                    # Попытка альтернативного клика (ActionChains)
                    with allure.step(
                            "Попытка альтернативного клика (ActionChains)"):
                        try:
                            short_wait = WebDriverWait(
                                self.browser, timeout=2, poll_frequency=0.1)

                            with allure.step(
                                    "Повторное ожидание кликабельности"):
                                element = short_wait.until(
                                    EC.element_to_be_clickable((by, selector))
                                )

                            with allure.step(
                                    "Альтернативный клик через ActionChains"):
                                actions = ActionChains(self.browser)
                                actions.move_to_element(
                                    element).click().perform()
                                return element
                        except (StaleElementReferenceException,
                                ElementNotInteractableException):

                            with allure.step(
                                    "Элемент недоступен для альтернативного"
                                    "клика — продолжаем следующую попытку"):
                                continue
                        except Exception as unexpected_e:

                            with allure.step(
                                    f"Неожиданная ошибка в альтернативном"
                                    f"клике (попытка"
                                    f"{attempt}): {unexpected_e}"):
                                print(f"Unexpected error in"
                                      f"alternative click ("
                                      f"attempt {attempt}): {unexpected_e}")
                                continue

        # Если все попытки исчерпаны, выбрасываем исключение
        with allure.step(
                f"Не удалось кликнуть по элементу"
                f"'{selector}' после {max_attempts} попыток"):
            raise Exception(f"Failed to click element"
                            f"'{selector}' after {max_attempts} attempts")
