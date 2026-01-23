from enum import Enum


class VarType(Enum):
    BOOL = "BOOL"
    BYTE = "BYTE"
    WORD = "WORD"
    DWORD = "DWORD"
    INT = "INT"
    DINT = "DINT"
    REAL = "REAL"


class MemoryArea(Enum):
    DB = "DB"
    M = "M"
    I = "I"
    O = "O"


class VarStruct:
    name = 'Переменная 1'
    var_type = VarType.BYTE
    area = MemoryArea.M
    db = 1
    byte = 0
    bit = 0
    offset = 0.0
    koef = 1.0
