# coding=utf-8
import traceback
import time
import re
from src.pages.BasePageObject import BasePage

names_first_element_of_lists = []  # Здесь будут имена первых элементов в списке до и после поиска
names_of_brands = []  # Тут храним имена производителей
global_price_from = None  # Две переменные с ценой нужны для того, чтобы в конце теста проверить, что искомый
global_price_before = None  # товар отображается в диапазоне цен, который был задан
type_of_product = None
iteration_of_steps_plus_one = 0


class MarketPage(BasePage):
    """Страница Яндекс Маркета"""
    TYPE = "//a[contains(text(), '%s')]"
    ALL_FILTERS_BUTTON = "//span[contains(text(), 'Все фильтры')]"
    PRICE_FROM = "//input[@id='glf-pricefrom-var']"
    COUNT_OF_PRODUCT = "//*[contains(@class,'n-filter-panel-counter')]"
    PRICE_BEFORE = "//input[@id='glf-priceto-var']"
    BRAND_DISPLAY = "//div[@data-filter-id='7893318']/child::div[2]"
    BRAND = "//span[contains(text(), 'Производитель')]"
    DISPLAY_ALL = "//div[@data-filter-id='7893318']//button"
    SEARCH_FILTER = "//div[@data-filter-id='7893318']//span[@class = 'input__box']/input"
    TV = "//label[contains(text(), '%s')]"
    TV_CHECK_BOX = "//label[contains(text(), '%s')]/ancestor::span[1]"
    CLEAN_SEARCH = "//div[@data-filter-id='7893318']//span[@unselectable='on']"
    SHOW_RELEVANT = "//span[contains(text(), 'Показать подходящие')]/ancestor::a"
    FIRST_ELEMENT_OF_THE_LIST = "//div[contains(@class, 'snippet-list_js_inited')]" \
                                "/child::*[1]//div[@class='n-snippet-card2__title']/a"
    SEARCH = "//*[@class='search2__input']//input[@name='text']"
    SEARCH_BUTTON = "//span[@class='search2__button']/button"
    LIST_BUTTON = "//label[contains(@class, 'radio_side_right')]"
    MAIN = "//*[@class='main'])"
    CHECK_SHOW_ALL_BUTTON = "//div[@data-filter-id='7893318']//div[contains(@class, " \
                            "'more-list__top i-bem n-filt')]/child::div[1]"
    CHECK_PRICE = "//div[contains(@class, 'snippet-list_js_inited')]/child::*[1]//div[contains(@class," \
                  "\"n-snippet-card2__part_type_right\")]//div[@class='price']"

    def select_type(self, type_name):
        """Метод для выбора типа продукта Яндекс Маркета.

        Args:
            type_name: тип продукта

        """
        global type_of_product
        type_of_product = type_name

        product_type_xpath = self.xpath_maker(self.TYPE, type_name)
        self.check_visible_and_scroll(product_type_xpath)
        product_type = self.element(product_type_xpath)
        product_type.click()
        try:
            assert "%s — купить на Яндекс.Маркете" % type_name in self.driver.title

        except Exception:
            print(traceback.format_exc())
            self.tear_down()

    def all_filters_button(self):
        """Метод для отображения всех фильтров продукта."""
        filter_button = self.element(self.ALL_FILTERS_BUTTON)
        self.check_visible_and_scroll(self.ALL_FILTERS_BUTTON)
        filter_button.click()
        try:
            assert "Все фильтры — %s — выбор по параметрам на Яндекс.Маркете" % type_of_product in self.driver.title

        except Exception:
            print(traceback.format_exc())
            self.tear_down()

    def set_price(self, price_from, price_before):
        """Метод для установления цены в фильтре продуктов от и до.

        Args:
            price_from: минимальная цена продукта
            price_before: максимальная цена продукта

        """

        # Цена От
        from_price = self.element(self.PRICE_FROM)
        from_price.send_keys(price_from)
        # COUNT_OF_PRODUCT показывает сколько товаров соответствует фильтру
        self.visible(self.COUNT_OF_PRODUCT)
        global global_price_from
        global_price_from = from_price.get_attribute('value')

        # Цена До
        before_price = self.element(self.PRICE_BEFORE)
        before_price.send_keys(price_before)
        self.visible(self.COUNT_OF_PRODUCT)
        global global_price_before
        global_price_before = before_price.get_attribute('value')
        try:
            assert global_price_from in price_from
            assert global_price_before in price_before
        except Exception:
            print(traceback.format_exc())
            self.tear_down()

        # Проверяем что раздел Производители в Фильтре развёрнут, соответственно, если свёрнут, разворачиваем
        if "display: none;" in self.element(self.BRAND_DISPLAY).get_attribute("style"):
            brand = self.element(self.BRAND)
            brand.click()

        # Проверяем что список производителей свёрнут и разворачиваем его
        self.check_visible_and_scroll(self.DISPLAY_ALL)
        display_all = self.element(self.DISPLAY_ALL)
        if "n-filter-block__list-items i-bem" in self.element(self.CHECK_SHOW_ALL_BUTTON).get_attribute(
                "class"):
            display_all.click()

    # Сюда попадают названия Производителей
    def select_brands(self, all_brands_list):
        """Метод для выбора производителей в фильтре.

        Args:
            all_brands_list: массив со всеми производителями
        """
        global names_of_brands
        names_of_brands = all_brands_list

        # Сюда по очереди попадают названия Производителей, происходит их поиск, и выбор чек-бокса
        for manufacturer in all_brands_list:
            search_filter = self.element(self.SEARCH_FILTER)
            search_filter.send_keys(manufacturer)
            time.sleep(2)
            types = self.xpath_maker(self.TV, manufacturer)
            types = self.clickable(types)
            types.click()

            # Тут проверяется, что чек-бокс проставлен
            check_accept_checkbox = self.xpath_maker(self.TV_CHECK_BOX, manufacturer)
            try:
                assert "checkbox_checked_yes" in self.element(check_accept_checkbox).get_attribute("class")

            except Exception:
                print(traceback.format_exc())
                self.tear_down()

            # Очищается поле поиска
            clean_search_field = self.clickable(self.CLEAN_SEARCH)
            clean_search_field.click()

    def show_relevant_products(self):
        """Метод для отображения продуктов согласно выставленным значениям фильтра."""
        self.check_visible_and_scroll(self.SHOW_RELEVANT)
        show_relevant = self.clickable(self.SHOW_RELEVANT)
        show_relevant.click()
        try:
            if type_of_product == "Телевизоры":
                assert "%s — купить на Яндекс.Маркете" % type_of_product in self.driver.title
            else:
                assert "%s %s — купить на Яндекс.Маркете" % (type_of_product, names_of_brands[0]) in self.driver.title

        except Exception:
            print(traceback.format_exc())
            self.tear_down()

    def find_first_element_of_list(self):
        """Метод для поиска первого элемента в списке отфильтрованных товаров и сохранения его имени.

        Этот метод отрабатывает 2 раза. После фильтрации и после того как мы ищем товар в поисковике. После фильтрации
        цена товара находится в диапазоне который мы задали, а после поиска цена может измениться (потому что Яндекс
        Маркет предлагает более выгодные предложения с других магазинов). Для того чтобы ассерты на проверку цены
        отработали только при первой итерации нужна переменная iteration_of_steps_plus_one

        """
        global iteration_of_steps_plus_one
        iteration_of_steps_plus_one += 1

        # make_list переключает вывод результата поиска в список (а не ячейки)
        make_list = self.clickable(self.LIST_BUTTON)
        make_list.click()
        self.check_visible_and_scroll(self.FIRST_ELEMENT_OF_THE_LIST)
        first_element_of_list = self.element(self.FIRST_ELEMENT_OF_THE_LIST)
        global names_first_element_of_lists
        names_first_element_of_lists.append(first_element_of_list.get_attribute("title"))

        # Достаём значение цены товара, убираем пробелы и знак рубля
        price = self.element(self.CHECK_PRICE).text
        result = re.findall(r'[0-9]+', price)
        price_without_space = ""
        for x in result:
            price_without_space += x

        # Проверяем, что искомый товар отображается в диапазоне цен, который мы задали в фильтре
        try:
            if iteration_of_steps_plus_one == 1:
                assert int(global_price_from) <= int(price_without_space)
                if int(global_price_before) != 0:
                    assert int(price_without_space) <= int(global_price_before)

            # Проверяем, что искомый товар отображается по производителям, которые были заданы в фильтре
            array_length = len(names_of_brands)
            for name in names_of_brands:
                if name in names_first_element_of_lists:
                    break
                if array_length == 0:
                    assert name in names_first_element_of_lists
                array_length -= 1

        except Exception:
            print(traceback.format_exc())
            self.tear_down()

    def search_by_save_value(self):
        """Метод для поиска товара в поисковике Яндекс Маркета по сохранённому значению."""
        search = self.clickable(self.SEARCH)
        search.send_keys(names_first_element_of_lists[0])
        search_button = self.clickable(self.SEARCH_BUTTON)
        search_button.click()
        try:
            assert "«%s» — %s — купить на Яндекс.Маркете" % (names_first_element_of_lists[0], type_of_product) \
                   in self.driver.title

        except Exception:
            print(traceback.format_exc())
            self.tear_down()

    def compare_first_elements(self):
        """Метод для сравнения двух сохраненных значений"""
        try:
            assert names_first_element_of_lists[0] in names_first_element_of_lists[1]

        except Exception:
            print(traceback.format_exc())
            self.tear_down()
