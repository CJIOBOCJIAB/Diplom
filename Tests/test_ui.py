import os
import time
import pytest
import allure
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from dotenv import load_dotenv

from Diplom.Pages.ui_vk_page import UiVkPage


load_dotenv()


@allure.feature("UI тестирование VK")
@allure.title("Тест аудиораздела")
@allure.description(
    "Проверка функциональности раздела 'Музыка' в VK: загрузка"
    "страницы, переход в раздел, отображение новинок и треков")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_ui_audio(browser: WebDriver) -> None:
    base_url: str = os.getenv("UI_BASE_URL")

    # Селекторы
    audio_css: str = os.getenv("AUDIO_CSS_SELECTOR")
    new_songs_css: str = os.getenv("SONG_CSS_SELECTOR")
    track_css: str = os.getenv("TRACK_CSS_SELECTOR")

    # Создание экземпляра страницы
    page: UiVkPage = UiVkPage(browser, base_url)

    with allure.step("Проверка загрузки страницы пользователя"):
        start_time: float = time.time()
        page.navigate_to_base_url()
        load_time: float = time.time() - start_time
        with allure.step(f"Время загрузки страницы: {load_time:.2f} сек"):
            assert load_time < 70, \
                f"Страница загружалась слишком долго: {load_time:.2f} сек"

    with allure.step("Ожидание видимости элемента 'Музыка' и клик"):
        audio: WebElement = page.find_element_by_css(audio_css)
        with allure.step("Проверка видимости элемента 'Музыка'"):
            assert audio.is_displayed(), \
                "Элемент audio_selector не отображается на странице"
        page.click_element(audio_css, by=By.CSS_SELECTOR)
        print("Клик audio выполнен")

    with allure.step("Ожидание видимости элемента 'Показать все' и клик"):
        new_songs: WebElement = page.find_element_by_css(new_songs_css)
        with allure.step("Проверка видимости элемента 'Показать все'"):
            assert new_songs.is_displayed(), \
                "Элемент new_songs_selector не отображается на странице"
        page.click_element(new_songs_css, by=By.CSS_SELECTOR)
        print("Клик new_songs выполнен")

    with allure.step("Поиск всех элементов на странице 'Новинки'"):
        tracks: List[WebElement] = page.find_elements_by_css(track_css)
        with allure.step(
                f"Проверка количества найденных треков: {len(tracks)}"):
            assert len(tracks) >= 10, \
                f"Найдено слишком мало треков: {len(tracks)}"
        print(f"Найдено {len(tracks)} аудиозаписей")


@allure.feature("UI тестирование VK")
@allure.title("Тест видеораздела")
@allure.description(
    "Проверка функциональности раздела 'Видео' в VK: переход в раздел,"
    "открытие новой вкладки, переход в категорию 'Детям'")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_ui_video(browser: WebDriver) -> None:
    base_url: str = os.getenv("UI_BASE_URL")

    # Селекторы
    video_css: str = os.getenv("VIDEO_CSS_SELECTOR")
    child_xpath: str = os.getenv("CHILD_XPATH_SELECTOR")
    unik_xpath: str = os.getenv("UNIK_XPATH_SELECTOR")

    # Создание экземпляра страницы
    page: UiVkPage = UiVkPage(browser, base_url)

    page.navigate_to_base_url()

    with allure.step("Ожидание видимости элемента 'Видео' и клик"):
        video: WebElement = page.find_element_by_css(video_css)
        with allure.step("Проверка видимости элемента 'Видео'"):
            assert video.is_displayed(), \
                "Элемент video_selector не отображается на странице"
        page.click_element(video_css, by=By.CSS_SELECTOR)
        print("Клик video выполнен")

    with allure.step("Переход на новую вкладку"):
        browser.switch_to.window(browser.window_handles[-1])

    with allure.step("Ожидание видимости элемента 'Детям' и клик"):
        child: WebElement = page.find_element_by_xpath(child_xpath)
        with allure.step("Проверка видимости элемента 'Детям'"):
            assert child.is_displayed(), \
                "Элемент child_xpath не отображается на странице"
        page.click_element(child_xpath, by=By.XPATH)
        print("Клик child выполнен")

    with allure.step("Ожидание видимости элемента 'Любимые герои'"):
        unik: WebElement = page.find_element_by_xpath(unik_xpath)
        with allure.step("Проверка видимости элемента 'Любимые герои'"):
            assert unik.is_displayed(), \
                "Элемент unik_xpath не отображается на странице"


@allure.feature("UI тестирование VK")
@allure.title("Тест сообществ")
@allure.description(
    "Проверка поиска сообществ в категории"
    "'Спорт' по запросу 'Хоккей России'")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_ui_groups(browser: WebDriver) -> None:
    base_url: str = os.getenv("UI_BASE_URL")
    message: str = os.getenv("GROUPS_NAME")

    # Селекторы
    groups_xpath: str = os.getenv("GROUPS_XPATH_SELECTOR")
    sport_xpath: str = os.getenv("SPORT_XPATH_SELECTOR")
    input_xpath: str = os.getenv("INPUT_XPATH_SELECTOR")
    button_xpath: str = os.getenv("BUTTON_XPATH_SELECTOR")

    # Создание экземпляра страницы
    page: UiVkPage = UiVkPage(browser, base_url)

    page.navigate_to_base_url()

    with allure.step("Ожидание видимости элемента 'Сообщества' и клик"):
        groups: WebElement = page.find_element_by_xpath(groups_xpath)
        with allure.step("Проверка видимости элемента 'Сообщества'"):
            assert groups.is_displayed(), \
                "Элемент groups_xpath не отображается на странице"
        page.click_element(groups_xpath, by=By.XPATH)
        print("Клик groups выполнен")

    with allure.step("Ожидание видимости элемента 'Спорт' и клик"):
        sport: WebElement = page.find_element_by_xpath(sport_xpath)
        with allure.step("Проверка видимости элемента 'Спорт'"):
            assert sport.is_displayed(), \
                "Элемент sport_xpath не отображается на странице"
        page.click_element(sport_xpath, by=By.XPATH)
        print("Клик sport выполнен")

    with allure.step("Ожидание видимости поля поиска сообществ и ввод текста"):
        enter: WebElement = page.find_element_by_xpath(input_xpath)
        with allure.step("Проверка видимости поля поиска"):
            assert enter.is_displayed(), \
                "Элемент input_xpath не отображается на странице"
        page.send_keys(input_xpath, message)
        print("Текст введён в поле поиска")

    with allure.step("Ожидание видимости кнопки 'Поиск' и клик"):
        button: WebElement = page.find_element_by_xpath(button_xpath)
        with allure.step("Проверка видимости кнопки 'Поиск'"):
            assert button.is_displayed(), \
                "Элемент button_xpath не отображается на странице"
        page.click_element(button_xpath, by=By.XPATH)
        print("Клик button выполнен")


@allure.title("Тест перехода на страницу «Мини‑приложения»")
@allure.description(
    "Проверяет, что клик по элементу «Мини приложения» приводит к"
    "переходу на ожидаемую страницу с URL из"
    "переменной окружения SERVICES_URL.")
@allure.feature("UI‑тесты VK")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_ui_apps(browser: WebDriver) -> None:
    base_url: str = os.getenv("UI_BASE_URL")
    expected_url: str = os.getenv("SERVICES_URL")
    # Селекторы
    apps_xpath: str = os.getenv("APPS_XPATH_SELECTOR")

    # Создание экземпляра страницы
    page: UiVkPage = UiVkPage(browser, base_url)

    with allure.step("Переход на базовую страницу"):
        page.navigate_to_base_url()

    with allure.step(
            "Ожидание видимости элемента «Мини приложения» и клик по нему"):
        apps: WebElement = page.find_element_by_xpath(apps_xpath)
        assert apps.is_displayed(), \
            "Элемент apps_xpath не отображается на странице"
        page.click_element(apps_xpath, by=By.XPATH)
        print("Клик apps выполнен")

    with allure.step("Ожидание изменения URL после клика"):
        WebDriverWait(page.browser, 15).until(
            lambda driver: expected_url in driver.current_url
        )

    with allure.step("Проверка соответствия текущего URL ожидаемому"):
        actual_url: str = page.get_current_url()
        assert actual_url == expected_url, \
            f"Ожидаемый URL: {expected_url}, но получен: {actual_url}"
        print("URL соответствует ожидаемому: https://vk.com/services")


@allure.title("Тест перехода на страницу «Игры»")
@allure.description(
    "Проверяет, что клик по элементу «Игры» приводит к переходу на"
    "ожидаемую страницу с URL из переменной окружения GAMES_URL.")
@allure.feature("UI‑тесты VK")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_ui_games(browser: WebDriver) -> None:
    base_url: str = os.getenv("UI_BASE_URL")
    expected_url: str = os.getenv("GAMES_URL")

    # Селекторы
    games_xpath: str = os.getenv("GAMES_XPATH_SELECTOR")

    # Создание экземпляра страницы
    page: UiVkPage = UiVkPage(browser, base_url)

    with allure.step("Переход на базовую страницу"):
        page.navigate_to_base_url()

    with allure.step("Ожидание видимости элемента «Игры» и клик по нему"):
        games: WebElement = page.find_element_by_xpath(games_xpath)
        assert games.is_displayed(), \
            "Элемент games_xpath не отображается на странице"
        page.click_element(games_xpath, by=By.XPATH)
        print("Клик games выполнен")

    with allure.step("Ожидание изменения URL после клика"):
        WebDriverWait(page.browser, 15).until(
            lambda driver: expected_url in driver.current_url
        )

    with allure.step("Проверка соответствия текущего URL ожидаемому"):
        actual_url: str = page.get_current_url()
        assert actual_url == expected_url, \
            f"Ожидаемый URL: {expected_url}, но получен: {actual_url}"
        print("URL соответствует ожидаемому: https://vk.com/games")
