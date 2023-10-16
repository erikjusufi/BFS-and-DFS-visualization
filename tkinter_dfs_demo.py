from tkinter import *
import random
from queue import Queue

# definicija klase Matrica
class Matrica:
    def __init__(self, n, m=None):
        # ukoliko je zadan samo n argument, matrica je kvadratna nxn
        self.n = int(n)
        if m == None:
            self.m = int(n)
        else:
            self.m = int(m)
        self.mat  = dict()

    def __setitem__(self, key, value):
        self.mat[key] = value

    def __getitem__(self, key):
        return self.mat.get(key, 0)
    
    def __str__(self):
        s = ""
        for i in range(self.n):
            for j in range(self.m):
                s += str(self[i, j]) + " "
            s += "\n"
        return s
    
# definicija klase App
class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Matrica")
        # veličina prozora u pikselima
        self.master.geometry("400x400")
        # postavljamo da se veličina prozora ne može mijenjati
        #self.master.resizable(False, False)
        self.grid()
        self.interface()
        

    def interface(self):
        # naljepnica za unos dimenzija matrice
        self.label_dimenzije = Label(self, text="Dimenzije matrice:")
        self.label_dimenzije.grid(row=0, column=0, sticky=W)

        # naljepnica za broj redaka
        self.label_redaka = Label(self, text="Broj redaka:")
        self.label_redaka.grid(row=1, column=0, sticky=W)

        # unos broja redaka
        self.broj_redaka = StringVar()
        self.entry_redaka = Entry(self, textvariable=self.broj_redaka, width = 2)
        self.entry_redaka.grid(row=1, column=1, sticky=W)
        
        # naljepnica za broj stupaca
        self.label_stupaca = Label(self, text="Broj stupaca:")
        self.label_stupaca.grid(row=2, column=0, sticky=W)

        # unos broja stupaca
        self.broj_stupaca = StringVar()
        self.entry_stupaca = Entry(self, textvariable=self.broj_stupaca, width = 2)
        self.entry_stupaca.grid(row=2, column=1, sticky=W)

        # gumb za potvrdu unosa dimenzija
        self.gumb_dimenzije = Button(self, text="Potvrdi", command=self.potvrdi_dimenzije)
        self.gumb_dimenzije.grid(row=3, column=0, sticky=W)

        # naljepnica za prikaz broja redaka
        self.label_redaka = Label(self, text="Broj redaka:")
        self.label_redaka.grid(row=4, column=0, sticky=W)

        # prikaz broja redaka
        self.label_redaka = Label(self, textvariable=self.broj_redaka)
        self.label_redaka.grid(row=4, column=1, sticky=W)

        # naljepnica za prikaz broja stupaca
        self.label_stupaca = Label(self, text="Broj stupaca:")
        self.label_stupaca.grid(row=5, column=0, sticky=W)

        # prikaz broja stupaca
        self.label_stupaca = Label(self, textvariable=self.broj_stupaca)
        self.label_stupaca.grid(row=5, column=1, sticky=W)

        # gumb za izlaz iz programa
        self.gumb_izlaz = Button(self, text="Izlaz", command=self.master.destroy)
        self.gumb_izlaz.grid(row=6, column=0, sticky=W)

    def potvrdi_dimenzije(self):
        '''
        Funkcija koja se poziva pritiskom na gumb "Potvrdi" i inicializira matricu
        '''
        # inicijalizacija objekta MAtrica
        self.matrica = Matrica(self.broj_redaka.get(), self.broj_stupaca.get())
        
        # random generiraj dva znaka # u svakom retku
        for i in range(int(self.broj_redaka.get())):
            # kod koji generira znakove potpuno nasumično
            #i1 = random.randint(0, int(self.broj_stupaca.get())-1)
            #while i2 == i1:
            #    i2 = random.randint(0, int(self.broj_stupaca.get())-1)

            # kod koji generira prvi znak # u prvoj polovici redka, a drugi znak # u drugoj polovici redka
            i1 = random.randint(0, int((int(self.broj_stupaca.get())-1)/2))
            i2 = random.randint(int((int(self.broj_stupaca.get())-1)/2) +1, int(self.broj_stupaca.get())-1)
            self.matrica[i, i1] = "#"
            self.matrica[i, i2] = "#"

        # crtanje matrice
        # pritiskom na element matrice, obojati sve elemente matrice do rubova matrice ili do prvog znaka #
        for i in range(int(self.broj_redaka.get())):
            for j in range(0,int(self.broj_stupaca.get())):
                # gumb za znak # koji nema funkciju promijeni boju
                if self.matrica[i, j] == "#":
                    self.matrica[i,j] = Button(self,width=3, height=1, text="#", bg="red", fg="white")
                    self.matrica[i,j].grid(row=i+10, column=j+2)
                # gumb za znak o koji ima funkciju promijeni boju
                else:
                    self.matrica[i,j] = Button(self,width=3, height=1, text="o", bg="white", fg="black")
                    self.matrica[i,j].grid(row=i+10, column=j+2)
                    self.matrica[i,j].bind("<Button-1>", self.promijeni_boju)
                    
        

        
                

    def promijeni_boju(self, event):
        '''
        Funkcija koja se poziva pritiskom na gumb "o" i mijenja boju elementa i broji udaljenost do susjednih elemenata
        sve dok ne naiđe na rub matrice ili na znak #
        '''
        # incijalizacija reda i skupa posjećenih elemenata
        queue = Queue()
        visited = set()

        # dohvaćanje pozicije pritisnutog elementa matrice
        pozicija = event.widget.grid_info()
        i = pozicija["row"]-10 # pomaknut zbog prikaza u gridu za 10
        j = pozicija["column"]-2 # pomaknut zbog prikaza u gridu za 2

        # nova boja
        boja = self.random_color()
        # promijeni boju pritisnutog elementa
        self.matrica[i,j].configure(bg=boja, fg="white", text="0")
        
        # dodaj inicijalno pritisnuti element u red i skup posjećenih elemenata, uz njega dodaj i broj koraka do sljedećeg elementa
        queue.put((i,j,1))
        visited.add((i,j))

        # BFS algoritam
        # dok red nije prazan, dohvati element iz reda i provjeri njegove susjede
        while not queue.empty():
            
            # dohvati element i broj koraka potreban do njegovih susjeda
            i, j, broj = queue.get()

            if j != 0 and (i,j-1) not in visited:
                if self.matrica[i,j-1]["text"] != "#":
                    # promijeni tekst elementa u broj koraka do njega
                    self.matrica[i,j-1].configure(text=broj)
                    # dodaj novi element u red i skup posjećenih elemenata s uvećanim brojem koraka
                    queue.put((i,j-1, broj+1))
                    visited.add((i,j-1))
            if j != int(self.broj_stupaca.get())-1 and (i,j+1) not in visited:
                if self.matrica[i,j+1]["text"] != "#":
                    # promijeni tekst elementa u broj koraka do njega
                    self.matrica[i,j+1].configure(text=broj)
                    # dodaj novi element u red i skup posjećenih elemenata s uvećanim brojem koraka
                    queue.put((i,j+1, broj+1))
                    visited.add((i,j+1))
            if i != 0 and (i-1,j) not in visited:
                if self.matrica[i-1,j]["text"] != "#":
                    # promijeni tekst elementa u broj koraka do njega
                    self.matrica[i-1,j].configure(text=broj)
                    # dodaj novi element u red i skup posjećenih elemenata s uvećanim brojem koraka
                    queue.put((i-1,j, broj+1))
                    visited.add((i-1,j))
            if i != int(self.broj_redaka.get())-1 and (i+1,j) not in visited:
                if self.matrica[i+1,j]["text"] != "#":
                    # promijeni tekst elementa u broj koraka do njega
                    self.matrica[i+1,j].configure(text=broj)
                    # dodaj novi element u red i skup posjećenih elemenata s uvećanim brojem koraka
                    queue.put((i+1,j, broj+1))
                    visited.add((i+1,j))
    

    def random_color(self):
        '''
        Funkcija koja generira nasumičnu boju u hex zapisu
        '''
        color = "#"
        for i in range(6):
            color += random.choice("0123456789abcdef")
        return color

if __name__ == "__main__":
    root = App(Tk())
    root.mainloop()