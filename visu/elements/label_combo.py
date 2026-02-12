from tkinter import ttk, BOTTOM

from visu.elements.frame_with_label import FrameWithLabel


class LabelCombo(FrameWithLabel):
    def __init__(self, master=None, label_text='', combo_list=None, width=0, combo_change_command=lambda e: 0):
        super().__init__(master, label_text, width)
        if combo_list is None:
            combo_list = ['1', '2', '3']

        try:
            self.text_var.set(combo_list[0])
        except Exception as _:
            self.text_var.set('?')

        self.control_widget = ttk.Combobox(self, textvariable=self.text_var, width=self._width, values=combo_list)
        self.control_widget.bind('<<ComboboxSelected>>', combo_change_command)

        self.control_widget.pack(side=BOTTOM)

    def getInt(self):
        try:
            return int(self.get_text())
        except Exception as _:
            return 0
