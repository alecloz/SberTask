from behave import step

from src.pages import MainPage

main_page = MainPage.MainPage()


@step("Выполнен переход в Яндекс '{category_yandex_menu}'")
def pick_category(context, category_yandex_menu):
    """Метод для перехода на выбранную категорию Яндекса.

    Args:
        category_yandex_menu: категория меню Яндекса

    """
    main_page.pick_category(category_yandex_menu)
