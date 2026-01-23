from tkinter import Tk

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
    title = f"PLC data recorder, v{version}"
    window.geometry(f'{win_width}x{win_height}')
    window.title(title)

    frame_with_scroll = ScrolledFrame(window, height=win_height, width=win_width)
    main_panel = MainPanel(frame_with_scroll.canvas)
    frame_with_scroll.setMainPanel(main_panel)

    window.mainloop()


if __name__ == '__main__':
    main()