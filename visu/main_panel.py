import threading
import time
from collections import deque
from tkinter import ttk, X

from com.connector import Connector
from visu.control_panel import ControlPanel
from visu.elements.text_area import TextArea
from visu.plc_panel import PLCpanel
from visu.var_panel import VarPanel


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
        self._in_process = False

        self.plc_panel = PLCpanel(self)
        self.control_panel = ControlPanel(self,
                                          check_plc_command=lambda: self._checkPLC(),
                                          check_vars_command=lambda: self._start_record(once=True),
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

    def _start_record(self, once=False):
        if self._thread is not None and self._thread.is_alive():
            print("Уже запущен")
            return
        self._thread = threading.Thread(target=self._record_thread_func, args=(once, ), daemon=True)
        self._thread.start()

    def _stop_record(self):
        self._in_process = False

    def _record_thread_func(self, once):

        if len(self.var_panel.var_strokes) == 0:
            self.info_area.clearAndInsertText("Добавьте переменные для проверки")
            return

        connected, error = self._connector.connect(*self.plc_panel.get_address())
        if not connected:
            self.info_area.clearAndInsertText(getMessage(error))
            return

        self._in_process = True

        self.info_area.clearArea()
        if not once:
            self.info_area.insertNewLineText("В процессе чтения...")

        while self._in_process:
            for var_stroke in self.var_panel.var_strokes:

                var_struct = var_stroke.get_var_struct()
                value, error = self._connector.getVar(var_struct)

                if error != "":
                    var_stroke.setActualValue("Ошибка")
                    if once:
                        self.info_area.insertNewLineText(f"{var_struct.name}: {getMessage(error)}")
                else:
                    var_stroke.setActualValue(value)
                    var_stroke.in_buffer(value)
                    if once:
                        self.info_area.insertNewLineText(f"{var_struct.name}: {value} OK")
            if once:
                self._in_process = False
                break
            time.sleep(self.plc_panel.get_period() / 1000.0)
        if not once:
            self.info_area.clearAndInsertText("Чтение остановлено")
        self._connector.disconnect()

