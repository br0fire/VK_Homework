import unittest
from solve import CustomList


class CustomListTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(
            CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]),
            CustomList([6, 3, 10, 7])
        )
        self.assertEqual(CustomList([1]) + [2, 5], CustomList([3, 5]))
        self.assertEqual([2, 5] + CustomList([1]), CustomList([3, 5]))

    def test_sub(self):
        self.assertEqual(
            CustomList([5, 1, 3, 7]) - CustomList([1, 2, 7]),
            CustomList([4, -1, -4, 7])
        )
        self.assertEqual(CustomList([1]) - [2, 5], CustomList([-1, -5]))
        self.assertEqual([2, 5] - CustomList([1]), CustomList([1, 5]))

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
