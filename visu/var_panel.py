import re

from tkinter import ttk, BOTH, BOTTOM, TOP

from ordered_set import OrderedSet

from misc.types import VarStruct
from visu.var_stroke import VarStroke


class VarPanel(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=10)

        self._counter = 0

        self.var_strokes = OrderedSet()

        var_panels_label = ttk.Label(self, text='Переменные', anchor='center', relief='solid')
        var_panels_label.pack(fill=BOTH, pady=5)

        self.add_var_button = ttk.Button(self, text='Добавить переменную', command=lambda: self._add_var_stroke())

        self.add_var_button.pack(side=BOTTOM, pady=5)

    def _add_var_stroke(self):

        if len(self.var_strokes) > 0:
            self.var_strokes[-1].calculate_var_struct()
            prev_var_struct = VarStruct(self.var_strokes[-1].var_struct)
            search_result = re.search('\\d+$', prev_var_struct.name)
            if search_result is None:
                prev_var_struct.name += ' 1'
            else:
                index = int(search_result.group()) + 1
                prev_var_struct.name = prev_var_struct.name[:search_result.start()] + str(index)
        else:
            prev_var_struct = VarStruct()

        self._add_var_stroke_from_var_struct(prev_var_struct)

    def _add_var_stroke_from_var_struct(self, var_struct: VarStruct):
        var_stroke = VarStroke(self, deleteAction=lambda: self.var_strokes.remove(var_stroke),
                               var_struct=var_struct)

        self.var_strokes.add(var_stroke)
        var_stroke.pack(side=TOP)

    def get_last_ts(self):
        if len(self.var_strokes) > 0:
            return self.var_strokes[-1].get_last_ts()

    def lock(self, lck=True):
        for var_stroke in self.var_strokes:
            var_stroke.lock(lck)
        self.add_var_button.config(state='disabled' if lck else 'normal')

    def get_config(self):
        result = []
        for var_stroke in self.var_strokes:
            var_stroke.calculate_var_struct()
            result.append(var_stroke.var_struct.get_dict())
        return result

    def set_config(self, config):
        try:
            for var_struct_dict in config:
                var_struct = VarStruct(var_struct=var_struct_dict)
                self._add_var_stroke_from_var_struct(var_struct)
        except Exception as e:
            return str(e)
        return ""
