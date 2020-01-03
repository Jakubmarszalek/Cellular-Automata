import random
import copy
import matplotlib.pyplot as plt
import numpy as np
import argparse
import io
import copy
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

board = []
base = 2
stop_point = base - 1
new_parametrs = dict()


def gui_function():
    def main(n, random_start, neighbourhood, export, base, inclusion_number, radius_min, radius_max, proc, DP_structure, DP_removal):
        global board
        new = {}
        check_new = []
        Z = list()
        delete = []
        sets = []
        p = base + 1
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

        if DP_structure != "yes":
            board = new_board(n, base)
        else:

            for i in board:
                sets = sets + list(set(i))
                sets = list(set(sets))
            for i in sets:
                if random.randint(0, 100) < int(DP_removal):
                    delete = delete + [i]
            board = clean_board(board, delete, base)

        for i in range(p, p + random_start):
            while 1:
                while i in sets:
                    i = i + random_start
                x = random.randint(0, n - 1)
                y = random.randint(0, n - 1)
                if board[x][y] == base:
                    board[x][y] = i
                    break
            new.update({"random{0}".format(i): [x, y, i]})

        for i in new:
            check_new.append(new[i][2])
        for i in sets:
            check_new.append(i)
        p = 0
        old_count = 0

        while 1:
            p = p + 1
            Z.clear()
            for j in board:
                Z.extend(j)
            if neighbourhood == "Grain_Curvature":
                board = grain_curvature(board, base, check_new, int(proc), stop_point, sets)
            else:
                board = one_grow(board, base, check_new, neighbourhood, stop_point, sets)
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
        return (plt)

    def new_board(n, base):
        board = []
        for x in range(0, n):
            board.append([])
            for y in range(0, n):
                board[x].append(base)
        return board

    def clean_board(board, delete, base):
        n = len(board)
        for x in range(0, n):
            for y in range(0, n):
                if board[x][y] in delete:
                    board[x][y] = base
        return board

    def clicked(paremetrs):
        global new_parametrs
        if len(new_parametrs) != 0:
            paremetrs = new_parametrs
        for i in paremetrs:
            try:
                if paremetrs[i]["value"].get() != "":
                    try:
                        paremetrs[i]["value"] = int(paremetrs[i]["value"].get())
                    except:
                        paremetrs[i]["value"] = paremetrs[i]["value"].get()
                else:
                    paremetrs[i]["value"] = paremetrs[i]["defult"]
            except:
                pass
        plt = main(paremetrs['size']["value"], paremetrs["number_start_place"]["value"],  paremetrs["neighbourhood"]["value"], paremetrs["output_file"]["value"], base, paremetrs["inclusion_number"]["value"], paremetrs["inclusion_min"]["value"],
                     paremetrs["inclusion_max"]["value"], paremetrs["proc_grain"]["value"], paremetrs["DP_structure"]["value"], paremetrs["%_removal"]["value"])

        new_parametrs = paremetrs_creator()
        plt.show()

    def callback(proc_end, plt):
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        img = img.resize((500, 500), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(window, image=img)
        panel.image = img
        panel.grid(column=0, row=11)
        panel2 = Label(window, text=proc_end)
        panel2.grid(column=2, row=11)

    window = Tk()
    window.title("Welcome to Multiscale modeling app")
    window.geometry('800x720')

    def paremetrs_creator():
        paremetrs = dict()
        paremetrs["size"] = {"value": Entry(window, width=10), "defult": 200, "name": "the size of the square"}

        paremetrs["neighbourhood"] = {"value": Combobox(window), "defult": "von Neumanna", "name": "type of Neighbourhood"}
        paremetrs["neighbourhood"]["value"]["values"] = ("von Neumanna", "Moore’a", "Grain_Curvature")

        paremetrs["proc_grain"] = {"value": Entry(window, width=10), "defult": 40, "name": "% for Grain_Curvature"}

        paremetrs["number_start_place"] = {"value": Entry(window, width=10), "defult": 25, "name": "Number of random start place"}

        paremetrs["output_file"] = {"value": Combobox(window), "defult": "non output file", "name": "Type of output file"}
        paremetrs["output_file"]["value"]["values"] = ("non output file", "pdf", "png")

        paremetrs["inclusion_number"] = {"value": Entry(window, width=10), "defult": 5, "name": "Number of random inclusions point"}

        paremetrs["inclusion_min"] = {"value": Entry(window, width=10), "defult": 1, "name": "minimal radius of inclusions"}

        paremetrs["inclusion_max"] = {"value": Entry(window, width=10), "defult": 5, "name": "maximal radius of inclusions"}

        paremetrs["DP_structure"] = {"value": Combobox(window), "defult": "no",
                                    "name": "DP_structure?"}
        paremetrs["DP_structure"]["value"]["values"] = ("yes", "no")

        paremetrs["%_removal"] = {"value": Entry(window, width=10), "defult": 80,
                                      "name": "DP Structure: % of Removal grains"}
        j = 0
        for i in paremetrs:
            Label(window, text=paremetrs[i]["name"]).grid(column=0, row=j)
            paremetrs[i]["value"].grid(column=1, row=j)
            j += 1
        return paremetrs

    paremetrs = paremetrs_creator()
    btn = Button(window, text="Add data", command=lambda: clicked(paremetrs))
    btn.grid(column=0, row=10)
    window.mainloop()


def value_decide(list_value, list_delete):
    new_value = copy.deepcopy(list_value)
    for i in list_value:
        if i in list_delete:
            new_value.remove(i)
    list_value = new_value
    value_set = set(list_value)
    value_dict = dict()
    result = list()
    for i in value_set:
        value_dict.update({i: list_value.count(i)})
    try:
        value_max = max(value_dict.values())
    except:
        return stop_point
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


def one_grow(board, base, check_new, neighbourhood, stop_point, list_delete):
    n = len(board)
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
                    decided_value = value_decide(new_value, list_delete)
                    if decided_value != stop_point:
                        board2[i][j] = decided_value
                new_value.clear()
    return board2


def grain_curvature(board, base, check_new, chance, stop_point, list_delete):
    n = len(board)
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
                    decided_value = value_decide(rule2_list + rule3_list, list_delete)
                    if decided_value != stop_point:
                        if random.randint(0, 100) <= chance:
                            board2[i][j] = decided_value
                rule2_list.clear()
                rule3_list.clear()
    return board2

if __name__ == '__main__':
    gui_function()
