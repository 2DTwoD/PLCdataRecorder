from collections import deque
from tkinter import ttk, LEFT, S, messagebox

from misc.types import VarType, MemoryArea, VarStruct, ValidationType
from visu.elements.label_combo import LabelCombo
from visu.elements.label_entry import LabelEntry
from visu.elements.label_monitor import LabelMonitor


type_list = [VarType.BOOL.value, VarType.BYTE.value, VarType.WORD.value, VarType.DWORD.value,
             VarType.INT.value, VarType.DINT.value, VarType.REAL.value]

area_list = [MemoryArea.DB.value, MemoryArea.M.value, MemoryArea.I.value, MemoryArea.O.value]

bit_list = ['0', '1', '2', '3', '4', '5', '6', '7']


class VarStroke(ttk.Frame):
    def __init__(self, master=None, deleteAction=lambda: 0, var_struct: VarStruct = None):
        super().__init__(master)
        self.buffer = deque()
        self.var_struct = var_struct

        self.name_entry = LabelEntry(self, label_text='Имя переменной', validation_type=ValidationType.ANY,
                                     entry_text='Var' if var_struct is None else var_struct.name, width=20)
        self.type_combo = LabelCombo(self, label_text='Тип', combo_list=type_list, width=13,
                                     combo_change_command=lambda e: self._update_bit_db())
        self.area_combo = LabelCombo(self, label_text='Область', combo_list=area_list,
                                     combo_change_command=lambda e: self._update_bit_db())
        self.db_entry = LabelEntry(self, label_text='Номер DB')
        self.byte_entry = LabelEntry(self, label_text='Байт')
        self.bit_combo = LabelCombo(self, label_text='Бит', combo_list=bit_list)
        self.offset_entry = LabelEntry(self, label_text='Смещение', entry_text='0.0', validation_type=ValidationType.FLOATING)
        self.koef_entry = LabelEntry(self, label_text='Коэффициент', entry_text='1.0', validation_type=ValidationType.FLOATING)
        self.value_monitor = LabelMonitor(self, label_text='Тек. значение')
        self.set_from_var_struct(var_struct)

        def deletecommand():
            if not messagebox.askyesno('Вопрос', f'Удалить строку "{self.get_name()}"?'):
                return
            deleteAction()
            self.destroy()

        self.delete_button = ttk.Button(self, text='Удалить', command=deletecommand, padding=0)

        self.name_entry.pack(side=LEFT)
        self.type_combo.pack(side=LEFT)
        self.area_combo.pack(side=LEFT)
        self.db_entry.pack(side=LEFT)
        self.byte_entry.pack(side=LEFT)
        self.bit_combo.pack(side=LEFT)
        self.offset_entry.pack(side=LEFT)
        self.koef_entry.pack(side=LEFT)
        self.value_monitor.pack(side=LEFT)
        self.delete_button.pack(side=LEFT, anchor=S)

    def calculate_var_struct(self):
        self.var_struct.name = self.name_entry.get_text()
        self.var_struct.var_type = VarType(self.type_combo.get_text())
        self.var_struct.area = MemoryArea(self.area_combo.get_text())
        self.var_struct.db = self.db_entry.get_value()
        self.var_struct.byte = self.byte_entry.get_value()
        self.var_struct.bit = self.bit_combo.getInt()
        self.var_struct.offset = self.offset_entry.get_value()
        self.var_struct.koef = self.koef_entry.get_value()

    def update_monitor_value(self):
        if len(self.buffer) > 0:
            last = self.buffer[-1]
            self.value_monitor.set_text(last[1] if last[2] == 'OK' else 'Ошибка')

    def set_from_var_struct(self, var_struct: VarStruct, copy_name: bool = True):
        if var_struct is not None:
            if copy_name:
                self.name_entry.set_text(var_struct.name)
            self.type_combo.set_text(var_struct.var_type.value)
            self.area_combo.set_text(var_struct.area.value)
            self.db_entry.set_text(var_struct.db)
            self.byte_entry.set_text(var_struct.byte)
            self.bit_combo.set_text(var_struct.bit)
            self.offset_entry.set_text(var_struct.offset)
            self.koef_entry.set_text(var_struct.koef)
        self._update_bit_db()

    def _update_bit_db(self, lck=False):
        self.bit_combo.lock(VarType(self.type_combo.get_text()) != VarType.BOOL or lck)
        self.db_entry.lock(MemoryArea(self.area_combo.get_text()) != MemoryArea.DB or lck)

    def get_name(self):
        return self.name_entry.get_text()

    def get_last_ts(self):
        if len(self.buffer) > 0:
            return self.buffer[-1][0]
        return 0

    def get_last_value(self):
        if len(self.buffer) > 0:
            return self.buffer[-1][1]
        return "-"

    def get_last_error(self):
        if len(self.buffer) > 0:
            return self.buffer[-1][2]
        return "-"

    def lock(self, lck=True):
        self.name_entry.lock(lck)
        self.type_combo.lock(lck)
        self.area_combo.lock(lck)
        self.byte_entry.lock(lck)
        self.offset_entry.lock(lck)
        self.koef_entry.lock(lck)
        self.delete_button.config(state='disabled' if lck else 'normal')
        self._update_bit_db(lck)
