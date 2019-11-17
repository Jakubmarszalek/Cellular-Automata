import random
import copy
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
from ast import literal_eval
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
base = 2


def clicked(n, neighbourhood, r, output_file, custom_x, custom_y):
    custom = dict()
    custom_x = custom_x.get().split(" ")
    custom_y = custom_y.get().split(" ")
    if custom_x != [""]:
        for i in range(len(custom_x)):
            custom.update({"custom{0}".format(i+1): [int(custom_x[i]), int(custom_y[i])]})

    if n.get() != "":
        size = int(n.get())
    else:
        size = 200

    if r.get() != "":
        random = int(r.get())
    else:
        random = 25

    image = main(size, custom, random, neighbourhood.get(), output_file.get(), base)


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
    window = Tk()

    window.title("Welcome to LikeGeeks app")
    window.geometry('450x150')

    lbl = Label(window, text="the size of the square")
    lbl.grid(column=0, row=0)

    lbl = Label(window, text="type of Neighbourhood")
    lbl.grid(column=0, row=1)

    lbl = Label(window, text="Number of random start place")
    lbl.grid(column=0, row=2)

    lbl = Label(window, text="Type of output file")
    lbl.grid(column=0, row=3)

    lbl = Label(window, text="parametr of custom start point: X and Y")
    lbl.grid(column=0, row=4)

    n = Entry(window, width=10)
    n.grid(column=1, row=0)

    r = Entry(window, width=10)
    r.grid(column=1, row=2)

    custom_x = Entry(window, width=10)
    custom_x.grid(column=1, row=4)

    custom_y = Entry(window, width=10)
    custom_y.grid(column=2, row=4)

    neighbourhood = Combobox(window)
    neighbourhood['values'] = ("von Neumanna", "Moore’a")
    neighbourhood.grid(column=1, row=1)

    output_file = Combobox(window)
    output_file['values'] = ("non output file", "pdf", "png")
    output_file.grid(column=1, row=3)

    btn = Button(window, text="Add data", command=lambda: clicked(n, neighbourhood, r, output_file, custom_x, custom_y))
    btn.grid(column=0, row=5)

    #x = "image.png" #openfn()
    #img = Image.open(x)
    #img = img.resize((250, 250), Image.ANTIALIAS)
    #img = ImageTk.PhotoImage(img)
    #panel = Label(window, image=img)
    #panel.image = img
    #panel.grid(column=0, row =6)
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


def one_grow(board, base, n, check_new, neighbourhood):
    board2 = copy.deepcopy(board)
    new_value = list()
    for i in range(n):
        for j in range(n):
            if board[i][j] not in check_new:
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
                if len(new_value) != 0:
                    board2[i][j] = value_decide(new_value)
                new_value.clear()
    return board2


def main(n, custom, random_start, neighbourhood, export, base):
    new = {}
    check_new = []
    Z = list()
    board = []

    for x in range(0, n):
        board.append([])
        for y in range(0, n):
            board[x].append(base)
    p = base + 1
    #custom = literal_eval(custom)
    for i in custom:
        try:
            board[custom[i][0]][custom[i][1]] = p
            custom[i].append(p)
        except IndexError:
            print("Custom start point not in declare box value")
            sys.exit(1)
        new.update({i: [custom[i][0], custom[i][1], p]})
        p = p + 1

    for i in range(p, p + random_start):
        while 1:
            x = random.randint(0, n - 1)
            y = random.randint(0, n - 1)
            if board[x][y] not in new:
                board[x][y] = i
                break
        new.update({"random{0}".format(i): [x, y, i]})

    for i in new:
        check_new.append(new[i][2])

    p = 0
    while 1:
        p = p + 1
        Z.clear()
        for j in board:
            Z.extend(j)
        board = one_grow(board, base, n, check_new, neighbourhood)
        print(str(100 - Z.count(base)*100/(n*n))[0:5]+"%")
        image = np.zeros(len(Z))
        for i in range(len(image)):
            image[i] = Z[i]
        image = image.reshape((n, n))
        plt.matshow(image)
        plt.savefig('png_file/output{0}.png'.format(p))
        plt.close()
        if not base in Z:
            break
    print("Proces end after {0} iteration".format(p))
    image = np.zeros(len(Z))
    for i in range(len(image)):
        image[i] = Z[i]
    for i in new:
        print(str(i)+": start point:" + "[x:" + str(new[i][0]) + " y:" + str(new[i][1]) + "] "+str((Z.count(new[i][2])*100)/(n*n)) + "%")
    image = image.reshape((n, n))
    plt.matshow(image)
    if export == "png":
        plt.savefig('output.png')
    elif export == "pdf":
        plt.savefig('output.pdf')
    plt.show()
    return(image)



if __name__ == '__main__':
    args = parse_arguments()
    #main(args.n, args.custom, args.random, args.Neighbourhood, args.export, base)
    gui_function()
