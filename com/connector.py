import time

import snap7
from snap7.util import get_bool, get_real, get_byte, get_int, get_dint, get_word, get_dword

from misc.types import VarType, MemoryArea, VarStruct


def get_plc_state(default_state: str):
    match default_state:
        case 'S7CpuStatusUnknown':
            return 'Неизвестно'
        case 'S7CpuStatusStop':
            return 'Остановлен'
        case 'S7CpuStatusRun':
            return 'Запущен'


def get_final_value(value, var_struct: VarStruct):
    return value * var_struct.koef + var_struct.offset


class Connector:
    def __init__(self):
        self._plc = snap7.client.Client()
        self._connected = False

    def connect(self, ip: str, rack: int, slot: int) -> (bool, str):
        success = True, ''
        if self.connected():
            return success
        try:
            self._plc.connect(ip, rack, slot)
        except Exception as e:
            return False, str(e)
        self._connected = True
        return success

    def disconnect(self):
        if self.disconnected():
            return
        self._connected = False
        self._plc.disconnect()

    def connected(self):
        return self._connected

    def disconnected(self):
        return not self.connected()

    def checkPLC(self):
        result = 'Ошибка!'
        error = ''
        if self.disconnected():
            error = 'Сначала подключитесь к ПЛК'
            return result, error
        try:
            cpu_info = self._plc.get_cpu_info()
            module_type_name = cpu_info.ModuleTypeName.decode('utf-8')
            serial_number = cpu_info.SerialNumber.decode('utf-8')
            as_name = cpu_info.ASName.decode('utf-8')
            module_name = cpu_info.ModuleName.decode('utf-8')
            plc_state = get_plc_state(self._plc.get_cpu_state())
            result = f'Тип модуля: {module_type_name}\nСерийный номер: {serial_number}\nИмя станции: {as_name}\nИмя модуля: {module_name}\nСтатус: {plc_state}'
        except Exception as e:
            error = str(e)
        return result, error

    def getVarMatchCase(self, var_struct: VarStruct):
        result = 0
        error = 'OK'
        if self.disconnected():
            error = 'Сначала подключитесь к ПЛК'
            return time.time(), result, error

        match var_struct.var_type:
            case VarType.BOOL, VarType.BYTE:
                length = 1
            case VarType.INT, VarType.WORD:
                length = 2
            case _:
                length = 4

        try:
            match var_struct.area:
                case MemoryArea.DB:
                    data = self._plc.db_read(var_struct.db, var_struct.byte, length)
                case MemoryArea.M:
                    data = self._plc.mb_read(var_struct.byte, length)
                case MemoryArea.I:
                    data = self._plc.eb_read(var_struct.byte, length)
                case MemoryArea.O:
                    data = self._plc.ab_read(var_struct.byte, length)
                case _:
                    raise Exception('Неизвестная область памяти')
            ts = time.time()

            match var_struct.var_type:
                case VarType.BOOL:
                    result = get_final_value(get_bool(data, 0, var_struct.bit), var_struct)
                case VarType.BYTE:
                    result = get_final_value(get_byte(data, 0), var_struct)
                case VarType.WORD:
                    result = get_final_value(get_word(data, 0), var_struct)
                case VarType.DWORD:
                    result = get_final_value(get_dword(data, 0), var_struct)
                case VarType.INT:
                    result = get_final_value(get_int(data, 0), var_struct)
                case VarType.DINT:
                    result = get_final_value(get_dint(data, 0), var_struct)
                case VarType.REAL:
                    result = get_final_value(get_real(data, 0), var_struct)
                case _:
                    raise Exception('Неизвестный тип переменной')

        except Exception as e:
            error = str(e)
            ts = time.time()
        return ts, result, error

    def getVarIfElse(self, var_struct: VarStruct):
        result = 0
        error = ""
        if self.disconnected():
            error = 'Сначала подключитесь к ПЛК'
            return result, time.time(), error

        if var_struct.var_type == VarType.BOOL:
            length = 1
        elif var_struct.var_type == VarType.INT or var_struct.var_type == VarType.WORD:
            length = 2
        else:
            length = 4

        try:
            if var_struct.area == MemoryArea.DB:
                data = self._plc.db_read(var_struct.db, var_struct.byte, length)
            elif var_struct.area == MemoryArea.M:
                data = self._plc.mb_read(var_struct.byte, length)
            elif var_struct.area == MemoryArea.I:
                data = self._plc.eb_read(var_struct.byte, length)
            elif var_struct.area == MemoryArea.O:
                data = self._plc.ab_read(var_struct.byte, length)
            else:
                raise Exception('Неизвестная область памяти')
            ts = time.time()

            if var_struct.var_type == VarType.BOOL:
                result = get_final_value(get_bool(data, 0, var_struct.bit), var_struct)
            elif var_struct.var_type == VarType.BYTE:
                result = get_final_value(get_byte(data, 0), var_struct)
            elif var_struct.var_type == VarType.WORD:
                result = get_final_value(get_word(data, 0), var_struct)
            elif var_struct.var_type == VarType.DWORD:
                result = get_final_value(get_dword(data, 0), var_struct)
            elif var_struct.var_type == VarType.INT:
                result = get_final_value(get_int(data, 0), var_struct)
            elif var_struct.var_type == VarType.DINT:
                result = get_final_value(get_dint(data, 0), var_struct)
            elif var_struct.var_type == VarType.REAL:
                result = get_final_value(get_real(data, 0), var_struct)
            else:
                raise Exception('Неизвестный тип переменной')

        except Exception as e:
            error = str(e)
            ts = time.time()
        return result, ts, error
