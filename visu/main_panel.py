from tkinter import ttk, X

from com.connector import Connector
from visu.control_panel import ControlPanel
from visu.elements.text_area import TextArea
from visu.plc_panel import PLCpanel
from visu.var_panel import VarPanel


def getMessage(message, error_flag=False):
    if message == '':
        return message
    result = "Ошибка: " if error_flag else ""
    if len(message) > 2 and message[0:2] == "b'":
        result += message[2: -1]
    else:
        result += message
    return result


class MainPanel(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._connector = Connector()

        self.plc_panel = PLCpanel(self)
        self.control_panel = ControlPanel(self,
                                          check_plc_command=lambda: self._checkPLC(),
                                          check_vars_command=lambda: self._getVarFromPLC())
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
        self.info_area.insertNewLineText(getMessage(error, error_flag=True))

    def _getVarFromPLC(self):
        if len(self.var_panel.var_strokes) == 0:
            self.info_area.clearAndInsertText("Добавьте переменные для проверки")
            return
        connected, error = self._connector.connect(*self.plc_panel.get_address())
        if not connected:
            self.info_area.clearAndInsertText(getMessage(error, error_flag=True))
            return
        self.info_area.clearArea()
        for var_stroke in self.var_panel.var_strokes:
            var_struct = var_stroke.get_var_struct()
            value, error = self._connector.getVar(var_struct)
            if error != "":
                var_stroke.setActualValue("Ошибка")
                self.info_area.insertNewLineText(f"{var_struct.name}: {getMessage(error, error_flag=True)}")
            else:
                var_stroke.setActualValue(value)
                self.info_area.insertNewLineText(f"{var_struct.name}: {value} OK")
        self._connector.disconnect()
