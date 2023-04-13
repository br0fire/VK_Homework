import unittest
from descriptors import ChipTantrix


class TestChipTantrix(unittest.TestCase):

    def test_area_positive(self):
        chip = ChipTantrix(5, 1, (True, False, True))
        self.assertEqual(chip.area, 5)
        chip.area = 5.5
        try:
            chip.area = 1.1
        except ValueError:
            self.fail('Float error')

    def test_area_negative(self):
        with self.assertRaises(ValueError):
            _ = ChipTantrix(-5, 1, (True, False, True))

    def test_area_non_numeric(self):
        with self.assertRaises(ValueError):
            _ = ChipTantrix("five", 1, (True, False, True))

    def test_label_valid(self):
        chip = ChipTantrix(5, 1, (True, False, True))
        self.assertEqual(chip.label, 1)

    def test_label_invalid(self):
        with self.assertRaises(ValueError):
            _ = ChipTantrix(5, 11, (True, False, True))

    def test_solid_lines_valid(self):
        chip = ChipTantrix(5, 1, (True, False, True))
        self.assertEqual(chip.solid_lines, (True, False, True))

    def test_solid_lines_invalid_tuple(self):
        with self.assertRaises(ValueError):
            _ = ChipTantrix(5, 1, (True, False))
        with self.assertRaises(ValueError):
            _ = ChipTantrix(5, 1, [True, False, True])

    def test_solid_lines_invalid_boolean(self):
        with self.assertRaises(ValueError):
            _ = ChipTantrix(5, 1, (True, "False", True))


if __name__ == '__main__':
    unittest.main()
