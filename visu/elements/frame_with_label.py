from tkinter import ttk, CENTER, TOP, X, StringVar


class FrameWithLabel(ttk.Frame):
    def __init__(self, master=None, label_text='', width=0):
        super().__init__(master)
        self._width = len(label_text) + 3 if width == 0 else width
        self.control_widget = None
        self.text_var = StringVar()
        self.label = ttk.Label(self, text=label_text, width=width, anchor=CENTER, foreground='gray')
        self.label.pack(side=TOP, fill=X)

    def lock(self, lck: bool):
        st = 'disable' if lck else 'normal'
        self.control_widget.config(state=st)

    def get_text(self):
        return self.text_var.get()

    def set_text(self, text):
        self.text_var.set(str(text))
