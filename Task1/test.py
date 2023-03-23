import unittest
from unittest import mock
from task1 import SomeModel
from task1 import predict_message_mood
from task2 import filter_gen


class Test1(unittest.TestCase):
    def setUp(self):
        self.model = SomeModel()

    def test_predict_msg_mood_otl(self):
        with mock.patch('task1.SomeModel.predict') as mock_predict:
            mock_predict.return_value = 0.9
            message = 'Привет'
            self.assertEqual(
                predict_message_mood(message, self.model,
                                     bad_thresholds=0.3, good_thresholds=0.8),
                'отл'
            )

    def test_predict_msg_mood_norm(self):
        with mock.patch('task1.SomeModel.predict') as mock_predict:
            mock_predict.return_value = 0.5
            message = 'Привет'
            self.assertEqual(
                predict_message_mood(message, self.model,
                                     bad_thresholds=0.3, good_thresholds=0.8),
                'норм'
            )
            mock_predict.return_value = 0.8
            self.assertEqual(
                predict_message_mood(message, self.model,
                                     bad_thresholds=0.3, good_thresholds=0.8),
                'норм'
            )
            mock_predict.return_value = 0.3
            self.assertEqual(
                predict_message_mood(message, self.model,
                                     bad_thresholds=0.3, good_thresholds=0.8),
                'норм'
            )

    def test_predict_msg_mood_neud(self):
        with mock.patch('task1.SomeModel.predict') as mock_predict:
            mock_predict.return_value = 0.1
            message = 'Привет'
            self.assertEqual(
                predict_message_mood(message, self.model,
                                     bad_thresholds=0.3, good_thresholds=0.8),
                'неуд'
             )


class TestFileSearch(unittest.TestCase):

    def setUp(self):
        self.file = open('input.txt', 'r', encoding="utf-8")

    def test_search_single_word(self):

        search_words = ["коричневая"]
        expected_output = "Быстрая коричневая лиса"
        self.assertEqual(
            next(filter_gen(self.file, search_words)),
            expected_output
        )
        self.file.close()

    def test_search_multiple_words(self):
        search_words = ["мир", "собаку"]
        expected_output = ["Привет мир", "прыгает через ленивую собаку"]
        self.assertEqual(
            next(filter_gen(self.file, search_words)),
            expected_output[0]
        )
        self.assertEqual(
            next(filter_gen(self.file, search_words)),
            expected_output[1]
        )
        self.file.close()

    def test_case_insensitive(self):
        search_words = ["БЫСТРАЯ"]
        expected_output = "Быстрая коричневая лиса"
        self.assertEqual(
            next(filter_gen(self.file, search_words)),
            expected_output
        )
        self.file.close()

    def test_no_match(self):

        search_words = "кошку"
        with self.assertRaises(StopIteration):
            next(filter_gen(self.file, search_words))
        self.file.close()
