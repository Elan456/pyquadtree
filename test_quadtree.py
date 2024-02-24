import unittest
from pyquadtree import QuadTree
import random


class AddThenQuery(unittest.TestCase):
    def test_center(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (0, 0))
        value_found = qtree.query((-1, -1, 1, 1))[0].item
        self.assertEqual(value_found, 1)

    def test_top_left(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (-500, 500))
        value_found = qtree.query((-501, 499, -499, 501))[0].item
        self.assertEqual(value_found, 1)

    def test_bottom_right(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (500, -500))
        value_found = qtree.query((499, -501, 501, -499))[0].item
        self.assertEqual(value_found, 1)

    def test_bottom_left(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (-500, -500))
        value_found = qtree.query((-501, -501, -499, -499))[0].item
        self.assertEqual(value_found, 1)

    def test_top_right(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (500, 500))
        value_found = qtree.query((499, 499, 501, 501))[0].item
        self.assertEqual(value_found, 1)

    def test_out_of_bounds(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (500, 500))
        value_found = qtree.query((501, 501, 502, 502))
        self.assertEqual(value_found, [])

    def test_out_of_bounds_negative(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (500, 500))
        value_found = qtree.query((-502, -502, -501, -501))
        self.assertEqual(value_found, [])

    def test_find_out_of_bounds_item(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        qtree.add(1, (600, 600))
        value_found = qtree.query((599, 599, 601, 601))[0].item
        self.assertEqual(value_found, 1)


class AddManyThenLookForEach(unittest.TestCase):
    def test_seed_1(self):
        import random
        random.seed(1)
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        items = []
        for i in range(1000):
            x = random.randint(-500, 500)
            y = random.randint(-500, 500)
            items.append((i, x, y))
            qtree.add(i, (x, y))

        for item in items:
            items_found = qtree.query((item[1] - 1, item[2] - 1, item[1] + 1, item[2] + 1))
            found = False
            for found in items_found:
                if found.item == item[0]:
                    found = True
                    break
            if not found:
                raise AssertionError("Item not found: " + str(item))

    def test_seed_2(self):
        import random
        random.seed(2)
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        items = []
        for i in range(1000):
            x = random.randint(-500, 500)
            y = random.randint(-500, 500)
            items.append((i, x, y))
            qtree.add(i, (x, y))

        for item in items:
            items_found = qtree.query((item[1] - 1, item[2] - 1, item[1] + 1, item[2] + 1))
            found = False
            for found in items_found:
                if found.item == item[0]:
                    found = True
                    break
            if not found:
                raise AssertionError("Item not found: " + str(item))


class AddManyThenQueryForMany(unittest.TestCase):

    def group_query(self):
        qtree = QuadTree((-500, -500, 500, 500), 3, 10)
        items = []
        for i in range(50000):
            x = random.randint(-500, 500)
            y = random.randint(-500, 500)
            items.append((i, x, y))
            qtree.add(i, (x, y))

        # Query an area and check that only the expected items are found
        items_found_full = qtree.query((-30, -30, 30, 30))
        items_expected = []
        for item in items:
            if -30 <= item[1] < 30 and -30 <= item[2] < 30:
                items_expected.append(item[0])

        items_found = [item.item for item in items_found_full]
        items_found.sort()
        items_expected.sort()

        self.assertEqual(items_found, items_expected)

    def test_seed_1(self):
        random.seed(1)
        self.group_query()

    def test_seed_2(self):
        random.seed(2)
        self.group_query()

    def test_seed_3(self):
        random.seed(3)
        self.group_query()


if __name__ == '__main__':
    unittest.main()
