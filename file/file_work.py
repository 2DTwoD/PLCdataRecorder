import ast
import datetime
import os
import queue

from misc.types import VarStruct, MemoryArea

time_format_for_file_name = '%Y.%m.%d %H-%M-%S-%f'


def get_address_from_var_struct(var_struct: VarStruct):
    result = ""
    result += var_struct.area.value
    if var_struct.area == MemoryArea.DB:
        result += f"{var_struct.db} DBX"
    result += f"{var_struct.byte}.{var_struct.bit}"
    return result


def write_file(plc_name: str, plc_address: str, vs: VarStruct, buffer: queue):
    if len(buffer) == 0:
        return
    error = ""
    try:
        os.makedirs(f"records/{plc_name}/{vs.name}", exist_ok=True)
    except Exception as e:
        error = str(e)
        print(error)

    dt = datetime.datetime.fromtimestamp(buffer[0][0]).strftime(time_format_for_file_name)[: -3]
    with open(f"records/{plc_name}/{vs.name}/{dt} total {len(buffer)}.pdr", "w", encoding="utf-8") as file:
        try:
            file.write(f"Дата: {dt}, ПЛК: {plc_name}{plc_address}, Переменная: {vs.name}, Адрес: {get_address_from_var_struct(vs)}, Тип:{vs.var_type.value}, Смещение: {vs.offset}, Коэффициент: {vs.koef}, Количество измерений: {len(buffer)}\n")
            file.write("Номер: timestamp : Значение : Статус\n")
            for index, data in enumerate(buffer):
                stroke = f"{index + 1} : {int(data[0] * 1000)} : {data[1]} : {data[2]}\n"
                file.write(stroke)
        except Exception as e:
            error = str(e)
            print(error)
            file.write(error)
    return error


def save_config(file_name:str, plc_config, var_config):
    print(file_name)
    print(plc_config)
    print(var_config)
    with open(file_name, "w", encoding="utf-8") as file:
        write_val = {"plc config": plc_config,
                     "var config": var_config}
        file.write(str(write_val))


def read_config(file_name:str):
    with open(file_name, "r", encoding="utf-8") as file:
        file_content = file.read()

    return ast.literal_eval(file_content)
