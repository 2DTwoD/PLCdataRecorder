from tkinter import ttk, BOTTOM

from visu.elements.frame_with_label import FrameWithLabel


class LabelMonitor(FrameWithLabel):
    def __init__(self, master=None, label_text='', width=0):
        super().__init__(master, label_text, width)

        self.lock = lambda slf, lck: 0

        self.text_var.set('-')
        self.control_widget = ttk.Entry(self, textvariable=self.text_var, width=self._width, state='readonly')

        self.control_widget.pack(side=BOTTOM)
