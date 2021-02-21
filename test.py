import sbc

import unittest


class TStruct1(sbc.LEFormat):
    _fields_ = [
        # (字段名, c类型)
        ('a', sbc.c_uint32),
        ('b', sbc.c_int16),
        ('c', sbc.c_uint8),
    ]


class TStruct2(sbc.LEFormatAlign4):
    _fields_ = [
        # (字段名, c类型)
        ('a', sbc.c_uint32),
        ('b', sbc.c_int16),
        ('c', sbc.c_uint8),
    ]


class TStruct3(sbc.BEFormat):
    _fields_ = [
        # (字段名, c类型)
        ('a', sbc.c_uint16),
        ('b', sbc.c_uint8 * 5),
        ('c', sbc.c_uint32),
    ]


class _UnitTest(unittest.TestCase):
    def test_case1(self):
        """
        测试小端1字节对齐,C语言结构体转换为二进制
        """
        ts = TStruct1()
        ts.a = 0x12345678
        ts.b = 0x2345
        ts.c = 0x67
        data = ts.encode()
        self.assertEqual(len(data), 7)
        self.assertEqual(data, bytearray([0x78, 0x56, 0x34, 0x12, 0x45, 0x23, 0x67]))

    def test_case2(self):
        """
        测试小端1字节对齐,二进制转换为C语言结构体
        """
        ts = TStruct1()
        ts.decode(bytearray([0x78, 0x56, 0x34, 0x12, 0x45, 0x23, 0x67]))
        self.assertEqual(ts.a, 0x12345678)
        self.assertEqual(ts.b, 0x2345)
        self.assertEqual(ts.c, 0x67)

    def test_case3(self):
        """
        测试小端4字节对齐,C语言结构体转换为二进制
        """
        ts = TStruct2()
        ts.a = 0x12345678
        ts.b = 0x2345
        ts.c = 0x67
        data = ts.encode()
        self.assertEqual(len(data), 8)
        self.assertEqual(data, bytearray([0x78, 0x56, 0x34, 0x12, 0x45, 0x23, 0x67, 0x00]))

    def test_case4(self):
        """
        测试小端4字节对齐,二进制转换为C语言结构体
        """
        ts = TStruct2()
        ts.decode(bytearray([0x78, 0x56, 0x34, 0x12, 0x45, 0x23, 0x67, 0x00]))
        self.assertEqual(ts.a, 0x12345678)
        self.assertEqual(ts.b, 0x2345)
        self.assertEqual(ts.c, 0x67)

    def test_case5(self):
        """
        测试小端4字节对齐,二进制转换为C语言结构体
        """
        ts = TStruct2()
        err = ts.decode(bytearray([0x78, 0x56, 0x34]))
        self.assertEqual(err, False)

    def test_case6(self):
        """
        测试大端1字节对齐,C语言结构体转换为二进制
        """
        ts = TStruct3()
        ts.a = 0x2345
        for i in range(5):
            ts.b[i] = i
        ts.c = 0x12345678
        data = ts.encode()
        self.assertEqual(len(data), 11)
        self.assertEqual(data, bytearray([0x23, 0x45, 0x00, 0x01, 0x02, 0x03, 0x04, 0x12, 0x34, 0x56, 0x78]))


def print_hex(data):
    for i in data:
        print('%x' % i, end=' ')
    print()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
