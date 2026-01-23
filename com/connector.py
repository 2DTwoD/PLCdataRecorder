import snap7
from snap7.util import get_bool, get_real, get_byte, get_int, get_dint, get_word, get_dword

from misc.types import VarType, MemoryArea, VarStruct


def getPLCState(default_state: str):
    match default_state:
        case "S7CpuStatusUnknown":
            return "Неизвестно"
        case "S7CpuStatusStop":
            return "Остановлен"
        case "S7CpuStatusRun":
            return "Запущен"


def getFinalValue(value, var_struct: VarStruct):
    return value * var_struct.koef + var_struct.offset


class Connector:
    def __init__(self):
        self._plc = snap7.client.Client()
        self._connected = False
        # plc.connect('192.168.213.130', 0, 1)
        # start_time = time.time()
        # for i in range(100):
        #     mb20 = plc.mb_read(20, 1)
        #     db = plc.db_read(1, 0, 1)
        # print(f"Время выполнения функции: {time.time() - start_time} секунд, результат: {mb20}, {db}")
        # plc.disconnect()

    def connect(self, ip: str, rack: int, slot: int) -> (bool, str):
        success = True, ""
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
        result = "Ошибка!"
        error = ""
        if self.disconnected():
            error = "Сначала подключитесь к ПЛК"
            return result, error
        try:
            cpu_info = self._plc.get_cpu_info()
            module_type_name = cpu_info.ModuleTypeName.decode("utf-8")
            serial_number = cpu_info.SerialNumber.decode('utf-8')
            as_name = cpu_info.ASName.decode('utf-8')
            module_name = cpu_info.ModuleName.decode('utf-8')
            plc_state = getPLCState(self._plc.get_cpu_state())
            result = f'Тип модуля: {module_type_name}, Серийный номер: {serial_number}, Имя станции: {as_name}, Имя модуля: {module_name}\nСтатус: {plc_state}'
        except Exception as e:
            error = str(e)
        return result, error

    def getVar(self, var_struct: VarStruct):
        result = 0
        error = ""
        if self.disconnected():
            error = "Сначала подключитесь к ПЛК"
            return result, error

        len = 4
        match var_struct.var_type:
            case VarType.BOOL, VarType.BYTE:
                len = 1
            case VarType.WORD, VarType.INT:
                len = 2

        try:
            match var_struct.area:
                case MemoryArea.DB:
                    data = self._plc.db_read(var_struct.db, var_struct.byte, len)
                case MemoryArea.M:
                    data = self._plc.mb_read(var_struct.byte, len)
                case MemoryArea.I:
                    data = self._plc.eb_read(var_struct.byte, len)
                case MemoryArea.O:
                    data = self._plc.ab_read(var_struct.byte, len)
                case _:
                    raise Exception("Неизвестная область памяти")

            match var_struct.var_type:
                case VarType.BOOL:
                    result = getFinalValue(get_bool(data, 0, var_struct.bit), var_struct)
                case VarType.BYTE:
                    result = getFinalValue(get_byte(data, 0), var_struct)
                case VarType.WORD:
                    result = getFinalValue(get_word(data, 0), var_struct)
                case VarType.DWORD:
                    result = getFinalValue(get_dword(data, 0), var_struct)
                case VarType.INT:
                    result = getFinalValue(get_int(data, 0), var_struct)
                case VarType.DINT:
                    result = getFinalValue(get_dint(data, 0), var_struct)
                case VarType.REAL:
                    result = getFinalValue(get_real(data, 0), var_struct)
                case _:
                    raise Exception("Неизвестный тип переменной")

        except Exception as e:
            error = str(e)
        return result, error

