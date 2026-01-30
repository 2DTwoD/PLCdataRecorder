from tkinter import ttk, BOTTOM
import re
from typing import override

from misc.types import ValidationType
from visu.elements.frame_with_label import FrameWithLabel


class LabelEntry(FrameWithLabel):
    def __init__(self, master=None, label_text='', entry_text='', validation_type=ValidationType.INTEGER,
                 low=None, high=None, width=0):
        super().__init__(master, label_text, width)
        match validation_type:
            case ValidationType.INTEGER:
                self.regex = '^\\d*$'
                self.default = '0' if entry_text == '' else entry_text
            case ValidationType.FLOATING:
                self.regex = '^[+-]?(\\d*(\\.\\d*)?|[.]\\d+)$'
                self.default = '0.0' if entry_text == '' else entry_text
            case ValidationType.IP_ADDRESS:
                self.regex = '^(\\d*|\\.*)$'
                self.default = '127.0.0.1' if entry_text == '' else entry_text
                low = None
                high = None
            case ValidationType.ANY:
                self.regex = '^.*$'
                self.default = '-' if entry_text == '' else entry_text
                low = None
                high = None

        self.text_var.set(self.default)
        self.validation_type = validation_type

        self.low = low
        self.high = high
        self.control_widget = ttk.Entry(self, textvariable=self.text_var,
                                        validate='key',
                                        validatecommand=(self.register(self._is_valid), '%S' if validation_type == ValidationType.IP_ADDRESS else '%P'),
                                        width=self._width)

        self.control_widget.pack(side=BOTTOM)

    def _is_valid(self, text):
        return re.match(self.regex, text) is not None

    @override
    def get_text(self):
        value = self.text_var.get()
        if len(value) == 0:
            value = self.default

        match self.validation_type:
            case ValidationType.INTEGER:
                value = int(value)
            case ValidationType.FLOATING:
                value = float(value)

        if self.low is not None:
            value = max(value, self.low)
        if self.high is not None:
            value = min(value, self.high)

        self.set_text(value)
        return self.text_var.get()

    def get_value(self):
        try:
            match self.validation_type:
                case ValidationType.INTEGER:
                    return int(self.get_text())
                case ValidationType.FLOATING:
                    return float(self.get_text())
        except:
            return self.default
        return self.get_text()

    @override
    def set_text(self, value):
        text = str(value)
        if self.validation_type == ValidationType.IP_ADDRESS:
            res = True
            for c in text:
                res &= self._is_valid(c)
                if not res:
                    return
        elif not self._is_valid(text):
            return
        self.text_var.set(text)

