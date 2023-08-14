import unittest
import pandas as pd
import os


def read_csv_file(file_path):
    return pd.read_csv(file_path)


class TestTableComparison(unittest.TestCase):
    def test_table_comparison(self):
        csv_directory = "test"

        csv_file_1 = os.path.join(csv_directory, "Honda2023data.csv")
        csv_file_2 = os.path.join(csv_directory, "Honda2023-Test.csv")

        table1 = read_csv_file(csv_file_1)
        table2 = read_csv_file(csv_file_2)

        self.assertTrue(table1.equals(table2))


if __name__ == "__main__":
    unittest.main()
