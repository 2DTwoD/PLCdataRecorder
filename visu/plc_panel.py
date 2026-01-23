from tkinter import ttk, LEFT, BOTH, CENTER, SOLID

from com.connector import Connector
from visu.elements.label_entry import LabelEntry, ValidationType
from visu.elements.text_area import TextArea
from visu.var_stroke import VarStroke


def getErrorMessage(message):
    if len(message) > 2 or message[0:2] == "b'":
        return message[2: -1]
    return message


class PLCpanel(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=10)

        panel_label = ttk.Label(self, text="Настройки ПЛК", anchor=CENTER, relief=SOLID)

        entry_frame = ttk.Frame(self, padding=5)
        self.name_entry = LabelEntry(entry_frame, label_text="Название ПЛК", validation_type=ValidationType.ANY,
                                width=15, entry_text='ПЛК1')
        self.ip_entry = LabelEntry(entry_frame, label_text="IP адрес", validation_type=ValidationType.IP_ADDRESS,
                                   width=15, entry_text='192.168.213.130')
        self.rack_entry = LabelEntry(entry_frame, label_text="Рейка")
        self.slot_entry = LabelEntry(entry_frame, label_text="Слот", entry_text='1')
        self.period_entry = LabelEntry(entry_frame, label_text="Период опроса, мс", entry_text='1000')
        self.buffer_entry = LabelEntry(entry_frame, label_text="Буфер для записи", entry_text='3600')
        self.name_entry.pack(side=LEFT)
        self.ip_entry.pack(side=LEFT)
        self.rack_entry.pack(side=LEFT)
        self.slot_entry.pack(side=LEFT)
        self.period_entry.pack(side=LEFT)
        self.buffer_entry.pack(side=LEFT)

        panel_label.pack(fill=BOTH, pady=5)
        entry_frame.pack()

    def get_address(self):
        return self.ip_entry.getValue(), self.rack_entry.getValue(), self.slot_entry.getValue()

    def get_period(self):
        return self.period_entry.getValue()
