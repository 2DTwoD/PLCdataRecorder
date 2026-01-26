import datetime
import os

from misc.types import VarStruct, MemoryArea
from visu.var_stroke import VarStroke

time_format_for_file_name = '%Y.%m.%d %H-%M-%S-%f'


def get_address_from_var_struct(var_struct: VarStruct):
    result = ""
    result += var_struct.area.value
    if var_struct.area == MemoryArea.DB:
        result += f"{var_struct.db} DBX"
    result += f"{var_struct.byte}.{var_struct.bit}"
    return result


def write_file(plc_name: str, var_stroke: VarStroke):
    error = ""
    vs = var_stroke.var_struct
    try:
        os.makedirs(f"records/{plc_name}/{vs.name}", exist_ok=True)
    except Exception as e:
        error = str(e)
        print(error)
    dt = datetime.datetime.now().strftime(time_format_for_file_name)[: -3]
    with open(f"records/{plc_name}/{vs.name}/{dt}.pdr", "w", encoding="utf-8") as file:
        try:
            file.write(f"Дата: {dt}, ПЛК: {plc_name}, Переменная: {vs.name}, Адрес: {get_address_from_var_struct(vs)}, Тип:{vs.var_type.value}, Смещение: {vs.offset}, Коэффициент: {vs.koef}\n")
            for index, data in enumerate(var_stroke.buffer):
                stroke = f"{index} : {int(data[0] * 1000)} : {data[1]} : {data[2]}\n"
                file.write(stroke)
        except Exception as e:
            error = str(e)
            print(error)
            file.write(error)
    return error
