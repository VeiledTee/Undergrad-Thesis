import glob
import os
import random
import tkinter as tk
from copy import deepcopy
from typing import List

import matplotlib
import numpy as np
import pandas as pd
import stl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d
from numpy import ndarray
from stl import mesh

matplotlib.use("TkAgg")

NUM_GEN: int = 10
C_RATE: float = 0.8
M_RATE: float = 1
T_RATE: float = 1
POP_SIZE: int = 10
POPULATION: List[ndarray] = []
CURRENT_DIRECTORY: str = ""
CURRENT_USER: str = ""
CURRENT_SHAPE: int = 0
CSV_FILE: str = "phylogenetic.csv"
TO_LOAD: str = ""

win1 = tk.Tk()
win1.title("3D Generations")
win1.rowconfigure(2)
win1.columnconfigure(5)
win1.withdraw()

win2 = tk.Tk()
win2.title("3D Generations")
win2.rowconfigure(2)
win2.columnconfigure(5)
win2.withdraw()

win3 = tk.Tk()
win3.title("3D Generations")
win3.rowconfigure(2)
win3.columnconfigure(5)
win3.withdraw()

win4 = tk.Tk()
win4.title("Start")


def make_cube() -> ndarray:
    data = np.zeros(12, dtype=stl.mesh.Mesh.dtype)
    # Looks like everything is defined as a triangle
    # Top face
    # (x -- left right, y --- front back, z --- up)
    data["vectors"][0] = np.array([[0, 1, 1], [1, 0, 1], [0, 0, 1]])
    data["vectors"][1] = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 1]])
    # Front face
    data["vectors"][2] = np.array([[1, 0, 0], [1, 0, 1], [1, 1, 0]])
    data["vectors"][3] = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 0]])
    # Left face
    data["vectors"][4] = np.array([[0, 0, 0], [1, 0, 0], [1, 0, 1]])
    data["vectors"][5] = np.array([[0, 0, 0], [0, 0, 1], [1, 0, 1]])
    # Bottom
    data["vectors"][6] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    data["vectors"][7] = np.array([[1, 0, 0], [0, 1, 0], [1, 1, 0]])
    # Back face
    data["vectors"][8] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
    data["vectors"][9] = np.array([[0, 1, 1], [0, 0, 1], [0, 1, 0]])
    # Right face
    data["vectors"][10] = np.array([[0, 1, 1], [1, 1, 1], [1, 1, 0]])
    data["vectors"][11] = np.array([[0, 1, 1], [0, 1, 0], [1, 1, 0]])

    return data


def make_pyramid() -> ndarray:
    data = np.zeros(12, dtype=stl.mesh.Mesh.dtype)
    # Looks like everything is defined as a triangle
    # Top face
    # (x -- left right, y --- front back, z --- up)
    data["vectors"][0] = np.array([[-1, 1, 0], [1, 1, 0], [0, 0, 2]])
    data["vectors"][1] = np.array([[-1, 1, 0], [-1, -1, 0], [0, 0, 2]])
    data["vectors"][2] = np.array([[-1, -1, 0], [1, -1, 0], [0, 0, 2]])
    data["vectors"][3] = np.array([[1, -1, 0], [1, 1, 0], [0, 0, 2]])
    data["vectors"][4] = np.array([[-1, 1, 0], [1, 1, 0], [0, 0, 0]])
    data["vectors"][5] = np.array([[-1, 1, 0], [-1, -1, 0], [0, 0, 0]])
    data["vectors"][6] = np.array([[-1, -1, 0], [1, -1, 0], [0, 0, 0]])
    data["vectors"][7] = np.array([[1, -1, 0], [1, 1, 0], [0, 0, 0]])

    return data


def get_user() -> None:
    global CURRENT_USER
    CURRENT_USER = input("Input your Username: ")


def initialize_scratch():
    # do the population thing
    # fitness will be an overarching thing, keeping track of which of the shapes
    # gets selected per generation so we can develop a tree
    global POPULATION
    global CURRENT_USER
    global CURRENT_DIRECTORY
    files = glob.glob("*.csv")
    if not files:
        csv = open(os.path.join(os.getcwd(), CSV_FILE), "w")
        csv.write("Parent,Child")
        csv.close()
    cube = make_cube()
    pyramid = make_pyramid()
    new_pop = [cube, pyramid]
    CURRENT_DIRECTORY = path_setup()
    return new_pop


def initialize_from():
    # do the population thing
    # fitness will be an overarching thing, keeping track of which of the shapes
    # gets selected per generation so we can develop a tree
    global POPULATION
    global CURRENT_USER
    global CURRENT_DIRECTORY
    files = glob.glob("*.csv")
    if not files:
        csv = open(os.path.join(os.getcwd(), CSV_FILE), "w")
        csv.write("Parent,Child")
        csv.close()
    CURRENT_DIRECTORY = path_setup()
    pop_files = glob.glob(f"{CURRENT_DIRECTORY}/*.stl")
    cleaned_files = []
    for i in pop_files:
        cleaned_files.append(os.path.basename(i))
    parents = []
    new_pop = []
    for i in range(POP_SIZE):
        p = str(cleaned_files[random.randint(0, len(cleaned_files) - 1)])
        new_mesh = mesh.Mesh.from_file(CURRENT_DIRECTORY + "/" + p).data
        parents.append(p)
        new_pop.append(new_mesh)
    return new_pop, parents


def initialize_file():
    # do the population thing
    # fitness will be an overarching thing, keeping track of which of the shapes
    # gets selected per generation so we can develop a tree
    global POPULATION
    global CURRENT_DIRECTORY
    global TO_LOAD
    if TO_LOAD[-4:] != ".stl":
        TO_LOAD += ".stl"
    files = glob.glob("*.csv")
    if not files:
        csv = open(os.path.join(os.getcwd(), CSV_FILE), "w")
        csv.write("Parent,Child")
        csv.close()
    CURRENT_DIRECTORY = path_setup()
    new_pop = [mesh.Mesh.from_file(CURRENT_DIRECTORY + "/" + TO_LOAD).data for _ in range(POP_SIZE)]
    parent = TO_LOAD
    print(TO_LOAD)
    print(TO_LOAD.replace('.stl', ''))
    return new_pop, parent.replace('.stl', '')


def path_setup() -> str:
    cur_path: str = os.getcwd()
    if not os.path.exists(os.path.join(cur_path, "Shapes")):
        os.makedirs(os.path.join(cur_path, "Shapes"))
    path: str = cur_path + "/Shapes"
    return path


def update_shape():
    global CURRENT_SHAPE
    files = [int(f[-8:-4]) for f in os.listdir(CURRENT_DIRECTORY) if f.startswith(f"{CURRENT_USER}_")]
    if files:
        CURRENT_SHAPE = max(files) + 1


def scratch_window():
    win2.destroy()
    win3.destroy()
    win4.destroy()

    win1.iconify()
    f = GeneticAlgorithmScratch(win1)
    f.pack()
    win1.deiconify()


def from_window():
    win1.destroy()
    win3.destroy()
    win4.destroy()

    win2.iconify()
    f = GeneticAlgorithmFrom(win2)
    f.pack()
    win2.deiconify()


def file_window():
    global TO_LOAD
    win1.destroy()
    win2.destroy()
    TO_LOAD = s.entry.get()
    win4.destroy()

    win3.iconify()
    f = GeneticAlgorithmFile(win3)
    f.pack()
    win3.deiconify()


class StartPage(tk.Frame):
    entry = tk.Entry(win4, width=35, bd=1)
    entry.insert(0, "File to load...")
    entry.config(fg="grey")
    entry.pack(side="left")

    def __init__(self):
        global TO_LOAD
        StartPage.entry.bind("<FocusIn>", self.on_entry_click)
        StartPage.entry.bind("<FocusOut>", self.on_focusout)
        self.BeginNewButton = tk.Button(
            win4,
            text="From Scratch",
            width=25,
            command=scratch_window,
        )
        self.BeginNewButton.pack()
        self.BeginFromButton = tk.Button(
            win4,
            text="From Random",
            width=25,
            command=from_window,
        )
        self.BeginFromButton.pack()
        self.BeginFileButton = tk.Button(
            win4,
            text="From File",
            width=25,
            command=file_window,
        )
        self.BeginFileButton.pack()

    def on_entry_click(self, event):
        """
        function that gets called whenever entry is clicked
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if StartPage.entry.cget("fg") == "grey":
            StartPage.entry.delete(0, "end")  # delete all the text in the entry
            StartPage.entry.insert(0, "")  # Insert blank for user input
            StartPage.entry.config(fg="black")

    def on_focusout(self, event):
        """
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if StartPage.entry.get() == "":
            StartPage.entry.insert(0, "File to load...")
            StartPage.entry.config(fg="grey")


class GeneticAlgorithmScratch(tk.Frame):
    entry = tk.Entry(win1, width=35, bd=1)
    entry.insert(0, "Shape number you like the most...")
    entry.config(fg="grey")
    entry.pack(side="left")
    scratch_pop = initialize_scratch()
    counter: int = 0
    parent = "parent"

    def __init__(self, master=None, **kwargs):
        update_shape()
        super().__init__(master, **kwargs)
        self.master = master
        figure = Figure(figsize=(12, 8))
        self.fig = figure
        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.get_tk_widget().pack()
        self._pop = GeneticAlgorithmScratch.scratch_pop
        self.plot_start()
        self.input_value = 1
        self.new_pop = self._pop
        tk.Button(self, text="    Save    ", command=self.save_and_exit_button).pack(side=tk.BOTTOM)
        tk.Button(self, text="   Evolve   ", command=self.plot_next_button).pack(side=tk.BOTTOM)
        master.bind("<Return>", self.plot_next_key)
        master.bind("<Escape>", self.save_and_exit_key)
        GeneticAlgorithmScratch.entry.bind("<FocusIn>", self.on_entry_click)
        GeneticAlgorithmScratch.entry.bind("<FocusOut>", self.on_focusout)

    def plot_start(self):
        for i in range(2):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 1, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()

    def plot_next_button(self):
        self.get_entry()  # update selection
        if GeneticAlgorithmScratch.counter == 0:
            # keep track of parents
            if self.input_value - 1 == 0:
                GeneticAlgorithmScratch.parent = "cube"
            elif self.input_value - 1 == 1:
                GeneticAlgorithmScratch.parent = "pyramid"
            self.save(
                self._pop[self.input_value - 1],
                f"{CURRENT_DIRECTORY}/{GeneticAlgorithmScratch.parent}",
            )

        self.generate_pop(self.input_value - 1)  # make new pop based on selection
        self.fig.clear()  # clear old figures
        self.fig.suptitle(f"Generation {GeneticAlgorithmScratch.counter}")
        # do the plotting thing
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()
        GeneticAlgorithmScratch.counter += 1

    def plot_next_key(self, event):
        self.get_entry()  # update selection
        if GeneticAlgorithmScratch.counter == 0:
            # keep track of parents
            if self.input_value - 1 == 0:
                GeneticAlgorithmScratch.parent = "cube"
            elif self.input_value - 1 == 1:
                GeneticAlgorithmScratch.parent = "pyramid"
            self.save(
                self._pop[self.input_value - 1],
                f"{CURRENT_DIRECTORY}/{GeneticAlgorithmScratch.parent}",
            )

        self.generate_pop(self.input_value - 1)  # make new pop based on selection
        self.fig.clear()  # clear old figures
        self.fig.suptitle(f"Generation {GeneticAlgorithmScratch.counter}")
        # do the plotting thing
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()
        GeneticAlgorithmScratch.counter += 1

    def save(self, to_plot, save_file: str):
        self.get_entry()
        my_mesh = stl.mesh.Mesh(to_plot.copy())
        my_mesh.save(f"{save_file}.stl", mode=stl.Mode.BINARY)

    def save_and_exit_button(self):
        self.get_final_entry()
        print(self.input_value)
        my_mesh = stl.mesh.Mesh(self._pop[self.input_value - 1].copy())
        my_mesh.save(f"{CURRENT_DIRECTORY}/{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", mode=stl.Mode.BINARY)
        df = pd.read_csv(CSV_FILE)
        index = len(df.index)
        diction = {
            df.columns[0]: GeneticAlgorithmScratch.parent,
            df.columns[1]: f"{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}",
        }
        df.loc[index] = diction
        df.to_csv(CSV_FILE, index=False)

        new_win = tk.Toplevel(self.master)
        to_kill = self.master
        new_win.title("Saved Successfully")
        tk.Label(
            new_win, text=f"Saved to file: {CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", font="Helvetica 24 bold"
        ).pack(side=tk.TOP)
        tk.Button(new_win, text="Exit", command=to_kill.destroy).pack(side=tk.BOTTOM)

    def save_and_exit_key(self, event):
        self.get_final_entry()
        print(self.input_value)
        my_mesh = stl.mesh.Mesh(self._pop[self.input_value - 1].copy())
        my_mesh.save(f"{CURRENT_DIRECTORY}/{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", mode=stl.Mode.BINARY)
        df = pd.read_csv(CSV_FILE)
        index = len(df.index)
        diction = {
            df.columns[0]: GeneticAlgorithmScratch.parent,
            df.columns[1]: f"{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}",
        }
        df.loc[index] = diction
        df.to_csv(CSV_FILE, index=False)

        new_win = tk.Toplevel(self.master)
        to_kill = self.master
        new_win.title("Saved Successfully")
        tk.Label(
            new_win, text=f"Saved to file: {CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", font="Helvetica 24 bold"
        ).pack(side=tk.TOP)
        tk.Button(new_win, text="Exit", command=to_kill.destroy).pack(side=tk.BOTTOM)

    def get_entry(self):
        self.input_value = GeneticAlgorithmScratch.entry.get()
        if self.input_value == "":
            self.input_value = 1
        else:
            try:
                self.input_value = int(self.input_value)
            except ValueError:
                self.error_window()

    def get_final_entry(self):
        self.input_value = GeneticAlgorithmScratch.entry.get()
        if self.input_value == "":
            self.input_value = 1
        else:
            try:
                self.input_value = int(self.input_value)
            except ValueError:
                self.error_window()

    def generate_pop(self, selected: int) -> None:
        parent: ndarray = self._pop[selected]
        self.new_pop: List[ndarray] = [deepcopy(parent) for _ in range(POP_SIZE)]
        for i in range(POP_SIZE):  # for the pop size
            if (
                np.random.uniform(0, 1) < T_RATE and GeneticAlgorithmScratch.counter > 0
            ):  # if not first evolution and we make new triangle
                t = np.random.randint(0, len(self.new_pop[i]["vectors"]))  # choose random triangle
                self.new_pop[i] = self.break_up_triangle(
                    to_break=self.new_pop[i]["vectors"][t], index=t, parent=self.new_pop[i]
                )  # make more triangles
            if np.random.randint(0, 2) % 2 == 0:
                self.point_manipulation(self.new_pop[i], self.multiply_points)  # multiply a point by random value
            else:
                self.point_manipulation(self.new_pop[i], self.add_points)  # add a random value to a point
        self._pop = self.new_pop

    def on_entry_click(self, event):
        """
        function that gets called whenever entry is clicked
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if GeneticAlgorithmScratch.entry.cget("fg") == "grey":
            GeneticAlgorithmScratch.entry.delete(0, "end")  # delete all the text in the entry
            GeneticAlgorithmScratch.entry.insert(0, "")  # Insert blank for user input
            GeneticAlgorithmScratch.entry.config(fg="black")

    def on_focusout(self, event):
        """
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if GeneticAlgorithmScratch.entry.get() == "":
            GeneticAlgorithmScratch.entry.insert(0, "Shape number you like the most...")
            GeneticAlgorithmScratch.entry.config(fg="grey")

    def error_window(self):
        msg = tk.Toplevel()
        msg.title("WARNING")
        tk.Label(msg, text="Only input numbers between 1 and the total number of shapes").pack()
        tk.Button(msg, text="Okay", command=msg.destroy).pack()
        msg.bind("<Return>", lambda destroy: msg.destroy())

    def point_manipulation(self, object: ndarray, manipulation) -> None:
        index = np.random.randint(len(object["vectors"]))
        point = object["vectors"][index][random.randint(0, 2)]
        compare = deepcopy(point)
        new_point = manipulation(point)
        for i in range(len(object["vectors"])):
            for j in range(len(object["vectors"][i])):
                if list(object["vectors"][i][j]) == list(compare):
                    object["vectors"][i][j] = new_point

    def multiply_points(self, point) -> None:
        if random.randint(0, 1) == 0:
            point *= random.uniform(0.1, 2)
        else:
            point *= random.uniform(-2, -0.1)
        return point

    def add_points(self, point: ndarray) -> ndarray:
        largest: int = max(np.max(point[0]), np.max(point[1]), np.max(point[2]))
        point[0] += int(random.uniform(np.negative(largest / 2), largest / 2))
        point[1] += int(random.uniform(np.negative(largest / 2), largest / 2))
        point[2] += int(random.uniform(np.negative(largest / 2), largest / 2))
        return point

    def midpoint(self, coords: ndarray) -> ndarray:
        final_list: List[List[float]] = []
        for i in range(coords.shape[0]):
            if i + 1 == coords.shape[0]:
                m_x = (coords[i][0] + coords[0][0]) / 2
                m_y = (coords[i][1] + coords[0][1]) / 2
                m_z = (coords[i][2] + coords[0][2]) / 2
                final_list.append([m_x, m_y, m_z])
            else:
                m_x = (coords[i][0] + coords[i + 1][0]) / 2
                m_y = (coords[i][1] + coords[i + 1][1]) / 2
                m_z = (coords[i][2] + coords[i + 1][2]) / 2
                final_list.append([m_x, m_y, m_z])
        return np.array(final_list)

    def break_up_triangle(self, to_break: ndarray, index: int, parent: ndarray) -> ndarray:
        """
        Split a Mesh triangle into 4 identical ones
        :param to_break: a 3D numpy array of shape (3, 3), representing a triangle in 3D space
        """
        midpoints: ndarray = self.midpoint(to_break)
        # increase the size of the DATA object by 3 for the new sides we are adding
        new_data = np.zeros(parent.shape[0] + 3, dtype=stl.mesh.Mesh.dtype)
        for v in range(len(parent["vectors"])):
            new_data["vectors"][v] = deepcopy(parent["vectors"][v])
        new_data["vectors"][index] = np.array((midpoints[0], midpoints[1], midpoints[2]))
        new_data["vectors"][v + 1] = np.array([to_break[0], midpoints[0], midpoints[2]])
        new_data["vectors"][v + 2] = np.array([to_break[1], midpoints[0], midpoints[1]])
        new_data["vectors"][v + 3] = np.array([to_break[2], midpoints[1], midpoints[2]])
        return new_data


class GeneticAlgorithmFrom(tk.Frame):
    entry = tk.Entry(win2, width=35, bd=1)
    entry.insert(0, "Shape number you like the most...")
    entry.config(fg="grey")
    entry.pack(side="left")
    counter: int = 0
    parent = "parent"

    def __init__(self, master=None, **kwargs):
        update_shape()
        self.master = master
        super().__init__(master, **kwargs)
        figure = Figure(figsize=(12, 8))
        self.fig = figure
        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.get_tk_widget().pack()
        self._pop, self.parent_list = initialize_from()
        self.plot_start()
        self.input_value = 1
        self.new_pop = self._pop
        tk.Button(self, text="    Save    ", command=self.save_and_exit_button).pack(side=tk.BOTTOM)
        tk.Button(self, text="   Evolve   ", command=self.plot_next_button).pack(side=tk.BOTTOM)
        master.bind("<Return>", self.plot_next_key)
        master.bind("<Escape>", self.save_and_exit_key)
        GeneticAlgorithmFrom.entry.bind("<FocusIn>", self.on_entry_click)
        GeneticAlgorithmFrom.entry.bind("<FocusOut>", self.on_focusout)

    def plot_start(self):
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()

    def plot_next_button(self):
        self.get_entry()  # update selection
        if GeneticAlgorithmFrom.counter == 0:
            # keep track of parents
            GeneticAlgorithmFrom.parent = str(self.parent_list[self.input_value - 1][:-4])
            self.save(
                self._pop[self.input_value - 1],
                f"{CURRENT_DIRECTORY}/{GeneticAlgorithmFrom.parent}",
            )

        self.generate_pop(self.input_value - 1)  # make new pop based on selection
        self.fig.clear()  # clear old figures
        self.fig.suptitle(f"Generation {GeneticAlgorithmFrom.counter}")
        # do the plotting thing
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()
        GeneticAlgorithmFrom.counter += 1

    def plot_next_key(self, event):
        self.get_entry()  # update selection
        if GeneticAlgorithmFrom.counter == 0:
            # keep track of parents
            GeneticAlgorithmFrom.parent = str(self.parent_list[self.input_value - 1])
            self.save(
                self._pop[self.input_value - 1],
                f"{CURRENT_DIRECTORY}/{GeneticAlgorithmFrom.parent}",
            )

        self.generate_pop(self.input_value - 1)  # make new pop based on selection
        self.fig.clear()  # clear old figures
        self.fig.suptitle(f"Generation {GeneticAlgorithmFrom.counter}")
        # do the plotting thing
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()
        GeneticAlgorithmFrom.counter += 1

    def save(self, to_plot, save_file: str):
        self.get_entry()
        my_mesh = stl.mesh.Mesh(to_plot.copy())
        my_mesh.save(f"{save_file}", mode=stl.Mode.BINARY)

    def save_and_exit_button(self):
        self.get_final_entry()
        my_mesh = stl.mesh.Mesh(self._pop[self.input_value - 1].copy())
        my_mesh.save(f"{CURRENT_DIRECTORY}/{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}", mode=stl.Mode.BINARY)
        df = pd.read_csv(CSV_FILE)
        index = len(df.index)
        diction = {
            df.columns[0]: GeneticAlgorithmFrom.parent,
            df.columns[1]: f"{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}",
        }
        df.loc[index] = diction
        df.to_csv(CSV_FILE, index=False)

        new_win = tk.Toplevel(self.master)
        to_kill = self.master
        new_win.title("Saved Successfully")
        tk.Label(
            new_win, text=f"Saved to file: {CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", font="Helvetica 24 bold"
        ).pack(side=tk.TOP)
        tk.Button(new_win, text="Exit", command=to_kill.destroy).pack(side=tk.BOTTOM)

    def save_and_exit_key(self, event):
        self.get_final_entry()
        my_mesh = stl.mesh.Mesh(self._pop[self.input_value - 1].copy())
        my_mesh.save(f"{CURRENT_DIRECTORY}/{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}", mode=stl.Mode.BINARY)
        df = pd.read_csv(CSV_FILE)
        index = len(df.index)
        diction = {
            df.columns[0]: GeneticAlgorithmFrom.parent,
            df.columns[1]: f"{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}",
        }
        df.loc[index] = diction
        df.to_csv(CSV_FILE, index=False)

        new_win = tk.Toplevel(self.master)
        to_kill = self.master
        new_win.title("Saved Successfully")
        tk.Label(
            new_win, text=f"Saved to file: {CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", font="Helvetica 24 bold"
        ).pack(side=tk.TOP)
        tk.Button(new_win, text="Exit", command=to_kill.destroy).pack(side=tk.BOTTOM)

    def get_entry(self):
        self.input_value = GeneticAlgorithmFrom.entry.get()
        if self.input_value == "":
            self.input_value = 1
        else:
            try:
                self.input_value = int(self.input_value)
            except ValueError:
                self.error_window()

    def get_final_entry(self):
        self.input_value = GeneticAlgorithmFrom.entry.get()
        if type(self.input_value) != int:
            self.input_value = 1
        else:
            try:
                self.input_value = int(self.input_value)
            except ValueError:
                self.error_window()

    def generate_pop(self, selected: int) -> None:
        parent: ndarray = self._pop[selected]
        self.new_pop: List[ndarray] = [deepcopy(parent) for _ in range(POP_SIZE)]
        for i in range(POP_SIZE):  # for the pop size
            if (
                np.random.uniform(0, 1) < T_RATE and GeneticAlgorithmFile.counter > 0
            ):  # if not first evolution and we make new triangle
                t = np.random.randint(0, len(self.new_pop[i]["vectors"]))  # choose random triangle
                self.new_pop[i] = self.break_up_triangle(
                    to_break=self.new_pop[i]["vectors"][t], index=t, parent=self.new_pop[i]
                )  # make more triangles
            if np.random.randint(0, 2) % 2 == 0:
                self.point_manipulation(self.new_pop[i], self.multiply_points)  # multiply a point by random value
            else:
                self.point_manipulation(self.new_pop[i], self.add_points)  # add a random value to a point
        self._pop = self.new_pop

    def on_entry_click(self, event):
        """
        function that gets called whenever entry is clicked
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if GeneticAlgorithmFrom.entry.cget("fg") == "grey":
            GeneticAlgorithmFrom.entry.delete(0, "end")  # delete all the text in the entry
            GeneticAlgorithmFrom.entry.insert(0, "")  # Insert blank for user input
            GeneticAlgorithmFrom.entry.config(fg="black")

    def on_focusout(self, event):
        """
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if GeneticAlgorithmFrom.entry.get() == "":
            GeneticAlgorithmFrom.entry.insert(0, "Shape number you like the most...")
            GeneticAlgorithmFrom.entry.config(fg="grey")

    def error_window(self):
        msg = tk.Toplevel()
        msg.title("WARNING")
        tk.Label(msg, text="Only input numbers between 1 and the total number of shapes").pack()
        tk.Button(msg, text="Okay", command=msg.destroy).pack()
        msg.bind("<Return>", lambda destroy: msg.destroy())

    def point_manipulation(self, object: ndarray, manipulation) -> None:
        index = np.random.randint(len(object["vectors"]))
        point = object["vectors"][index][random.randint(0, 2)]
        compare = deepcopy(point)
        new_point = manipulation(point)
        for i in range(len(object["vectors"])):
            for j in range(len(object["vectors"][i])):
                if list(object["vectors"][i][j]) == list(compare):
                    object["vectors"][i][j] = new_point

    def multiply_points(self, point) -> None:
        if random.randint(0, 1) == 0:
            point *= random.uniform(0.1, 2)
        else:
            point *= random.uniform(-2, -0.1)
        return point

    def add_points(self, point: ndarray) -> ndarray:
        largest: int = max(np.max(point[0]), np.max(point[1]), np.max(point[2]))
        point[0] += int(random.uniform(np.negative(largest / 2), largest / 2))
        point[1] += int(random.uniform(np.negative(largest / 2), largest / 2))
        point[2] += int(random.uniform(np.negative(largest / 2), largest / 2))
        return point

    def midpoint(self, coords: ndarray) -> ndarray:
        final_list: List[List[float]] = []
        for i in range(coords.shape[0]):
            if i + 1 == coords.shape[0]:
                m_x = (coords[i][0] + coords[0][0]) / 2
                m_y = (coords[i][1] + coords[0][1]) / 2
                m_z = (coords[i][2] + coords[0][2]) / 2
                final_list.append([m_x, m_y, m_z])
            else:
                m_x = (coords[i][0] + coords[i + 1][0]) / 2
                m_y = (coords[i][1] + coords[i + 1][1]) / 2
                m_z = (coords[i][2] + coords[i + 1][2]) / 2
                final_list.append([m_x, m_y, m_z])
        return np.array(final_list)

    def break_up_triangle(self, to_break: ndarray, index: int, parent: ndarray) -> ndarray:
        """
        Split a Mesh triangle into 4 identical ones
        :param to_break: a 3D numpy array of shape (3, 3), representing a triangle in 3D space
        """
        midpoints: ndarray = self.midpoint(to_break)
        # increase the size of the DATA object by 3 for the new sides we are adding
        new_data = np.zeros(parent.shape[0] + 3, dtype=stl.mesh.Mesh.dtype)
        for v in range(len(parent["vectors"])):
            new_data["vectors"][v] = deepcopy(parent["vectors"][v])
        new_data["vectors"][index] = np.array((midpoints[0], midpoints[1], midpoints[2]))
        new_data["vectors"][v + 1] = np.array([to_break[0], midpoints[0], midpoints[2]])
        new_data["vectors"][v + 2] = np.array([to_break[1], midpoints[0], midpoints[1]])
        new_data["vectors"][v + 3] = np.array([to_break[2], midpoints[1], midpoints[2]])
        return new_data


class GeneticAlgorithmFile(tk.Frame):
    entry = tk.Entry(win3, width=35, bd=1)
    entry.insert(0, "Shape number you like the most...")
    entry.config(fg="grey")
    entry.pack(side="left")
    counter: int = 0
    parent = TO_LOAD[:-4]

    def __init__(self, master=None, **kwargs):
        update_shape()
        self.master = master
        super().__init__(master, **kwargs)
        figure = Figure(figsize=(12, 8))
        self.fig = figure
        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.get_tk_widget().pack()
        self._pop, GeneticAlgorithmFile.parent = initialize_file()
        self.input_value = 1
        self.plot_start()
        self.new_pop = self._pop
        tk.Button(self, text="    Save    ", command=self.save_and_exit_button).pack(side=tk.BOTTOM)
        tk.Button(self, text="   Evolve   ", command=self.plot_next_button).pack(side=tk.BOTTOM)
        master.bind("<Return>", self.plot_next_key)
        master.bind("<Escape>", self.save_and_exit_key)
        GeneticAlgorithmFile.entry.bind("<FocusIn>", self.on_entry_click)
        GeneticAlgorithmFile.entry.bind("<FocusOut>", self.on_focusout)

    def plot_start(self):
        self.generate_pop(0)
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()

    def plot_next_button(self):
        self.get_entry()  # update selection
        if GeneticAlgorithmFile.counter == 0:
            # keep track of parent
            self.save(
                self._pop[self.input_value - 1],
                f"{CURRENT_DIRECTORY}/{GeneticAlgorithmFile.parent}",
            )

        self.generate_pop(self.input_value - 1)  # make new pop based on selection
        self.fig.clear()  # clear old figures
        self.fig.suptitle(f"Generation {GeneticAlgorithmFile.counter}")
        # do the plotting thing
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()
        GeneticAlgorithmFile.counter += 1

    def plot_next_key(self, event):
        self.get_entry()  # update selection
        if GeneticAlgorithmFile.counter == 0:
            # keep track of parent
            self.save(
                self._pop[self.input_value - 1],
                f"{CURRENT_DIRECTORY}/{GeneticAlgorithmFile.parent}",
            )

        self.generate_pop(self.input_value - 1)  # make new pop based on selection
        self.fig.clear()  # clear old figures
        self.fig.suptitle(f"Generation {GeneticAlgorithmFile.counter}")
        # do the plotting thing
        for i in range(POP_SIZE):
            msh = mesh.Mesh(self._pop[i])
            axes = self.fig.add_subplot(2, 5, i + 1, projection="3d")
            axes.set_xlim([-2, 2])
            axes.set_ylim([-2, 2])
            axes.set_zlim([-2, 2])
            axes.title.set_text(f"Shape {i + 1}")
            axes.add_collection3d(mplot3d.art3d.Poly3DCollection(msh.vectors))
            self.canvas.mpl_connect("button_press_event", axes._button_press)
            self.canvas.mpl_connect("button_release_event", axes._button_release)
            self.canvas.mpl_connect("motion_notify_event", axes._on_move)
        self.fig.canvas.draw()
        GeneticAlgorithmFile.counter += 1

    def save(self, to_plot, save_file: str):
        self.get_entry()
        my_mesh = stl.mesh.Mesh(to_plot.copy())
        my_mesh.save(f"{save_file}", mode=stl.Mode.BINARY)

    def save_and_exit_button(self):
        self.get_final_entry()
        my_mesh = stl.mesh.Mesh(self._pop[self.input_value - 1].copy())
        my_mesh.save(f"{CURRENT_DIRECTORY}/{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", mode=stl.Mode.BINARY)
        df = pd.read_csv(CSV_FILE)
        index = len(df.index)
        diction = {
            df.columns[0]: GeneticAlgorithmFile.parent,
            df.columns[1]: f"{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}",
        }
        df.loc[index] = diction
        df.to_csv(CSV_FILE, index=False)

        new_win = tk.Toplevel(self.master)
        to_kill = self.master
        new_win.title("Saved Successfully")
        tk.Label(
            new_win, text=f"Saved to file: {CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", font="Helvetica 24 bold"
        ).pack(side=tk.TOP)
        tk.Button(new_win, text="Exit", command=to_kill.destroy).pack(side=tk.BOTTOM)

    def save_and_exit_key(self, event):
        self.get_final_entry()
        my_mesh = stl.mesh.Mesh(self._pop[self.input_value - 1].copy())
        my_mesh.save(f"{CURRENT_DIRECTORY}/{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", mode=stl.Mode.BINARY)
        df = pd.read_csv(CSV_FILE)
        index = len(df.index)
        diction = {
            df.columns[0]: GeneticAlgorithmFile.parent,
            df.columns[1]: f"{CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}",
        }
        df.loc[index] = diction
        df.to_csv(CSV_FILE, index=False)

        new_win = tk.Toplevel(self.master)
        to_kill = self.master
        new_win.title("Saved Successfully")
        tk.Label(
            new_win, text=f"Saved to file: {CURRENT_USER}_{str(CURRENT_SHAPE).zfill(4)}.stl", font="Helvetica 24 bold"
        ).pack(side=tk.TOP)
        tk.Button(new_win, text="Exit", command=to_kill.destroy).pack(side=tk.BOTTOM)

    def get_entry(self):
        self.input_value = GeneticAlgorithmFile.entry.get()
        if self.input_value == "":
            self.input_value = 1
        else:
            try:
                self.input_value = int(self.input_value)
            except ValueError:
                self.error_window()

    def get_final_entry(self):
        self.input_value = GeneticAlgorithmFile.entry.get()
        if type(self.input_value) != int:
            self.input_value = 1
        else:
            try:
                self.input_value = int(self.input_value)
            except ValueError:
                self.error_window()

    def generate_pop(self, selected: int) -> None:
        parent: ndarray = self._pop[selected]
        self.new_pop: List[ndarray] = [deepcopy(parent) for _ in range(POP_SIZE)]
        for i in range(POP_SIZE):  # for the pop size
            if (
                np.random.uniform(0, 1) < T_RATE and GeneticAlgorithmFile.counter > 0
            ):  # if not first evolution and we make new triangle
                t = np.random.randint(0, len(self.new_pop[i]["vectors"]))  # choose random triangle
                self.new_pop[i] = self.break_up_triangle(
                    to_break=self.new_pop[i]["vectors"][t], index=t, parent=self.new_pop[i]
                )  # make more triangles
            if np.random.randint(0, 2) % 2 == 0:
                self.point_manipulation(self.new_pop[i], self.multiply_points)  # multiply a point by random value
            else:
                self.point_manipulation(self.new_pop[i], self.add_points)  # add a random value to a point
        self._pop = self.new_pop

    def on_entry_click(self, event):
        """
        function that gets called whenever entry is clicked
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if GeneticAlgorithmFile.entry.cget("fg") == "grey":
            GeneticAlgorithmFile.entry.delete(0, "end")  # delete all the text in the entry
            GeneticAlgorithmFile.entry.insert(0, "")  # Insert blank for user input
            GeneticAlgorithmFile.entry.config(fg="black")

    def on_focusout(self, event):
        """
        referenced: https://stackoverflow.com/questions/30491721/how-to-insert-a-temporary-text-in-a-tkinter-entry-widget
        """
        if GeneticAlgorithmFile.entry.get() == "":
            GeneticAlgorithmFile.entry.insert(0, "Shape number you like the most...")
            GeneticAlgorithmFile.entry.config(fg="grey")

    def error_window(self):
        msg = tk.Toplevel()
        msg.title("WARNING")
        tk.Label(msg, text="Only input numbers between 1 and the total number of shapes").pack()
        tk.Button(msg, text="Okay", command=msg.destroy).pack()
        msg.bind("<Return>", lambda destroy: msg.destroy())

    def point_manipulation(self, object: ndarray, manipulation) -> None:
        index = np.random.randint(len(object["vectors"]))
        point = object["vectors"][index][random.randint(0, 2)]
        compare = deepcopy(point)
        new_point = manipulation(point)
        for i in range(len(object["vectors"])):
            for j in range(len(object["vectors"][i])):
                if list(object["vectors"][i][j]) == list(compare):
                    object["vectors"][i][j] = new_point

    def multiply_points(self, point) -> None:
        if random.randint(0, 1) == 0:
            point *= random.uniform(0.1, 2)
        else:
            point *= random.uniform(-2, -0.1)
        return point

    def add_points(self, point: ndarray) -> ndarray:
        largest: int = max(np.max(point[0]), np.max(point[1]), np.max(point[2]))
        point[0] += int(random.uniform(np.negative(largest / 2), largest / 2))
        point[1] += int(random.uniform(np.negative(largest / 2), largest / 2))
        point[2] += int(random.uniform(np.negative(largest / 2), largest / 2))
        return point

    def midpoint(self, coords: ndarray) -> ndarray:
        final_list: List[List[float]] = []
        for i in range(coords.shape[0]):
            if i + 1 == coords.shape[0]:
                m_x = (coords[i][0] + coords[0][0]) / 2
                m_y = (coords[i][1] + coords[0][1]) / 2
                m_z = (coords[i][2] + coords[0][2]) / 2
                final_list.append([m_x, m_y, m_z])
            else:
                m_x = (coords[i][0] + coords[i + 1][0]) / 2
                m_y = (coords[i][1] + coords[i + 1][1]) / 2
                m_z = (coords[i][2] + coords[i + 1][2]) / 2
                final_list.append([m_x, m_y, m_z])
        return np.array(final_list)

    def break_up_triangle(self, to_break: ndarray, index: int, parent: ndarray) -> ndarray:
        """
        Split a Mesh triangle into 4 identical ones
        :param to_break: a 3D numpy array of shape (3, 3), representing a triangle in 3D space
        """
        midpoints: ndarray = self.midpoint(to_break)
        # increase the size of the DATA object by 3 for the new sides we are adding
        new_data = np.zeros(parent.shape[0] + 3, dtype=stl.mesh.Mesh.dtype)
        for v in range(len(parent["vectors"])):
            new_data["vectors"][v] = deepcopy(parent["vectors"][v])
        new_data["vectors"][index] = np.array((midpoints[0], midpoints[1], midpoints[2]))
        new_data["vectors"][v + 1] = np.array([to_break[0], midpoints[0], midpoints[2]])
        new_data["vectors"][v + 2] = np.array([to_break[1], midpoints[0], midpoints[1]])
        new_data["vectors"][v + 3] = np.array([to_break[2], midpoints[1], midpoints[2]])
        return new_data


if __name__ == "__main__":
    get_user()
    s = StartPage()
    win4.mainloop()
