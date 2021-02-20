"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
sbc: struct convert binary.C语言格式结构体和二进制转换库
Authors: jdh99 <jdh821@163.com>
"""

from ctypes import *


def _encode(self) -> bytearray:
    """
    C语言格式结构体转换成二进制
    :return: 返回二进制字节流
    """
    return bytearray(string_at(addressof(self), sizeof(self)))


def _decode(self, data: bytearray):
    """
    二进制转换成C语言结构体
    """
    memmove(addressof(self), bytes(data), sizeof(self))


class LEFormat(LittleEndianStructure):
    _pack_ = 1

    def encode(self) -> bytearray:
        return _encode(self)

    def decode(self, data: bytearray):
        _decode(self, data)


class BEFormat(BigEndianStructure):
    _pack_ = 1

    def encode(self) -> bytearray:
        return _encode(self)

    def decode(self, data: bytearray):
        _decode(self, data)


class LEFormatAlign4(LittleEndianStructure):
    _pack_ = 4

    def encode(self) -> bytearray:
        return _encode(self)

    def decode(self, data: bytearray):
        _decode(self, data)


class BEFormatAlign4(BigEndianStructure):
    _pack_ = 4

    def encode(self) -> bytearray:
        return _encode(self)

    def decode(self, data: bytearray):
        _decode(self, data)


class LEFormatAlign8(LittleEndianStructure):
    _pack_ = 8

    def encode(self) -> bytearray:
        return _encode(self)

    def decode(self, data: bytearray):
        _decode(self, data)


class BEFormatAlign8(BigEndianStructure):
    _pack_ = 8

    def encode(self) -> bytearray:
        return _encode(self)

    def decode(self, data: bytearray):
        _decode(self, data)
