import unittest
from unittest.mock import Mock, call
from parse import parse_json


class TestParseJSON(unittest.TestCase):
    def setUp(self):
        self.json_str = '{"имя": "Грозный Сергей", "пол": "м",' \
                        '"город": "Москва", "адрес":"Ул Победы д 12"}'

    def test_parse_json(self):

        required_fields = ['имя', 'пол', 'адрес']
        keywords = ['Грозный', 'Сергей', 'м', 'Победы', 'Москва']
        keyword_callback = Mock()
        parse_json(self.json_str, required_fields, keywords, keyword_callback)
        calls = [call('имя', 'Грозный'), call('имя', 'Сергей'),
                 call('пол', 'м'), call('адрес', 'Победы')]
        keyword_callback.assert_has_calls(calls)

    def test_parse_fields_none(self):
        keywords = ['Грозный', 'Сергей', 'м', 'Победы', 'Москва']
        keyword_callback = Mock()
        parse_json(self.json_str, keywords=keywords,
                   keyword_callback=keyword_callback)
        calls = [call('имя', 'Грозный'), call('имя', 'Сергей'),
                 call('пол', 'м'), call('город', 'Москва'),
                 call('адрес', 'Победы')]
        keyword_callback.assert_has_calls(calls)

    def test_parse_keywords_none(self):
        required_fields = ['адрес']
        keyword_callback = Mock()
        parse_json(self.json_str, required_fields=required_fields,
                   keyword_callback=keyword_callback)
        calls = [call('адрес', 'Ул'), call('адрес', 'Победы'),
                 call('адрес', 'д'), call('адрес', "12")]
        keyword_callback.assert_has_calls(calls)

    def test_parse_handler_none(self):
        required_fields = ['адрес']
        with self.assertRaises(TypeError):
            parse_json(self.json_str, required_fields=required_fields)


unittest.main()
