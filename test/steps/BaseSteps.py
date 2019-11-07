from behave import step

from src.pages import BasePageObject

base_page_object = BasePageObject.BasePage()


@step("Выполнен переход на сайт '{url}'")
def set_up(context, url):
    """Метод для запуска браузера.

    Раскрывает браузер на весь экран. Переходит по заданной ссылке (url) на сайт.
    Задает тайм-аут ожидания для неявного ожидания обнаружения элемента или завершения команды.

    Args:
        url: адрес страницы

    """
    base_page_object.set_up(url)


@step("Выполнен выход из браузера")
def tear_down(context):
    """Метод для выхода из браузера и завершения теста."""
    base_page_object.tear_down()
