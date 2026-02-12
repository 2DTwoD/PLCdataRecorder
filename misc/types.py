from enum import Enum


class VarType(Enum):
    BOOL = 'BOOL'
    BYTE = 'BYTE'
    WORD = 'WORD'
    DWORD = 'DWORD'
    INT = 'INT'
    DINT = 'DINT'
    REAL = 'REAL'


class MemoryArea(Enum):
    DB = 'DB'
    M = 'M'
    I = 'I'
    O = 'O'


class ValidationType(Enum):
    INTEGER = 0
    FLOATING = 1
    IP_ADDRESS = 2
    ANY = 3


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
        elif var_struct is not None and isinstance(var_struct, dict):
            self.name = var_struct['name']
            self.var_type = VarType(var_struct['var_type'])
            self.area = MemoryArea(var_struct['area'])
            self.db = var_struct['db']
            self.byte = var_struct['byte']
            self.bit = var_struct['bit']
            self.offset = var_struct['offset']
            self.koef = var_struct['koef']
        else:
            self.name = 'Переменная 1'
            self.var_type = VarType.BYTE
            self.area = MemoryArea.M
            self.db = 1
            self.byte = 0
            self.bit = 0
            self.offset = 0.0
            self.koef = 1.0

    def get_dict(self):
        return {'name': self.name,
                'var_type': self.var_type.value,
                'area': self.area.value,
                'db': self.db,
                'byte': self.byte,
                'bit': self.bit,
                'offset': self.offset,
                'koef': self.koef
                }


# Не используется
class MutableBool(list):
    def __init__(self, value=False):
        super().__init__()
        self.set(value)

    def get(self):
        return self[0]

    def set(self, value):
        self[0] = value
