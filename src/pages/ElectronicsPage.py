import traceback

from src.pages.BasePageObject import BasePage


class ElectronicsPage(BasePage):
    """Страница с электроникой"""
    SECTION = "//span[contains(text(), '%s')]"

    def select_section(self, section_name):
        """Метод для перехода в раздел (section_name) Яндекс Маркета.

        Args:
            section_name: название раздела с продуктами

        """
        section_xpath = self.xpath_maker(self.SECTION, section_name)
        section = self.element(section_xpath)
        section.click()
        try:
            assert "%s — купить на Яндекс.Маркете" % section_name in self.driver.title

        except Exception:
            print(traceback.format_exc())
            self.tear_down()