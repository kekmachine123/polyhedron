import unittest
from math import sqrt, isclose
from common.r3 import R3
from shadow.polyedr import Facet
from tests.matchers import R3ApproxMatcher, R3CollinearMatcher
from shadow.polyedr import Polyedr
from unittest.mock import patch, mock_open


class TestMod(unittest.TestCase):

    def test_mod01(self):  # коробка целиком внутри единичного куба
        fake_file_content = """200.0	60.0	-140.0	60.0
8	5	20
-0.25	-0.25	0.25
-0.25	0.25	0.25
0.25	0.25	0.25
0.25	-0.25	0.25
-0.25	-0.25	-0.25
-0.25	0.25	-0.25
0.25	0.25	-0.25
0.25	-0.25	-0.25
4	1    2    3    4
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5   """
        fake_file_path = 'data/test01.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)
        self.polyedr.shadow()
        self.assertEqual(self.polyedr.p, 0.0)

    def test_mod02(self):  # коробка та же коробка сдвинута вверх
        fake_file_content = """200.0	60.0	-140.0	60.0
8	5	20
-0.25	-0.25	5
-0.25	0.25	5
0.25	0.25	5
0.25	-0.25	5
-0.25	-0.25	4.5
-0.25	0.25	4.5
0.25	0.25	4.5
0.25	-0.25	4.5
4	1    2    3    4
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5   """
        fake_file_path = 'data/test02.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)
        self.polyedr.shadow()
        print(self.polyedr.p)
        self.assertTrue(isclose(self.polyedr.p, 0.3883547522))

    def test_mod03(self):
        fake_file_content = """200.0	60.0	-140.0	60.0
8	5	20
-0.5	-0.5	0.5
-0.5	0.5	0.5
0.5	0.5	0.5
0.5	-0.5	0.5
-0.5	-0.5	-0.5
-0.5	0.5	-0.5
0.5	0.5	-0.5
0.5	-0.5	-0.5
4	1    2    3    4
4	5    6    2    1
4	3    2    6    7
4	3    7    8    4
4	1    4    8    5    """
        fake_file_path = 'data/test03.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)
        self.polyedr.shadow()
        print(self.polyedr.p)
        self.assertTrue(isclose(self.polyedr.p, 0.3883547522 * 2))

    def test_mod04(self):  # пирамида без двух граней, 1 просвет
        fake_file_content = """33 0 0 0
5 3 10
0 0 11
2 0 11
0 2 11
2 2 11
3 1 21
4 1 2 4 3
3 3 4 5
3 1 2 5    """
        fake_file_path = 'data/test04.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)
        self.polyedr.shadow()
        print(self.polyedr.p)
        self.assertTrue(isclose(self.polyedr.p, 2/3))

    def test_mod05(self):  # пирамида без трех граней, 2 просвета на одно ребро
        fake_file_content = """33 0 0 0
5 2 7
0 0 11
2 0 11
0 2 11
2 2 11
3 1 21
4 1 2 4 3
3 3 1 5    """
        fake_file_path = 'data/test05.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)
        self.polyedr.shadow()
        print(self.polyedr.p)
        self.assertTrue(isclose(self.polyedr.p, 4/3))

    def test_mod06(self):  # частично видимое ребро с центром в единичном кубе
        fake_file_content = """33 0 0 0
8 2 8
0.25 1 0
1 1 0
1 -1 0
0.25 -1 0
0 0.5 3
1.5 1.5 3
1.5 -1.5 3
0 -0.5 3
4 1 2 3 4
4 5 6 7 8   """
        fake_file_path = 'data/test06.geom'
        with patch('shadow.polyedr.open'.format(__name__),
                   new=mock_open(read_data=fake_file_content)) as _file:
            self.polyedr = Polyedr(fake_file_path)
            _file.assert_called_once_with(fake_file_path)
        self.polyedr.shadow()
        print(self.polyedr.p)
        self.assertTrue(isclose(self.polyedr.p, 1.0))
