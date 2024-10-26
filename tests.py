'''
Так как я никогда не писала тестов, их писал ChatGPT на основе кода из chunk_module.py
Я попыталась разобраться, как это работает, и немного подкорректировала.
'''

import unittest
import pandas as pd
from chunk_module import chunk_cutting


class TestChunkCutting(unittest.TestCase):
    def setUp(self):
        # Создаем фиксированные данные для тестирования
        self.dates = pd.date_range("2023-01-01 00:00:00", "2023-01-01 00:00:05", freq="s")
        self.random_counts = [3, 2, 1, 4, 2, 3]  # фиксированные размеры для каждой даты
        self.df = pd.DataFrame({"dt": self.dates.repeat(self.random_counts)})

    def test_basic_chunking(self):
        """Тестируем, что функция корректно разбивает фрейм на чанки"""
        chunk_size = 6
        result = chunk_cutting(self.df, chunk_size=chunk_size)

        # Проверяем, что результат состоит из списка списков
        self.assertIsInstance(result, list)
        for chunk in result:
            self.assertIsInstance(chunk, list)

    def test_chunk_sizes(self):
        """Тестируем, что каждый чанк имеет размер не меньше указанного chunk_size (кроме последнего чанка)"""
        chunk_size = 6
        result = chunk_cutting(self.df, chunk_size=chunk_size)

        for chunk in result[:-1]:  # Проверяем все чанки, кроме последнего
            self.assertGreaterEqual(sum(len(group) for group in chunk), chunk_size)

    def test_chunk_combination(self):
        """Тестируем, что все группы суммируются обратно в исходный DataFrame"""
        chunk_size = 6
        result = chunk_cutting(self.df, chunk_size=chunk_size)

        combined_df = pd.concat([pd.concat(chunk) for chunk in result]).reset_index(drop=True)
        pd.testing.assert_frame_equal(self.df.reset_index(drop=True), combined_df)

    def test_empty_dataframe(self):
        """Тестируем работу функции с пустым DataFrame"""
        empty_df = pd.DataFrame({"dt": pd.to_datetime([])})
        result = chunk_cutting(empty_df, chunk_size=6)
        self.assertEqual(result, [], "Результат должен быть пустым списком")

    def test_small_chunk_size(self):
        """Тестируем, когда размер чанка меньше, чем любая из групп"""
        chunk_size = 1
        result = chunk_cutting(self.df, chunk_size=chunk_size)

        # Должен быть чанк для каждой группы, так как chunk_size=1
        self.assertEqual(len(result), len(self.df["dt"].unique()))


if __name__ == "__main__":
    unittest.main()
