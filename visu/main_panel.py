import datetime
import threading
import time
from tkinter import ttk, X

from com.connector import Connector
from file.file_work import write_file
from misc.types import VarStruct
from visu.control_panel import ControlPanel
from visu.elements.text_area import TextArea
from visu.plc_panel import PLCpanel
from visu.var_panel import VarPanel


time_format_for_record = '%d.%m.%Y %H:%M:%S:%f'

def getMessage(message):
    if message == '':
        return message
    result = "Ошибка: "
    if len(message) > 2 and message[0:2] == "b'":
        result += message[2: -1]
    else:
        result += message
    return result


class MainPanel(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self._connector = Connector()
        self._thread = None
        self._timer = None

        self._in_process = False

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

    def _checkPLC(self):
        result, error = self._connector.connect(*self.plc_panel.get_address())
        if result:
            result, error = self._connector.checkPLC()
        self._connector.disconnect()
        self.info_area.clearAndInsertText(result)
        self.info_area.insertNewLineText(getMessage(error))

    def _start_record(self, many_times=True):
        if self._thread is not None and self._thread.is_alive():
            print("Уже запущен")
            return

        for var_stroke in self.var_panel.var_strokes:
            var_stroke.buffer.clear()
            var_stroke.calculate_var_struct()

        self._thread = threading.Thread(target=self._record_thread_func, args=(many_times, ), daemon=True)
        self._thread.start()

    def _stop_record(self):
        self._in_process = False

    def _record_thread_func(self, many_times=True):

        if len(self.var_panel.var_strokes) == 0:
            self.info_area.clearAndInsertText("Добавьте переменные для проверки")
            return

        connected, error = self._connector.connect(*self.plc_panel.get_address())
        if not connected:
            self.info_area.clearAndInsertText(getMessage(error))
            return

        period = self.plc_panel.get_period() / 1000.0
        self._in_process = many_times

        self.info_area.clearArea()
        if many_times:
            self.info_area.insertNewLineText("В процессе чтения...")

        self._one_cycle(period)
        while self._in_process:
            pass

        if self._timer is not None:
            self._timer.join()
            self._timer = None

        if many_times:
            for var_stroke in self.var_panel.var_strokes:
                error = write_file(self.plc_panel.get_name(), var_stroke)
                self.info_area.insertNewLineText(error)
            self.info_area.insertNewLineText("Чтение остановлено")

        self._connector.disconnect()

    def _one_cycle(self, period):
        if self._in_process:
            self._timer = threading.Timer(period, self._one_cycle, args=(period, ))
            self._timer.daemon = True
            self._timer.start()

        for var_stroke in self.var_panel.var_strokes:
            vs = var_stroke.var_struct
            value, ts, error = self._connector.getVar(vs)
            if self._timer is not None:
                var_stroke.in_buffer(ts, value, error == "")
            else:
                self.info_area.insertNewLineText(f"{vs.name}: {value} {getMessage(error)}")

            # var_stroke.setActualValue("Ошибка" if error != "" else f"{value}")
