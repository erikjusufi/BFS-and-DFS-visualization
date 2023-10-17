from tkinter import *
import random
from queue import Queue
import time

from matrix import Matrix

class App(Frame):
    '''
    Application that draws a matrix and allows user to change color of elements in matrix
    It uses BFS algorithm to change color of all elements in matrix that are connected to the element that user clicked on.
    Elements are connected if between there is no element with # sign
    '''
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Matrix")
        # windows size in pixels
        self.master.geometry("400x300")
        # window size unchangeable
        self.master.resizable(True, True)
        self.grid()
        self.interface()
        

    def interface(self):
        # label for dimensions
        self.label_dim = Label(self, text="Matrix dimensions:")
        self.label_dim.grid(row=0, column=0, sticky=W)

        # label for num of rows
        self.label_rows = Label(self, text="# of rows:")
        self.label_rows.grid(row=1, column=0, sticky=W)

        # input for num of rows
        self.row_num = StringVar()
        self.entry_rows = Entry(self, textvariable=self.row_num, width = 2)
        self.entry_rows.grid(row=1, column=1, sticky=W)
        
        # label for num of columns
        self.label_columns = Label(self, text="# of columns:")
        self.label_columns.grid(row=2, column=0, sticky=W)

        # input for num of columns
        self.column_num = StringVar()
        self.entry_columns = Entry(self, textvariable=self.column_num, width = 2)
        self.entry_columns.grid(row=2, column=1, sticky=W)

        # button for time delay
        self.label_delay = Label(self, text="Time delay (between 0 and 1):")
        self.label_delay.grid(row=3, column=0, sticky=W)

        # input for time delay
        self.delay = StringVar()
        self.entry_delay = Entry(self, textvariable=self.delay, width = 2)
        self.entry_delay.grid(row=3, column=1, sticky=W)

        # button for confirming dimensions
        self.button_dim = Button(self, text="Confirm", command=self.confirm_dimensions)
        self.button_dim.grid(row=4, column=0, sticky=W)

        # button for application exit
        self.button_exit = Button(self, text="Exit", command=self.master.destroy)
        self.button_exit.grid(row=4, column=1, sticky=W)

    def confirm_dimensions(self):
        '''
        Function initializes matrix object and draws matrix
        '''
        self.matrix = Matrix(self.row_num.get(), self.column_num.get())
        
        # random generate # in each row 2 times
        for i in range(int(self.row_num.get())):
            # code that generates # in completely random column
            '''
            i1 = random.randint(0, int(self.column_num.get())-1)
            while i2 == i1:
                i2 = random.randint(0, int(self.column_num.get())-1)
            '''
            # code that generates # in first half of row and in second half of row
            i1 = random.randint(0, int((int(self.column_num.get())-1)/2))
            i2 = random.randint(int((int(self.column_num.get())-1)/2) +1, int(self.column_num.get())-1)

            self.matrix[i, i1] = "#"
            self.matrix[i, i2] = "#"

        # draw matrix
        # when # is generated, button is red and has no function
        # when o is generated, button is white and has function to change color
        for i in range(int(self.row_num.get())):
            for j in range(int(self.column_num.get())):
                # button for # sign
                if self.matrix[i, j] == "#":
                    self.matrix[i,j] = Button(self,width=3, height=1, text="#", bg="red", fg="white")
                    self.matrix[i,j].grid(row=i+5, column=j+2)
                # button for o sign
                else:
                    self.matrix[i,j] = Button(self,width=3, height=1, text="o", bg="white", fg="black")
                    self.matrix[i,j].grid(row=i+5, column=j+2)
                    self.matrix[i,j].bind("<Button-1>", self.change_color)
 
    def change_color(self, event):
        '''
        Function changes color of all elements in matrix that are connected to the element that user clicked on.
        Elements are connected if between there is no element with # sign
        '''
        # queue for BFS algorithm
        queue = Queue()
        # set of visited elements
        visited = set()

        # position of element that user clicked on
        position = event.widget.grid_info()
        i = position["row"] -5 # shift because of grid display
        j = position["column"] -2 # shift because of grid display

        # get new color
        color = self.random_color()
        # change color of element that user clicked on
        self.matrix[i,j].configure(bg=color)
        
        # add initial element to queue and set of visited elements
        queue.put((i,j))
        visited.add((i,j))

        # ==================================
        # BFS ALGORITHM
        # ==================================
        # while queue is not empty, get element from queue and check its neighbors, if they are not in set of visited elements, add them to queue and set of visited elements
        while not queue.empty():
            i, j = queue.get()
            time.sleep(float(self.delay.get()))
            if j != 0 and (i,j-1) not in visited:
                if self.matrix[i,j-1]["text"] != "#":
                    self.matrix[i,j-1].configure(bg=color)
                    queue.put((i,j-1))
                    visited.add((i,j-1))
            if j != int(self.column_num.get())-1 and (i,j+1) not in visited:
                if self.matrix[i,j+1]["text"] != "#":
                    self.matrix[i,j+1].configure(bg=color)
                    queue.put((i,j+1))
                    visited.add((i,j+1))
            if i != 0 and (i-1,j) not in visited:
                if self.matrix[i-1,j]["text"] != "#":
                    self.matrix[i-1,j].configure(bg=color)
                    queue.put((i-1,j))
                    visited.add((i-1,j))
            if i != int(self.row_num.get())-1 and (i+1,j) not in visited:
                if self.matrix[i+1,j]["text"] != "#":
                    self.matrix[i+1,j].configure(bg=color)
                    queue.put((i+1,j))
                    visited.add((i+1,j))
            self.update()

    def random_color(self):
        '''
        Function generates random color in hexadecimal format
        '''
        color = "#"
        for i in range(6):
            color += random.choice("0123456789abcdef")
        return color

if __name__ == "__main__":
    root = App(Tk())
    root.mainloop()