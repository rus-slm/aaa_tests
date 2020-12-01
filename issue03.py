from typing import List, Tuple
import unittest


def fit_transform(*args) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


class Tester(unittest.TestCase):

    def test_cities(self):
        actual = fit_transform(['Moscow', 'London'])
        expected = [('Moscow', [0, 1]), ('London', [1, 0])]
        self.assertEqual(actual, expected)

    def test_countries(self):
        actual = fit_transform(['Russia', 'GB', 'Germany', 'France', 'Russia', 'Russia', 'Netherlands'])
        expected = ('Netherlands', [1, 0, 0, 0, 0])
        self.assertIn(expected, actual)

    def test_not_in(self):
        actual = fit_transform(['Russia', 'GB', 'Germany', 'France', 'Russia', 'Russia', 'Netherlands'])
        expected = ('Morocco', [0, 1, 0, 0, 0])
        self.assertNotIn(expected, actual)

    def test_cities2(self):
        actual = fit_transform(['MSC', 'SPB', 'EKB', 'NNO', 'HIM'])
        expected = [('MSC', [0, 0, 0, 0, 1]),
                    ('SPB', [0, 0, 0, 1, 0]),
                    ('EKB', [0, 0, 1, 0, 0]),
                    ('NNO', [0, 1, 0, 0, 0]),
                    ('HIM', [1, 0, 0, 0, 0])]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
