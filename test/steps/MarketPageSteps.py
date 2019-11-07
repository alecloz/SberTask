from behave import step

from src.pages import MarketPage

market_page = MarketPage.MarketPage()


@step("Выбран тип '{type_of_product}'")
def select_type(context, type_of_product):
    """Метод для выбора типа продукта Яндекс Маркета.

    Args:
        type_of_product: тип продукта

    """
    market_page.select_type(type_of_product)


@step('Выполнено нажатие на кнопку "Все фильтры"')
def all_filters_button(context):
    """Метод для отображения всех фильтров продукта."""
    market_page.all_filters_button()


@step("Установлена цена от '{price_from}' до '{price_before}' рублей")
def set_price(context, price_from, price_before):
    """Метод для установления цены в фильтре продуктов от и до.

    Здесь используется передача данных через Examples в feature-файле, потому что цены всегда только две.

    Args:
        price_from: минимальная цена продукта
        price_before: максимальная цена продукта

    """
    market_page.set_price(price_from, price_before)


@step("Выбраны производители")
def select_brands(context):
    """Метод для выбора производителей в фильтре, переданных в таблице из feature-файла.

    Здесь используется передача данных именно с таблицы, для того чтобы можно было добавить любое количество
    проиводителей в будущем. Получаем array_with_brands - лист со всеми производителями.

    """
    array_with_brands = []
    for name in context.table:
        array_with_brands.append(name["Производители"])
    market_page.select_brands(array_with_brands)


@step('Выполнено нажатие на кнопку "Показать подходящие"')
def show_relevant_products(context):
    """Метод для отображения продуктов согласно выставленным значениям фильтра."""
    market_page.show_relevant_products()


@step("Сохранено название первого товара в списке")
def find_first_element_of_list(context):
    """Метод для поиска первого элемента в списке отфильтрованных товаров и сохранения его имени."""
    market_page.find_first_element_of_list()


@step("Выполнен поиск по сохраненному названию товара")
def search_by_save_value(context):
    """Метод для поиска товара в поисковике Яндекс Маркета по сохранённому значению."""
    market_page.search_by_save_value()


@step("Выполнено сравнение двух сохраненных значений")
def compare_first_elements(context):
    """Метод для сравнения двух сохраненных значений"""
    market_page.compare_first_elements()
