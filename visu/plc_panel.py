from tkinter import ttk, LEFT, BOTH, CENTER, SOLID

from visu.elements.label_entry import LabelEntry
from misc.types import ValidationType


class PLCpanel(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=10)

        panel_label = ttk.Label(self, text='Настройки ПЛК (Siemens S7-300/400/1200/1500)', anchor=CENTER, relief=SOLID)

        entry_frame = ttk.Frame(self, padding=5)
        self.name_entry = LabelEntry(entry_frame, label_text='Название ПЛК', validation_type=ValidationType.ANY,
                                     width=15, entry_text='ПЛК')
        self.ip_entry = LabelEntry(entry_frame, label_text='IP адрес', validation_type=ValidationType.IP_ADDRESS,
                                   width=15, entry_text='192.168.0.1')
        self.rack_entry = LabelEntry(entry_frame, label_text='Рейка')
        self.slot_entry = LabelEntry(entry_frame, label_text='Слот', entry_text='1')
        self.period_entry = LabelEntry(entry_frame, label_text='Период опроса, мс', entry_text='1000',
                                       low=10, high=3600000)
        self.buffer_entry = LabelEntry(entry_frame, label_text='Буфер для записи', entry_text='3600',
                                       low=100, high=100000)
        self.name_entry.pack(side=LEFT)
        self.ip_entry.pack(side=LEFT)
        self.rack_entry.pack(side=LEFT)
        self.slot_entry.pack(side=LEFT)
        self.period_entry.pack(side=LEFT)
        self.buffer_entry.pack(side=LEFT)

        panel_label.pack(fill=BOTH, pady=5)
        entry_frame.pack()

    def get_address(self):
        return self.ip_entry.get_value(), self.rack_entry.get_value(), self.slot_entry.get_value()

    def get_period(self):
        return self.period_entry.get_value()

    def get_buffer_size(self):
        return self.buffer_entry.get_value()

    def get_name(self):
        return self.name_entry.get_text()

    def get_address_str(self):
        return str(self.get_address())

    def lock(self, lck):
        self.name_entry.lock(lck)
        self.ip_entry.lock(lck)
        self.rack_entry.lock(lck)
        self.slot_entry.lock(lck)
        self.period_entry.lock(lck)
        self.buffer_entry.lock(lck)

    def get_config(self):
        return {"name": self.name_entry.get_text(),
                "ip": self.ip_entry.get_text(),
                "rack": self.rack_entry.get_text(),
                "slot": self.slot_entry.get_text(),
                "period": self.period_entry.get_text(),
                "buffer": self.buffer_entry.get_text()}

    def set_config(self, config):
        try:
            self.name_entry.set_text(config["name"])
            self.ip_entry.set_text(config["ip"])
            self.rack_entry.set_text(config["rack"])
            self.slot_entry.set_text(config["slot"])
            self.period_entry.set_text(config["period"])
            self.buffer_entry.set_text(config["buffer"])
        except Exception as e:
            return str(e)
        return ""
