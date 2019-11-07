# Created by user at 06.11.2019
Feature: Поисковик в Яндекс Маркете

  Background:
    Given Выполнен переход на сайт 'https://yandex.ru/'

  Scenario Outline: Наушники Beats

    Given Выполнен переход в Яндекс 'Маркет'
    When Выбран раздел 'Электроника'
    And Выбран тип 'Наушники и Bluetooth-гарнитуры'
    And Выполнено нажатие на кнопку "Все фильтры"
    And Установлена цена от '<Цена от>' до '<Цена до>' рублей
    And Выбраны производители
      | Производители |
      | Beats         |
    And Выполнено нажатие на кнопку "Показать подходящие"
    Then Сохранено название первого товара в списке
    When Выполнен поиск по сохраненному названию товара
    Then Сохранено название первого товара в списке
    And Выполнено сравнение двух сохраненных значений
    And Выполнен выход из браузера
    Examples: Данные для заполнения цены товаров в фильтре
      | Цена от | Цена до |
      | 8000    | 0       |
