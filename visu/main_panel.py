import threading
import time
from tkinter import ttk, X, messagebox

import schedule

from com.connector import Connector
from file.file_work import write_file, save_config, read_config
from visu.control_panel import ControlPanel
from visu.elements.text_area import TextArea
from visu.plc_panel import PLCpanel
from visu.var_panel import VarPanel


def get_message(message, err_flag=True):
    if message == '':
        return message
    result = ''
    if err_flag:
        result += 'Ошибка: '
    if len(message) > 2 and message[0:2] == "b'":
        result += message[2: -1]
    else:
        result += message
    return result


class MainPanel(ttk.Frame):
    def __init__(self, master=None, title: str = 'App', updater_period=1):
        super().__init__(master)

        self._title = title
        self._updater_period = updater_period

        self._connector = Connector()
        self._thread = None

        self._in_process = False
        self._period = 1
        self._buffer_size = 1
        self._request_count = 0

        self.plc_panel = PLCpanel(self)
        self.control_panel = ControlPanel(self,
                                          check_plc_command=self._check_plc,
                                          check_vars_command=lambda: self._start_record(many_times=False),
                                          start_record_command=self._start_record,
                                          stop_record_command=self._stop_record)
        self.info_area = TextArea(self, height=9)
        clear_button = ttk.Button(self, text='Очистить поле вывода', command=self._clear_info)
        self.var_panel = VarPanel(self)

        self.plc_panel.pack(fill=X)
        self.control_panel.pack(fill=X)
        self.info_area.pack(fill=X)
        clear_button.pack(fill=X)
        self.var_panel.pack(fill=X)

        config, error = read_config(f'{title}.cfg')
        try:
            if config is not None and error == '':
                self.plc_panel.set_config(config['plc config'])
                self.var_panel.set_config(config['var config'])
        except Exception as e:
            error = str(e)
        self.info_area.insert_new_line_text(get_message(error))

        self.lock(False)

        threading.Thread(target=self._updater, daemon=True).start()

    def lock(self, lck):
        self.plc_panel.lock(lck)
        self.control_panel.lock(lck)
        self.var_panel.lock(lck)

    def _updater(self):
        while True:
            for var_stroke in self.var_panel.var_strokes:
                var_stroke.update_monitor_value()
            time.sleep(self._updater_period)

    def _connect(self):
        self.lock(True)
        self.info_area.clear_area()

        connected, error = self._connector.connect(*self.plc_panel.get_address())
        if connected:
            self.info_area.insert_new_line_text(
                f'Соединение с ПЛК "{self.plc_panel.get_name()}"{self.plc_panel.get_address()} установлено')
        else:
            self.lock(False)
            self.info_area.insert_new_line_text(get_message(error))
        return connected

    def _disconnect(self):
        self.lock(False)
        self._connector.disconnect()
        self.info_area.insert_new_line_text(
            f'Соединение с ПЛК "{self.plc_panel.get_name()}"{self.plc_panel.get_address()} разорвано')

    def _check_plc(self):
        if not self._connect():
            return
        result, error = self._connector.checkPLC()
        self.info_area.insert_new_line_text(result, date_flag=False)
        self.info_area.insert_new_line_text(get_message(error))
        self._disconnect()

    def _start_record(self, many_times=True):
        if many_times and not messagebox.askyesno('Вопрос', 'Начать запись переменных?'):
            return
        if self._thread is not None and self._thread.is_alive():
            self.info_area.insert_new_line_text('Уже запущен')
            return
        self._thread = threading.Thread(target=self._record_thread_func, args=(many_times, ), daemon=True)
        self._thread.start()

    def _stop_record(self, ask_flag=True):
        if ask_flag and not messagebox.askyesno('Вопрос', 'Остановить запись переменных?'):
            return
        self._in_process = False

    def _record_thread_func(self, many_times=True):
        if len(self.var_panel.var_strokes) == 0:
            self.info_area.clear_and_insert_text('Список переменных пуст')
            return

        if not self._connect():
            return

        self._period = self.plc_panel.get_period() / 1000.0
        self._in_process = many_times
        self._buffer_size = self.plc_panel.get_buffer_size()
        self._request_count = 0

        for var_stroke in self.var_panel.var_strokes:
            var_stroke.buffer.clear()
            var_stroke.calculate_var_struct()

        if many_times:
            self.info_area.insert_new_line_text('В процессе чтения...')
            self._one_cycle()
            self._repeat_schedule()
            self.info_area.insert_new_line_text('Чтение остановлено')
            self._save_data_in_file()
        else:
            start = self._one_cycle()
            for var_stroke in self.var_panel.var_strokes:
                error_msg = var_stroke.get_last_error()
                error = error_msg != 'OK'
                var_stroke.set_monitor_color(foreground='red' if error else '')
                self.info_area.insert_new_line_text(f'{var_stroke.get_name()}: {var_stroke.get_last_value()}, Статус: {get_message(error_msg, error)}',
                                                    date_flag=False)
                var_stroke.update_monitor_value()

            delta = self.var_panel.get_last_ts() - start
            self.info_area.insert_new_line_text(f'Время опроса: {delta * 1000} мс', date_flag=False)

        self._disconnect()

    def _one_cycle(self):
        start = time.time()
        for var_stroke in self.var_panel.var_strokes:
            var_stroke.in_buffer(self._connector.getVarMatchCase(var_stroke.var_struct))
        threading.Thread(target=self._after_cycle_action, args=(start, ), daemon=True).start()
        return start

    def _repeat_schedule(self):
        schedule.every(self._period).seconds.do(self._one_cycle)
        while self._in_process:
            schedule.run_pending()
        schedule.clear()

    # def _repeat_sleep(self):
    #     while self._in_process:
    #         time.sleep(self._period - time.time() + self._one_cycle())

    def _after_cycle_action(self, start):
        self._request_count += 1
        if self._request_count >= self._buffer_size:
            self._request_count = 0
            self._save_data_in_file()

        delta = self.var_panel.get_last_ts() - start
        if delta > self._period:
            self.info_area.insert_new_line_text(f'Внимание! Время опроса({delta * 1000} мс) больше периода опроса({self._period * 1000} мс)')
        # print(1000 * delta)

    def _save_data_in_file(self):
        self.info_area.insert_new_line_text('Начало записи переменных на диск')
        pairs = []
        for var_stroke in self.var_panel.var_strokes:
            pairs.append((var_stroke.var_struct, var_stroke.buffer.copy()))
            var_stroke.buffer.clear()

        error = ''
        for element in pairs:
            error = write_file(self.plc_panel.get_name(), self.plc_panel.get_address_str(), self.plc_panel.get_period(), element[0], element[1])
            self.info_area.insert_new_line_text(error)
        self.info_area.insert_new_line_text('Переменные сохранены на диск')
        return error

    def on_close(self):
        if self._in_process:
            self._stop_record(ask_flag=False)
            self._thread.join()

        error = save_config(f'{self._title}.cfg', self.plc_panel.get_config(), self.var_panel.get_config())
        if error != '':
            messagebox.showerror('Ошибка!', get_message(error))

    def _clear_info(self):
        self.info_area.clear_area()
        self.info_area.insert_text('Поле вывода очищено')
