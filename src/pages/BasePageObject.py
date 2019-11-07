import sys
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from src.utils import Driver


class BasePage:
    """Базовая страница"""
    driver = Driver.Driver().driver
    wait = WebDriverWait(driver, 60)

    def set_up(self, url):
        """Метод для запуска браузера

        Раскрывает браузер на весь экран. Переходит по заданной ссылке (url) на сайт.
        Задает тайм-аут ожидания для неявного ожидания обнаружения элемента или завершения команды.

        Args:
            url: адрес страницы

        """
        self.driver.maximize_window()
        self.driver.get(url)
        self.driver.implicitly_wait(30)

        try:
            assert 'Яндекс' in self.driver.title

        except Exception:
            print(traceback.format_exc())
            self.tear_down()

    def tear_down(self):
        """Метод для выхода из браузера и завершения теста

        Проверка на traceback необходима для того, чтобы если в тесте случалась ошибка, мы прекращали выполнение теста,
        а в случае если все шаги прошли успешно, программа не завершалась до окончания выполнения последнего шага

        """
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()

            trace = str(traceback.format_exc())
            if trace not in "NoneType: None\n":
                sys.exit()

    def xpath_maker(self, xpath, value):
        """Метод для создания xpath.

        В метод передаётся значение (xpath) с пропущенной частью типа %s и значение (value), которое подставляется
        в строку.

        Args:
            xpath: xpath запрос
            value: значение которое подставляется в xpath

        """
        full_xpath = xpath % value
        return full_xpath

    def element(self, xpath):
        """Метод для нахождения элемента на странице.

        Args:
            xpath: xpath запрос

        """
        find_element = self.driver.find_element_by_xpath(xpath)
        return find_element

    def visible(self, xpath):
        """Метод для проверки того, что элемент является виимым на странице.

        Args:
            xpath: xpath запрос

        """
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def clickable(self, xpath):
        """Метод для проверки того, что элемент является кликабельным.

        Args:
            xpath: xpath запрос

        """
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

    def check_visible_and_scroll(self, xpath):
        """Метод проверяет является ли элемент видимым. Если да, скролит страницу до этого элемента.

        Args:
            xpath: xpath запрос

        """
        if not self.visible(xpath):
            self.scroll(xpath)

    def scroll(self, xpath):
        """Метод для скрола страницы до заданного элемента.

        Args:
            xpath: xpath запрос

        """
        self.driver.execute_script("arguments[0].scrollIntoView();", self.element(xpath))
