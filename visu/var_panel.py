import re
from collections import deque
from tkinter import ttk, BOTH, BOTTOM, TOP

from ordered_set import OrderedSet

from misc.types import VarStruct
from visu.var_stroke import VarStroke


class VarPanel(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=10)

        self._counter = 0

        self.var_strokes = OrderedSet()

        var_panels_label = ttk.Label(self, text="Переменные", anchor="center", relief="solid")
        var_panels_label.pack(fill=BOTH, pady=5)

        self.add_var_button = ttk.Button(self, text="Добавить переменную", command=lambda: self._add_var_stroke())

        self.add_var_button.pack(side=BOTTOM, pady=5)

        # for _ in range(10):
        #     self._add_var_stroke()

    def _add_var_stroke(self):

        if len(self.var_strokes) > 0:
            prev_var_struct = VarStruct(self.var_strokes[-1].var_struct)
            search_result = re.search("\\d+$", prev_var_struct.name)
            if search_result is None:
                prev_var_struct.name += ' 1'
            else:
                index = int(search_result.group()) + 1
                prev_var_struct.name = prev_var_struct.name[:search_result.start()] + str(index)
        else:
            prev_var_struct = VarStruct()

        var_stroke = VarStroke(self, deleteAction=lambda: self.var_strokes.remove(var_stroke),
                               var_struct=prev_var_struct)

        self._prev_var_stroke = var_stroke

        self.var_strokes.add(var_stroke)
        var_stroke.pack(side=TOP)

    def get_delta_for_ts(self):
        if len(self.var_strokes) > 0:
            return self.var_strokes[-1].get_last_ts() - self.var_strokes[0].get_last_ts()

    def lock(self, lck=True):
        for var_stroke in self.var_strokes:
            var_stroke.lock(lck)
        self.add_var_button.config(state="disabled" if lck else "normal")

    def get_config(self):
        result = []
        for var_stroke in self.var_strokes:
            config = {"name": var_stroke.name_entry.getText(),
                      "type": var_stroke.type_combo.getText(),
                      "area": var_stroke.area_combo.getText(),
                      "db": var_stroke.db_entry.getText(),
                      "byte": var_stroke.byte_entry.getText(),
                      "bit": var_stroke.bit_combo.getText(),
                      "offset": var_stroke.offset_entry.getText(),
                      "koef": var_stroke.koef_entry.getText()}
            result.append(config)
        return result
