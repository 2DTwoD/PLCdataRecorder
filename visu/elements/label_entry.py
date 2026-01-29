from enum import Enum
from tkinter import ttk, BOTTOM
import re
from typing import override

from visu.elements.frame_with_label import FrameWithLabel


class ValidationType(Enum):
    INTEGER = 0
    FLOATING = 1
    IP_ADDRESS = 2
    ANY = 3


class LabelEntry(FrameWithLabel):
    def __init__(self, master=None, label_text='', entry_text='', validation_type=ValidationType.INTEGER, low=None, high=None, width=0):
        super().__init__(master, label_text, width)
        match validation_type:
            case ValidationType.INTEGER:
                self.regex = "^\\d*$"
                self.default = '0'
            case ValidationType.FLOATING:
                self.regex = "^[+-]?(\\d*(\\.\\d*)?|[.]\\d+)$"
                self.default = '0.0'
            case ValidationType.IP_ADDRESS:
                self.regex = "^(\\d*|\\.*)$"
                self.default = '127.0.0.1'
                low = None
                high = None
            case ValidationType.ANY:
                self.regex = "^.*$"
                self.default = ''
                low = None
                high = None

        entry_text = self.default if entry_text == '' else entry_text
        self.text_var.set(entry_text)
        self.validation_type = validation_type

        self.low = low
        self.high = high
        self.control_widget = ttk.Entry(self, textvariable=self.text_var,
                                        validate="key",
                                        validatecommand=(self.register(self._is_valid), "%S" if validation_type == ValidationType.IP_ADDRESS else "%P"),
                                        width=self._width)

        self.control_widget.pack(side=BOTTOM)

    def _is_valid(self, text):
        return re.match(self.regex, text) is not None

    @override
    def getText(self):
        value = self.text_var.get()
        if len(value) == 0:
            self.text_var.set(self.default)

        match self.validation_type:
            case ValidationType.INTEGER:
                value = int(value)
            case ValidationType.FLOATING:
                value = float(value)

        if self.low is not None:
            value = max(value, self.low)
        if self.high is not None:
            value = min(value, self.high)
        self.setText(value)
        return self.text_var.get()

    def getValue(self):
        try:
            match self.validation_type:
                case ValidationType.INTEGER:
                    return int(self.getText())
                case ValidationType.FLOATING:
                    return float(self.getText())
        except:
            return self.default
        return self.getText()

    @override
    def setText(self, value):
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

