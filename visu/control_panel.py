from tkinter import ttk, LEFT, X, CENTER, SOLID, BOTH


class ControlPanel(ttk.Frame):
    def __init__(self, master=None, check_plc_command=lambda: 0, check_vars_command=lambda: 0,
                 start_record_command=lambda: 0, stop_record_command=lambda: 0):
        super().__init__(master, padding=10)

        control_label = ttk.Label(self, text="Управление", anchor=CENTER, relief=SOLID)

        button_frame = ttk.Frame(self)
        check_plc_button = ttk.Button(button_frame, text="Проверка связи с ПЛК", command=check_plc_command)
        check_vars_button = ttk.Button(button_frame, text="Проверка переменных", command=check_vars_command)
        start_record_button = ttk.Button(button_frame, text="Начать запись", command=start_record_command)
        stop_record_button = ttk.Button(button_frame, text="Остановить запись", command=stop_record_command)

        check_plc_button.pack(side=LEFT)
        check_vars_button.pack(side=LEFT)
        start_record_button.pack(side=LEFT)
        stop_record_button.pack(side=LEFT)

        control_label.pack(fill=BOTH, pady=5)
        button_frame.pack()
