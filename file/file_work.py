import ast
import datetime
import os
import queue

from misc.types import VarStruct, MemoryArea

time_format_for_file_name = '%d.%m.%Y %H-%M-%S-%f'
time_format_for_save_timestamp = '%d.%m.%Y %H:%M:%S.%f'
file_extension_for_data = 'trnd'


def get_address_from_var_struct(var_struct: VarStruct):
    result = ''
    result += var_struct.area.value
    if var_struct.area == MemoryArea.DB:
        result += f'{var_struct.db} DBX'
    result += f'{var_struct.byte}.{var_struct.bit}'
    return result


def write_file(plc_name: str, plc_address: str,  period: str, vs: VarStruct, buffer: queue):
    pass
    if len(buffer) == 0:
        return
    error = ''
    try:
        os.makedirs(f'records/{plc_name}/{vs.name}', exist_ok=True)
    except Exception as e:
        return str(e)

    dt = datetime.datetime.fromtimestamp(buffer[0][0]).strftime(time_format_for_file_name)[: -3]
    try:
        f = open(f'records/{plc_name}/{vs.name}/{dt} total {len(buffer)}.{file_extension_for_data}', 'w', encoding='utf-8')
        try:
            f.write(
                f'Дата: {dt}; ПЛК: {plc_name}{plc_address}; Переменная: {vs.name}; Адрес: {get_address_from_var_struct(vs)}; Тип:{vs.var_type.value}; Смещение: {vs.offset}; Коэффициент: {vs.koef}; Количество измерений: {len(buffer)}; Период опроса (мс): {period}\n')
            f.write('Номер | Timestamp | Дата/время | Значение | Статус\n')
            for index, data in enumerate(buffer):
                stroke = f'{index + 1} | {data[0]} | {datetime.datetime.fromtimestamp(data[0]).strftime(time_format_for_save_timestamp)[:-3]} | {data[1]} | {data[2]}\n'
                f.write(stroke)
        except Exception as e:
            error = str(e)
            f.write(error)
        finally:
            f.close()
    except Exception as e:
        error = str(e)
    return error


def save_config(file_name: str, plc_config, var_config):
    error = ''
    try:
        f = open(file_name, 'w', encoding='utf-8')
        try:
            write_val = {'plc config': plc_config,
                         'var config': var_config}
            f.write(str(write_val))
        except Exception as e:
            error = str(e)
        finally:
            f.close()
    except Exception as e:
        error = str(e)
    return error


def read_config(file_name: str):
    result = None
    error = ''
    try:
        f = open(file_name, 'r', encoding='utf-8')
        try:
            file_content = f.read()
            result = ast.literal_eval(file_content)
        except Exception as e:
            error = str(e)
        finally:
            f.close()
    except Exception as e:
        error = str(e)
    return result, error
