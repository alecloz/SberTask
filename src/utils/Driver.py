from selenium import webdriver


class Driver:
    """Класс Singleton для генерации webdriver"""

    class __Driver:
        driver = None
        
        def __init__(self):
            self.driver = webdriver.Chrome("./chromedriver.exe")

    driver = None
    
    def __init__(self):
        if not self.driver:
            Driver.driver = Driver.__Driver().driver
