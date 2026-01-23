from tkinter import ttk, LEFT, S

from misc.types import VarType, MemoryArea, VarStruct
from visu.elements.label_combo import LabelCombo
from visu.elements.label_entry import LabelEntry, ValidationType
from visu.elements.label_monitor import LabelMonitor


type_list = [VarType.BOOL.value, VarType.BYTE.value, VarType.WORD.value, VarType.DWORD.value
             , VarType.INT.value, VarType.DINT.value, VarType.REAL.value]

area_list = [MemoryArea.DB.value, MemoryArea.M.value, MemoryArea.I.value, MemoryArea.O.value]

bit_list = ["0", "1", "2", "3", "4", "5", "6", "7"]


class VarStroke(ttk.Frame):
    def __init__(self, master=None, deleteAction=lambda: 0, var_struct: VarStruct=None):
        super().__init__(master)
        self.name_entry = LabelEntry(self, label_text="Имя переменной", validation_type=ValidationType.ANY, width=20)
        self.type_combo = LabelCombo(self, label_text="Тип", combo_list=type_list, width=13,
                                     combo_change_command=lambda e: self.update_visible())
        self.area_combo = LabelCombo(self, label_text="Область", combo_list=area_list,
                                     combo_change_command=lambda e: self.update_visible())
        self.db_entry = LabelEntry(self, label_text="Номер DB")
        self.byte_entry = LabelEntry(self, label_text="Байт")
        self.bit_combo = LabelCombo(self, label_text="Бит", combo_list=bit_list)
        self.offset_entry = LabelEntry(self, label_text="Смещение", entry_text='0.0', validation_type=ValidationType.FLOATING)
        self.koef_entry = LabelEntry(self, label_text="Коэффициент", entry_text='1.0', validation_type=ValidationType.FLOATING)
        self.value_monitor = LabelMonitor(self, label_text="Тек. значение")
        self.set_from_var_struct(var_struct)

        def deletecommand():
            deleteAction()
            self.destroy()

        self.delete_button = ttk.Button(self, text="Удалить", command=deletecommand, padding=0)

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

    def get_var_struct(self):
        result = VarStruct()
        result.name = self.name_entry.getText()
        result.var_type = VarType(self.type_combo.getText())
        result.area = MemoryArea(self.area_combo.getText())
        result.db = self.db_entry.getValue()
        result.byte = self.byte_entry.getValue()
        result.bit = self.bit_combo.getInt()
        result.offset = self.offset_entry.getValue()
        result.koef = self.koef_entry.getValue()
        return result

    def setActualValue(self, value):
        self.value_monitor.setText(str(value))

    def set_from_var_struct(self, var_struct: VarStruct, copy_name: bool=True):
        if var_struct is not None:
            if copy_name:
                self.name_entry.setText(var_struct.name)
            self.type_combo.setText(var_struct.var_type.value)
            self.area_combo.setText(var_struct.area.value)
            self.db_entry.setText(var_struct.db)
            self.byte_entry.setText(var_struct.byte)
            self.bit_combo.setText(var_struct.bit)
            self.offset_entry.setText(var_struct.offset)
            self.koef_entry.setText(var_struct.koef)
        self.update_visible()

    def update_visible(self):
        self.bit_combo.lock(VarType(self.type_combo.getText()) != VarType.BOOL)
        self.db_entry.lock(MemoryArea(self.area_combo.getText()) != MemoryArea.DB)

