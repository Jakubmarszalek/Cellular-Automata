import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import argparse
import io
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
base = 2
stop_point = base - 1


def draw(board):
    for i in board:
        print(i)


def parse_arguments():
    """
    Parses commandline arguments
    :return: Parsed arguments
    """
    parser = argparse.ArgumentParser('Run behave in parallel mode for scenarios')
    parser.add_argument('--n', '-n', type=int, help='the size of the square. Default = 100', default=200)
    parser.add_argument('--custom', '-c', help='Custom value. format: {"custom1": [x_int, y_int], "cystom2": [x_int, y_int]}', default={})
    parser.add_argument('--random', '-r', type=int, help='Number of random start point, default 10', default=25)
    parser.add_argument('--Neighbourhood', '-Neighbourhood', type=int, help='Type of Neighbourhood: 1)von Neumanna 2)Moore’a', default=1)
    parser.add_argument('--export', '-export', type=str, help='Type of export picture format', default="")

    args = parser.parse_args()
    return args


def gui_function():
    def main(n, custom, random_start, neighbourhood, export, base, inclusion_number, radius_min, radius_max, proc):
        new = {}
        check_new = []
        Z = list()
        board = []

        for x in range(0, n):
            board.append([])
            for y in range(0, n):
                board[x].append(base)
        p = base + 1
        for i in custom:
            try:
                board[custom[i][0]][custom[i][1]] = p
                custom[i].append(p)
            except IndexError:
                print("Custom start point not in declare box value")
                sys.exit(1)
            new.update({i: [custom[i][0], custom[i][1], p]})
            p = p + 1

        inclusion_point = []
        while inclusion_number != 0:
            y = random.randint(0, n - 1)
            x = random.randint(0, n - 1)
            if [y, x] not in inclusion_point:
                try:
                    radius = random.randint(radius_min, radius_max)
                except ValueError:
                    radius = random.randint(radius_max, radius_min)
                create_inclusions(board, [y, x], radius)
                inclusion_point.append([y, x])
                inclusion_number = inclusion_number - 1

        for i in range(p, p + random_start):
            while 1:
                x = random.randint(0, n - 1)
                y = random.randint(0, n - 1)
                if board[x][y] == base:
                    board[x][y] = i
                    break
            new.update({"random{0}".format(i): [x, y, i]})

        for i in new:
            check_new.append(new[i][2])

        p = 0
        old_count = 0
        while 1:
            p = p + 1
            Z.clear()
            for j in board:
                Z.extend(j)
            if neighbourhood == "Grain_Curvature":
                board = grain_curvature(board, base, n, check_new, int(proc))
            else:
                board = one_grow(board, base, n, check_new, neighbourhood)
            new_count = Z.count(base)
            if new_count == old_count:
                print("Part of image blocking by inculsion")
                break
            old_count = new_count
            proc_end = str(100 - new_count * 100 / (n * n))[0:5] + "%"
            image = np.zeros(len(Z))
            for i in range(len(image)):
                image[i] = Z[i]
            image = image.reshape((n, n))
            plt.matshow(image)
            callback(proc_end, plt)
            plt.close()
            if not base in Z:
                break
        print("Proces end after {0} iteration".format(p))
        image = np.zeros(len(Z))
        for i in range(len(image)):
            image[i] = Z[i]
        for i in new:
            print(str(i) + ": start point:" + "[x:" + str(new[i][0]) + " y:" + str(new[i][1]) + "] " + str(
                (Z.count(new[i][2]) * 100) / (n * n)) + "%")
        image = image.reshape((n, n))
        plt.matshow(image)
        if export == "png":
            plt.savefig('output.png')
        elif export == "pdf":
            plt.savefig('output.pdf')
        plt.show()
        return (image)

    def clicked(n, neighbourhood, r, output_file, custom_x, custom_y, inclusion_number, radius_min, radius_max, proc):
        custom = dict()
        custom_x = custom_x.get().split(" ")
        custom_y = custom_y.get().split(" ")
        if custom_x != [""]:
            for i in range(len(custom_x)):
                custom.update({"custom{0}".format(i + 1): [int(custom_x[i]), int(custom_y[i])]})

        if n.get() != "":
            size = int(n.get())
        else:
            size = 200

        if r.get() != "":
            random = int(r.get())
        else:
            random = 25

        if inclusion_number.get() != "":
            inclusion_number = int(inclusion_number.get())
        else:
            inclusion_number = 5

        if radius_min.get() != "":
            radius_min = int(radius_min.get())
        else:
            radius_min = 1

        if radius_max.get() != "":
            radius_max = int(radius_max.get())
        else:
            radius_max = 4

        if proc.get() != "":
            proc = int(proc.get())
        else:
            proc = 40
        image = main(size, custom, random, neighbourhood.get(), output_file.get(), base, inclusion_number, radius_min,
                     radius_max, proc)

    def callback(proc_end, plt):
       buf = io.BytesIO()
       plt.savefig(buf, format='png')
       buf.seek(0)
       img = Image.open(buf)
       img = img.resize((500, 500), Image.ANTIALIAS)
       img = ImageTk.PhotoImage(img)
       panel = Label(window, image=img)
       panel.image = img
       panel.grid(column=0, row=9)
       panel2 = Label(window, text=proc_end)
       panel2.grid(column=2, row=9)

    window = Tk()
    window.title("Welcome to LikeGeeks app")
    window.geometry('780x660')

    lbl = Label(window, text="the size of the square")
    lbl.grid(column=0, row=0)

    lbl = Label(window, text="type of Neighbourhood")
    lbl.grid(column=0, row=1)

    lbl = Label(window, text="% for Grain_Curvature")
    lbl.grid(column=0, row=2)

    lbl = Label(window, text="Number of random start place")
    lbl.grid(column=0, row=3)

    lbl = Label(window, text="Type of output file")
    lbl.grid(column=0, row=4)

    lbl = Label(window, text="parametr of custom start point: X and Y")
    lbl.grid(column=0, row=5)

    lbl = Label(window, text="Number of random inclusions point and radius min-max")
    lbl.grid(column=0, row=6)

    n = Entry(window, width=10)
    n.grid(column=1, row=0)

    proc = Entry(window, width=10)
    proc.grid(column=1, row=2)

    r = Entry(window, width=10)
    r.grid(column=1, row=3)

    custom_x = Entry(window, width=10)
    custom_x.grid(column=1, row=5)

    custom_y = Entry(window, width=10)
    custom_y.grid(column=2, row=5)

    inclusion_number = Entry(window, width=10)
    inclusion_number.grid(column=1, row=6)

    radius_min = Entry(window, width=10)
    radius_min.grid(column=2, row=6)

    radius_max = Entry(window, width=10)
    radius_max.grid(column=3, row=6)

    neighbourhood = Combobox(window)
    neighbourhood['values'] = ("von Neumanna", "Moore’a", "Grain_Curvature")
    neighbourhood.grid(column=1, row=1)

    output_file = Combobox(window)
    output_file['values'] = ("non output file", "pdf", "png")
    output_file.grid(column=1, row=4)

    btn = Button(window, text="Add data", command=lambda: clicked(n, neighbourhood, r, output_file, custom_x, custom_y, inclusion_number, radius_max, radius_min, proc))
    btn.grid(column=0, row=8)

    window.mainloop()


def value_decide(list_value):
    value_set = set(list_value)
    value_dict = dict()
    result = list()
    for i in value_set:
        value_dict.update({i: list_value.count(i)})
    value_max = max(value_dict.values())
    for i in value_dict:
        if value_dict[i] == value_max:
            result.append(i)
    if len(result) == 1:
        return result[0]
    return random.choice(result)


def create_stop_line(board, one, two):
    board[one[0]][one[1]] = stop_point
    board[two[0]][two[1]] = stop_point
    x = one[1]
    y = one[0]
    while x != two[1]:
        if two[1] > one[1]:
            x = x + 1
        else:
            x = x - 1
        board[y][x] = stop_point
    while y != two[0]:
        if two[0] > one[0]:
            y = y + 1
        else:
            y = y - 1
        board[y][x] = stop_point
    return board


def create_inclusions(board, point, radius):
    for i in range(radius):
        try:
            create_stop_line(board, [point[0] - i, point[1]], [point[0], point[1] + i])
        except IndexError:
            pass

        try:
            create_stop_line(board, [point[0] - i, point[1]], [point[0], point[1] - i])
        except IndexError:
            pass

        try:
            create_stop_line(board, [point[0] + i, point[1]], [point[0], point[1] + i])
        except IndexError:
            pass

        try:
            create_stop_line(board, [point[0] + i, point[1]], [point[0], point[1] - i])
        except IndexError:
            pass


def one_grow(board, base, n, check_new, neighbourhood):
    board2 = copy.deepcopy(board)
    new_value = list()
    for i in range(n):
        for j in range(n):
            if board[i][j] not in check_new and board[i][j] != stop_point:
                if i != (n-1) and board[i+1][j] != base:
                    new_value.append(board[i+1][j])
                if j != (n-1) and board[i][j+1] != base:
                    new_value.append(board[i][j+1])
                if j != 0 and board[i][j-1] != base:
                    new_value.append(board[i][j-1])
                if i != 0 and board[i-1][j] != base:
                    new_value.append(board[i-1][j])
                if neighbourhood == "Moore’a":
                    if i != (n - 1) and j != 0 and board[i + 1][j-1] != base:
                        new_value.append(board[i + 1][j-1])
                    if j != (n - 1) and i != (n - 1) and board[i+1][j + 1] != base:
                        new_value.append(board[i+1][j + 1])
                    if i != 0 and j != (n - 1) and board[i-1][j + 1] != base:
                        new_value.append(board[i-1][j + 1])
                    if i != 0 and j != 0 and board[i - 1][j-1] != base:
                        new_value.append(board[i - 1][j-1])
                while new_value.count(stop_point):
                    new_value.remove(stop_point)

                if len(new_value) != 0:
                    decided_value = value_decide(new_value)
                    if decided_value != stop_point:
                        board2[i][j] = decided_value
                new_value.clear()
    return board2


def grain_curvature(board, base, n, check_new, chance):
    board2 = copy.deepcopy(board)
    rule2_list = list()
    rule3_list = list()
    for i in range(n):
        for j in range(n):
            if board[i][j] not in check_new and board[i][j] != stop_point:
                if i != (n-1) and board[i+1][j] != base and board[i+1][j] != stop_point:
                    rule2_list.append(board[i+1][j])
                if j != (n-1) and board[i][j+1] != base and board[i][j+1] != stop_point:
                    rule2_list.append(board[i][j+1])
                if j != 0 and board[i][j-1] != base and board[i][j-1] != stop_point:
                    rule2_list.append(board[i][j-1])
                if i != 0 and board[i-1][j] != base and board[i-1][j] != stop_point:
                    rule2_list.append(board[i-1][j])
                if i != (n - 1) and j != 0 and board[i + 1][j-1] != base and board[i + 1][j-1] != stop_point:
                    rule3_list.append(board[i + 1][j-1])
                if j != (n - 1) and i != (n - 1) and board[i+1][j + 1] != base and board[i+1][j + 1] != stop_point:
                    rule3_list.append(board[i+1][j + 1])
                if i != 0 and j != (n - 1) and board[i-1][j + 1] != base and board[i-1][j + 1] != stop_point:
                    rule3_list.append(board[i-1][j + 1])
                if i != 0 and j != 0 and board[i - 1][j-1] != base and board[i - 1][j-1] != stop_point:
                    rule3_list.append(board[i - 1][j-1])
                if len(rule2_list + rule3_list) != 0:
                    for k in set(rule2_list + rule3_list):
                        if (rule2_list + rule3_list).count(k) >= 5:
                            board2[i][j] = k
                if len(rule2_list) != 0:
                    for k in set(rule2_list):
                        if rule2_list.count(k) >= 3:
                            board2[i][j] = k

                if len(rule3_list) != 0:
                    for k in set(rule3_list):
                        if rule3_list.count(k) >= 3:
                            board2[i][j] = k
                if len(rule2_list + rule3_list) != 0:
                    decided_value = value_decide(rule2_list + rule3_list)
                    if decided_value != stop_point:
                        if random.randint(0, 100) <= chance:
                            board2[i][j] = decided_value
                rule2_list.clear()
                rule3_list.clear()
    return board2


if __name__ == '__main__':
    args = parse_arguments()
    gui_function()
