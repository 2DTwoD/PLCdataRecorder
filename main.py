import datetime
import threading
from tkinter import Tk, messagebox

import matplotlib.pyplot as plt

from visu.elements.scrolled_frame import ScrolledFrame
from visu.main_panel import MainPanel

win_width = 900
win_height = 800

version = "1.0"

def main():
    # plt.plot(range(1000), range(1000), marker='.')
    # plt.ylabel('значение')
    # plt.xlabel('время')
    # plt.show()

    window = Tk()
    title = "PLC data recorder"
    title_with_version = f"{title}, v{version}"
    window.geometry(f'{win_width}x{win_height}')
    window.title(title_with_version)

    frame_with_scroll = ScrolledFrame(window, height=win_height, width=win_width)
    main_panel = MainPanel(frame_with_scroll.canvas, title)
    frame_with_scroll.setMainPanel(main_panel)

    def on_close():
        if messagebox.askokcancel("Выход", "Закрыть приложение?"):
            main_panel.on_close()
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    window.mainloop()


if __name__ == '__main__':
    main()