"""Бастапқы қателерді дәлелдеу және түзетулерді автоматты тексеру."""

import importlib.util
from pathlib import Path
import unittest


def load_program(filename):
    """Нөмірден басталатын файлды негізгі сценарийін орындамай жүктеу."""
    spec = importlib.util.spec_from_file_location(filename, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


buggy = load_program("01_buggy.py")
fixed = load_program("02_fixed.py")


class OriginalErrorsTests(unittest.TestCase):
    """Үш бастапқы қатенің қайталанатынын көрсету."""

    def test_empty_average_crashes(self):
        with self.assertRaises(ZeroDivisionError):
            buggy.average([])

    def test_discount_is_incorrect(self):
        self.assertEqual(buggy.final_price(1000, 20), -19000)

    def test_negative_maximum_is_incorrect(self):
        self.assertEqual(buggy.maximum([-8, -3, -5]), 0)


class FixedProgramTests(unittest.TestCase):
    """Қалыпты, шекаралық және қате кіріс мәндерін тексеру."""

    def test_average(self):
        self.assertEqual(fixed.average([10, 20, 30]), 20)

    def test_empty_average(self):
        with self.assertRaisesRegex(ValueError, "кемінде бір сан"):
            fixed.average([])

    def test_discount(self):
        self.assertEqual(fixed.final_price(1000, 20), 800)

    def test_discount_boundaries(self):
        self.assertEqual(fixed.final_price(1000, 0), 1000)
        self.assertEqual(fixed.final_price(1000, 100), 0)

    def test_invalid_discount(self):
        for price, percent in [(-1, 20), (1000, -1), (1000, 101)]:
            with self.subTest(price=price, percent=percent):
                with self.assertRaises(ValueError):
                    fixed.final_price(price, percent)

    def test_negative_maximum(self):
        self.assertEqual(fixed.maximum([-8, -3, -5]), -3)

    def test_positive_maximum(self):
        self.assertEqual(fixed.maximum([4, 9, 2]), 9)

    def test_single_maximum(self):
        self.assertEqual(fixed.maximum([-5]), -5)

    def test_empty_maximum(self):
        with self.assertRaises(ValueError):
            fixed.maximum([])


if __name__ == "__main__":
    unittest.main(verbosity=2)
