from behave import step

from src.pages import ElectronicsPage

electronics_page = ElectronicsPage.ElectronicsPage()


@step("Выбран раздел '{section_of_product}'")
def select_section(context, section_of_product):
    """Метод для перехода в раздел (section_of_product) Яндекс Маркета.

    Args:
        section_of_product: название раздела с продуктами

    """
    electronics_page.select_section(section_of_product)
