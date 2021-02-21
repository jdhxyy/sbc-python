# sbc

## 介绍
sbc: struct convert binary.C语言格式结构体和二进制转换库.

本软件包已上传到pypi,可输入命令直接安装:
```shell
pip install sbc
```

## Python和C对应类型
本软件包封装了ctypes,支持cytpes所有类型,对应表如下:

cyteps type|Ctype|Python type
---|---|---
c_bool|_Bool|bool (1)
c_char|char|1-character bytes object
c_wchar|wchar_t|1-character string
c_byte|char|int
c_ubyte|unsigned char|int
c_short|short|int
c_ushort|unsigned|short	int
c_int|int|int
c_uint|unsigned int|int
c_long|long|int
c_ulong|unsigned long|int
c_longlong|__int64 or long long|int
c_ulonglong|unsigned __int64 or unsigned long long|int
c_size_t|size_t|int
c_ssize_t|ssize_t or Py_ssize_t|int
c_float|float|float
c_double|double|float
c_longdouble|long double|float
c_char_p|char * (NUL terminated)|bytes object or None
c_wchar_p|wchar_t * (NUL terminated)|string or None
c_void_p|void *|int or None

## 使用说明
软件包支持4种C语言结构：

类名|说明
---|---
LEFormat|1字节对齐的小端结构体
LEFormatAlign4|4字节对齐的小端结构体
LEFormatAlign8|8字节对齐的小端结构体
BEFormat|1字节对齐的大端结构体
BEFormatAlign4|4字节对齐的大端结构体
BEFormatAlign8|4字节对齐的大端结构体

定义C语言结构体需继承对应的结构体,然后在_fields_中定义对应的成员。示例:
```python
class TStruct1(sbc.LEFormat):
    _fields_ = [
        # (字段名, c类型)
        ('a', sbc.c_uint32),
        ('b', sbc.c_int16),
        ('c', sbc.c_uint8),
    ]
```

C结构体转换为二进制字节流使用方法encode,二进制字节流转换为C语言结构体使用方法decode.API:
```python
"""
C语言格式结构体转换成二进制
:return: 返回二进制字节流
"""
def encode(self) -> bytearray

"""
二进制转换成C语言结构体
:return: 返回True表示转换成功,False表示转换失败
"""
def decode(self, data: bytearray) -> bool

"""
读取结构体字节数
"""
def size(self) -> int
```


## 示例
```python
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
```
