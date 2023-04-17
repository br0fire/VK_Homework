import unittest
from custom_list import CustomList


class CustomListTest(unittest.TestCase):

    def test_add(self):

        a = CustomList([5, 1, 3, 7])
        b = CustomList([1, 2, 7])

        self.assertEqual(
            list(a + b),
            list(CustomList([6, 3, 10, 7]))
        )

        self.assertEqual(list(a), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(b), list(CustomList([1, 2, 7])))

        self.assertEqual(
            list(b + a),
            list(CustomList([6, 3, 10, 7]))
        )

        self.assertEqual(list(a), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(b), list(CustomList([1, 2, 7])))

        a = CustomList([1])
        b = [2, 5]

        self.assertEqual(list(a + b), list(CustomList([3, 5])))

        self.assertEqual(list(a), list(CustomList([1])))
        self.assertEqual(b, [2, 5])

        self.assertEqual(list(b + a), list(CustomList([3, 5])))

        self.assertEqual(list(a), list(CustomList([1])))
        self.assertEqual(b, [2, 5])

        a = CustomList([5, 4, 7])
        b = [1, 9]

        self.assertEqual(list(a + b), list(CustomList([6, 13, 7])))

        self.assertEqual(list(a), list(CustomList([5, 4, 7])))
        self.assertEqual(b, [1, 9])

        self.assertEqual(list(b + a), list(CustomList([6, 13, 7])))

        self.assertEqual(list(a), list(CustomList([5, 4, 7])))
        self.assertEqual(b, [1, 9])

    def test_sub(self):

        a = CustomList([5, 1, 3, 7])
        b = CustomList([1, 2, 7])

        self.assertEqual(
            list(a - b),
            list(CustomList([4, -1, -4, 7]))
        )

        self.assertEqual(list(a), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(b), list(CustomList([1, 2, 7])))

        self.assertEqual(
            list(b - a),
            list(CustomList([-4, 1, 4, -7]))
        )

        self.assertEqual(list(a), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(b), list(CustomList([1, 2, 7])))

        a = CustomList([1])
        b = [2, 5]

        self.assertEqual(list(a - b), list(CustomList([-1, -5])))

        self.assertEqual(list(a), list(CustomList([1])))
        self.assertEqual(b, [2, 5])

        self.assertEqual(list(b - a), list(CustomList([1, 5])))

        self.assertEqual(list(a), list(CustomList([1])))
        self.assertEqual(b, [2, 5])

        a = CustomList([5, 7, 8])
        b = [6]

        self.assertEqual(list(a - b), list(CustomList([-1, 7, 8])))

        self.assertEqual(list(a), list(CustomList([5, 7, 8])))
        self.assertEqual(b, [6])

        self.assertEqual(list(b - a), list(CustomList([1, -7, -8])))

        self.assertEqual(list(a), list(CustomList([5, 7, 8])))
        self.assertEqual(b, [6])

    def test_cmp(self):
        self.assertTrue(CustomList([1, 2, 3]) == CustomList([6]))
        self.assertFalse(CustomList([1, 2, 3]) != CustomList([6]))
        self.assertTrue(CustomList([1, 2, 3]) > CustomList([2, 3]))
        self.assertTrue(CustomList([1, 2, 3]) >= CustomList([6]))
        self.assertTrue(CustomList([1, 2, 3]) < CustomList([4, 5]))
        self.assertFalse(CustomList([1, 2, 3]) <= CustomList([2]))

    def test_str(self):
        self.assertEqual(str(CustomList([1, 2, 3])), "[1, 2, 3], sum=6")


if __name__ == "__main__":
    unittest.main()
