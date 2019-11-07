import traceback

from src.pages.BasePageObject import BasePage


class MainPage(BasePage):
    """Главная страница Яндекса"""
    CATEGORY = "//a[contains(text(), '%s')]"

    def pick_category(self, category_name):
        """Метод для перехода на выбранную категорию Яндекс.

        Args:
            category_name: категория меню Яндекса

        """
        category_xpath = self.xpath_maker(self.CATEGORY, category_name)
        category = self.clickable(category_xpath)
        category.click()
        try:
            assert 'Яндекс.Маркет — выбор и покупка товаров из проверенных интернет-магазинов' in self.driver.title

        except Exception:
            print(traceback.format_exc())
            self.tear_down()
