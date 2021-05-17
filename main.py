import functools
import matplotlib.pyplot as plt
import numpy as np
import os
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Equalizador(tk.Tk):
    def __init__(self):
        super().__init__()

        basepath = os.getcwd()
        icon = basepath + "\\img\\icon.png"
        self.iconphoto(True, tk.PhotoImage(file=icon))
        self.title("Equalizador")
        self.mainapp = MainApplication(self)

    def destroy(self):
        super().destroy()

    def start(self):
        self.mainloop()


class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(side="bottom", fill="both")

        self.audiofile = tk.StringVar()
        self.audiofile.set(os.getcwd()+"/audio/audio_test.wav")
        self.Gp = [(tk.IntVar(), "Graves"),
                   (tk.IntVar(), "Médios"),
                   (tk.IntVar(), "Agudos")]

        self.createWidgets()

    def createWidgets(self):
        """Cria cada um dos Widgets da janela.
        """
        ttk.Label(
            text="Equalizador de PDS",
            font=("Helvetica", 20, "bold")
        ).pack()

        self.setFileFrame()
        list(map(self.setScaleFrame, [1, 2, 3]))
        self.setApplyButton()

    def setFileFrame(self):
        """Cria o frame para escolha de áudio.
        """
        ttk.Label().pack()  # Blank row for better organization

        labelframe = ttk.LabelFrame(text="Seleção do arquivo de áudio")
        labelframe.pack(fill="both")

        ttk.Entry(
            labelframe,
            textvariable=self.audiofile,
            width=80
        ).pack(side="left", fill="both")

        # Select file path button
        title = f"Selecione o arquivo de áudio"
        ttk.Button(
            labelframe,
            text="...",
            command=lambda: self.audiofile.set(
                tk.filedialog.askopenfilename(
                    title=title,
                    initialdir="./audio/"
                )),
            width=3,
        ).pack(side="right")

        ttk.Label().pack()  # Blank row for better organization

    def setScaleFrame(self, i):
        """Cria o frame para escolha dos ganhos.
        """
        self.Gp[i-1][0].set(100)

        labelframe = ttk.LabelFrame(text=f"Ganho Gp{i} - {self.Gp[i-1][1]}")
        labelframe.pack(side="left", fill="both")

        tk.Scale(
            labelframe,
            from_=0,
            to=100,
            variable=self.Gp[i-1][0],
            orient="horizontal",
            length=165,
        ).pack()

    def setApplyButton(self):
        """Cria o botão para rodar os cálculos.
        """
        ttk.Label(self).pack()  # Blank row for better organization

        _wrapper = functools.partial(
            Results,
            master=self.master,
            audiofile=self.audiofile,
            Gp=[self.Gp[i][0] for i in range(3)])

        ttk.Button(
            self,
            text="Apply",
            command=_wrapper
        ).pack(side="right")


class Results(tk.Toplevel):
    """Window that shows the results.

    Where the magic happens!!!
    """
    def __init__(self, audiofile, Gp, master=None):
        super().__init__(master)
        self.master.withdraw()

        if not os.path.isfile(audiofile.get()):
            self.withdraw()
            tkinter.messagebox.showerror(
                title="Erro muito errado",
                message="Arquivo de áudio inválido ou inexistente")
            self.destroy()
        else:
            self.audiofile = audiofile.get()
            self.Gp = [Gp[i].get() for i in range(3)]

            self.audio = None
            self.samplerate = None
            self.audio_fft = None

            self.doTheMagic()

    def destroy(self):
        super().destroy()
        self.master.destroy()

    def doTheMagic(self):
        """It runs all"""
        self.readAudioFile()

    def readAudioFile(self):
        self.samplerate, self.audio = wavfile.read(self.audiofile)
        self.audio = np.transpose(self.audio)
        self.audio_fft = [None] * self.audio.ndim
        # self.audio_fft = [[] for _ in range(self.audio.ndim)]

        print(f"Sample Rate: {self.samplerate} with {self.audio.ndim} channels")

        fig1 = plt.Figure(figsize=(6, 5), dpi=100)
        chart_type = FigureCanvasTkAgg(fig1, self)
        chart_type.get_tk_widget().pack()

        duration = len(self.audio[:][0]) / float(self.samplerate)
        t = np.linspace(0, duration, len(self.audio[0]))
        ax = fig1.add_subplot(111)
        ax.set_title("No tempo")
        ax.plot(t, self.audio[0])
        ax.set_xlabel(f"Tempo [s]")
        ax.grid()

        self.audio_fft[0] = rfft(self.audio[0])
        self.audio_fft[1] = rfft(self.audio[1])
        fig2 = plt.Figure(figsize=(6, 5), dpi=100)
        ay = fig2.add_subplot(111)
        ay.set_title("Na frequencia")
        ay.plot(abs(self.audio_fft[0]))
        ay.grid()
        # plt.show()

    def showAnalisysSpectrumGraph(self):
        pass

    def filterChannels(self):
        pass


if __name__ == '__main__':
    eq = Equalizador()
    eq.start()
