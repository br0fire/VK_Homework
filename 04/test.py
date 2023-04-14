import unittest
from descriptors import ChipTantrix
from metaclass import CustomClass


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


class TestCustomClass(unittest.TestCase):

    def setUp(self):
        self.inst = CustomClass()

    def test_custom_x(self):
        self.assertEqual(CustomClass.custom_x, 50)

    def test_custom_class_x(self):
        with self.assertRaises(AttributeError):
            self.inst.x

    def test_custom_val(self):
        self.assertEqual(self.inst.custom_val, 99)

    def test_custom_line(self):
        self.assertEqual(self.inst.custom_line(), 100)

    def test_str(self):
        self.assertEqual(str(self.inst), "Custom_by_metaclass")

    def test_inst_x(self):
        with self.assertRaises(AttributeError):
            self.inst.x

    def test_inst_val(self):
        with self.assertRaises(AttributeError):
            self.inst.val

    def test_inst_line(self):
        with self.assertRaises(AttributeError):
            self.inst.line()

    def test_inst_yyy(self):
        with self.assertRaises(AttributeError):
            self.inst.yyy

    def test_dynamic(self):
        self.inst.dynamic = "added later"
        self.assertEqual(self.inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            self.inst.dynamic


if __name__ == '__main__':
    unittest.main()
