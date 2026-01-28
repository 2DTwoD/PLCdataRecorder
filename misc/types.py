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
    def __init__(self, var_struct=None):
        if var_struct is not None and isinstance(var_struct, VarStruct):
            self.name = var_struct.name
            self.var_type = var_struct.var_type
            self.area = var_struct.area
            self.db = var_struct.db
            self.byte = var_struct.byte
            self.bit = var_struct.bit
            self.offset = var_struct.offset
            self.koef = var_struct.koef
        else:
            self.name = 'Переменная 1'
            self.var_type = VarType.BYTE
            self.area = MemoryArea.M
            self.db = 1
            self.byte = 20
            self.bit = 0
            self.offset = 0.0
            self.koef = 1.0


class MutableBool(list):
    def __init__(self, value=False):
        super().__init__()
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
