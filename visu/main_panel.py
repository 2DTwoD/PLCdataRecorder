import threading
import time
from tkinter import ttk, X

from com.connector import Connector
from file.file_work import write_file, save_config, read_config
from misc.repeat import Repeat
from misc.types import MutableBool
from visu.control_panel import ControlPanel
from visu.elements.text_area import TextArea
from visu.plc_panel import PLCpanel
from visu.var_panel import VarPanel


time_format_for_record = '%d.%m.%Y %H:%M:%S:%f'

updater_period = 2


def getMessage(message, err_flag=True):
    if message == '':
        return message
    result = ""
    if err_flag:
        result += "Ошибка: "
    if len(message) > 2 and message[0:2] == "b'":
        result += message[2: -1]
    else:
        result += message
    return result


class MainPanel(ttk.Frame):
    def __init__(self, master=None, title: str = 'App'):
        super().__init__(master)

        self.title = title

        self._connector = Connector()
        self._thread = None

        self._in_process = MutableBool()
        self._period = 1
        self._buffer_size = 1
        self._request_count = 0

        self.plc_panel = PLCpanel(self)
        self.control_panel = ControlPanel(self,
                                          check_plc_command=lambda: self._checkPLC(),
                                          check_vars_command=lambda: self._start_record(many_times=False),
                                          start_record_command=lambda: self._start_record(),
                                          stop_record_command=lambda: self._stop_record())
        self.info_area = TextArea(self, height=5)
        self.var_panel = VarPanel(self)

        self.plc_panel.pack(fill=X)
        self.control_panel.pack(fill=X)
        self.info_area.pack(fill=X)
        self.var_panel.pack(fill=X)

        config = read_config(f"{title}.cfg")
        self.plc_panel.set_config(config["plc config"])

        self.lock(False)

        threading.Thread(target=self._updater, daemon=True).start()

    def lock(self, lck):
        self.plc_panel.lock(lck)
        self.control_panel.lock(lck)
        self.var_panel.lock(lck)

    def _updater(self):
        for var_stroke in self.var_panel.var_strokes:
            var_stroke.update_monitor_value()
        time.sleep(updater_period)
        self._updater()

    def _checkPLC(self):
        self.lock(True)
        result, error = self._connector.connect(*self.plc_panel.get_address())
        if result:
            result, error = self._connector.checkPLC()
        self._connector.disconnect()
        self.info_area.clearAndInsertText(result)
        self.info_area.insertNewLineText(getMessage(error))
        self.lock(False)

    def _start_record(self, many_times=True):
        if self._thread is not None and self._thread.is_alive():
            self.info_area.insertNewLineText("Уже запущен")
            return

        for var_stroke in self.var_panel.var_strokes:
            var_stroke.buffer.clear()
            var_stroke.calculate_var_struct()

        self._thread = threading.Thread(target=self._record_thread_func, args=(many_times, ), daemon=True)
        self._thread.start()

    def _stop_record(self):
        self.var_panel.lock(False)
        self._in_process.set(False)

    def _record_thread_func(self, many_times=True):

        if len(self.var_panel.var_strokes) == 0:
            self.info_area.clearAndInsertText("Список переменных пуст")
            return

        self.lock(True)

        connected, error = self._connector.connect(*self.plc_panel.get_address())
        if not connected:
            self.info_area.clearAndInsertText(getMessage(error))
            self.lock(False)
            return

        self._period = self.plc_panel.get_period() / 1000.0
        self._in_process.set(many_times)
        self._buffer_size = self.plc_panel.get_buffer_size()
        self._request_count = 0

        self.info_area.clearArea()

        if many_times:
            self.info_area.insertNewLineText("В процессе чтения...")
            Repeat(self._period, self._one_cycle, self._in_process)
            while self._in_process.get():
                pass
            self._save_data_in_file()
            self.info_area.insertNewLineText("Чтение остановлено")
        else:
            self._one_cycle()
            for var_stroke in self.var_panel.var_strokes:
                error = var_stroke.get_last_error()
                self.info_area.insertNewLineText(f"{var_stroke.get_name()}: {var_stroke.get_last_value()}, Статус: {getMessage(error, error != 'OK')}")
                var_stroke.update_monitor_value()

        self.lock(False)
        self._connector.disconnect()

    def _one_cycle(self):
        for var_stroke in self.var_panel.var_strokes:
            var_stroke.in_buffer(self._connector.getVarMatchCase(var_stroke.var_struct))
        threading.Thread(target=self._after_cycle_action, daemon=True).start()

    def _after_cycle_action(self):
        print(int(1000 * (self.var_panel.get_delta_for_ts())))

        self._request_count += 1
        if self._request_count >= self._buffer_size:
            self._save_data_in_file()
            self._request_count = 0

        if self.var_panel.get_delta_for_ts() > self._period:
            self.info_area.insertNewLineText("Внимание! Время опроса больше периода опроса")

    def _save_data_in_file(self):
        pairs = []
        for var_stroke in self.var_panel.var_strokes:
            pairs.append((var_stroke.var_struct, var_stroke.buffer.copy()))
            var_stroke.buffer.clear()

        for element in pairs:
            error = write_file(self.plc_panel.get_name(), self.plc_panel.get_address_str(), element[0], element[1])
            self.info_area.insertNewLineText(error)

    def on_close(self):
        save_config(f"{self.title}.cfg", self.plc_panel.get_config(), self.var_panel.get_config())
