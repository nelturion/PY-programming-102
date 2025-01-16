import unittest
from unittest.mock import mock_open
from unittest.mock import patch

import src.lab4.store as store


class test_store(unittest.TestCase):
    def test_phone_validator(self):
        # given
        wrong_number_a = "+7-996-abc-12-36"
        wrong_number_b = '+7-996-abc-12-36'
        wrong_number_c = '+7-996-123-1236'
        wrong_number_d = '+79961231236'
        wrong_number_e = '+7996-123-12-36'
        wrong_number_f = '+7996-123-+12-36'
        wrong_number_g = "+1-101-123-78-7k"
        wrong_number_h = ""
        wrong_number_i = "Москва. Красная площадь. Красная площадь. ЖК Кремль"

        correct_number_a = '+7-789-456-78-78'
        correct_number_b = "+7-789-456-78-78"

        #when
        fun = store.validate_phone

        # then
        self.assertEqual(fun(wrong_number_a), (False, 'invalid format'))
        self.assertEqual(fun(wrong_number_b), (False, 'invalid format'))
        self.assertEqual(fun(wrong_number_c), (False, 'invalid format'))
        self.assertEqual(fun(wrong_number_d), (False, 'invalid format'))
        self.assertEqual(fun(wrong_number_e), (False, 'invalid format'))
        self.assertEqual(fun(wrong_number_f), (False, 'invalid format'))
        self.assertEqual(fun(wrong_number_g), (False, 'invalid format'))
        self.assertEqual(fun(wrong_number_h), (False, 'no data'))
        self.assertEqual(fun(wrong_number_i), (False, 'invalid format'))

        self.assertEqual(fun(correct_number_a), (True, correct_number_a))
        self.assertEqual(fun(correct_number_b), (True, correct_number_b))

    def test_address_validator(self):
        # given
        wrong_address_a = ""
        wrong_address_b = "+7-996-abc-12-36"
        wrong_address_c = "+7-996-123-12-36"
        wrong_address_d = "+7-996-123-12-36"
        wrong_address_e = "Sample country. Sample city. Sample district. Sample street."
        wrong_address_f = "sample country. sample city. sample district. sample street."
        wrong_address_g = "sample country.sample city.sample district.sample street"
        wrong_address_h = "sample country; sample city; sample district; sample street"

        correct_address_a = "Sample country. Sample city. Sample district. Sample street"
        correct_address_b = "sample country. sample city. sample district. sample street"

        # when
        fun = store.validate_address

        # then
        self.assertEqual(fun(wrong_address_a), (False, 'no data'))
        self.assertEqual(fun(wrong_address_b), (False, 'invalid format'))
        self.assertEqual(fun(wrong_address_c), (False, 'invalid format'))
        self.assertEqual(fun(wrong_address_d), (False, 'invalid format'))
        self.assertEqual(fun(wrong_address_e), (False, 'invalid format'))
        self.assertEqual(fun(wrong_address_f), (False, 'invalid format'))
        self.assertEqual(fun(wrong_address_g), (False, 'invalid format'))
        self.assertEqual(fun(wrong_address_h), (False, 'invalid format'))
        self.assertEqual(fun(correct_address_a), (True, correct_address_a))
        self.assertEqual(fun(correct_address_b), (True, correct_address_b))

    """
    @patch("builtins.open", new_callable=mock_open)
    def test_order_processor(self, mock_file):
        # given
        mock_file.return_value.read.return_value = (
            "31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE\n"
            "87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX\n"
            "31987;Сыр, Колбаса, Макароны, Сыр, Колбаса;Петрова Анна Сергеевна;Франция. Иль-де-Франс. Париж. Шанз-Элизе;+3-214-020-50-50;MIDDLE\n"
            "56342;Хлеб, Молоко, Хлеб, Молоко;Смирнова Мария Леонидовна;Германия. Бавария. Мюнхен. Мариенплац;+4-989-234-56;LOW\n"
            "48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX\n"
            "65829;Сок, Вода, Сок, Вода;Белова Екатерина Михайловна;Испания. Каталония. Барселона. Рамбла;+34-93-1234-567;LOW\n"
            "72901;Чай, Кофе, Чай, Кофе;Михайлов Сергей Петрович;Великобритания. Англия. Лондон. Бейкер-стрит;+4-207-946-09-58;LOW\n"
            "84756;Печенье, Сыр, Печенье, Сыр;Васильева Анна Владимировна;Япония. Шибуя. Шибуя-кроссинг;+8-131-234-5678;MAX\n"
            "90385;Макароны, Сыр, Макароны, Сыр;Николаев Николай;;+1-416-123-45-67;LOW\n"
        )

        # when
        valid_orders_count = 5  # Ожидаем 5 валидных заказов
        invalid_orders_count = 5  # Ожидаем 5 невалидных заказов

        valid_orders_list = store.process_orders("dummy_path")

        # then
        self.assertEqual(len(valid_orders_list[0]), valid_orders_count)
        self.assertEqual(len(valid_orders_list[1]), invalid_orders_count)
    """