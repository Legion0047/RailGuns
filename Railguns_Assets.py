import json
import os
from tkinter import *
from tkinter.ttk import *

from Railguns_Entity import entity as entity

class Assets(Frame):

    # Calls the save function which then calls it rekursively. Data is then dumped in a pretty JSON file.
    def save(self):
        data = []
        self.faction.save(data)
        js = {}
        js['Bonus'] = int(self.bonus_e.get())
        js['Assets'] = data
        with open('data.json', 'w') as outfile:
            json.dump(js, outfile, indent=4)

    # Opens the json file the data is stored in and reads it. It then adds the top level entity (Faction) before calling it's load function, which appends entities rekursively.
    def load(self):
        if os.path.isfile('data.json'):
            with open('data.json') as json_file:
                data = json.load(json_file)

                self.bonus_e.delete(0, END)
                self.bonus_e.insert(0, data['Bonus'])

                i = data['Assets']
                faction = entity(self, i[0]['name'], int(i[0]['pop']), int(i[0]['limit']), bool(int(i[0]['contr'])), int(i[0]['ind']), int(i[0]['inf']), int(i[0]['sci']), int(i[0]['hea']), int(i[0]['sec']), int(i[0]['dip']), int(i[0]['gdef']), int(i[0]['sdef']))
                faction.load(i[0]['entities'])
                return faction
        else:
            return entity(self)


   # Calls update of the currently selected faction every 1000ms, then call itself
    def clock(self):
        self.update()
        self.after(1000, self.clock)  # run itself again after 1000 ms

    # Calls the Budget function of the currently selected, then displays the result in the appropriate label
    def budget(self):
        self.budget_lbl.configure(text=self.faction.calcBudget())

    # Updates the stats of the entities
    def update(self):
        self.faction.update()

    def refresh(self):
        self.faction.destroy_gui()
        self.faction.place(1, 3)

    def pop(self):
        self.pop_lbl.configure(text=int((int(self.pop_g.get())/100)*int(self.pop_c.get())*(1-int(self.pop_c.get())/int(self.pop_l.get()))))

    def pop_all(self):
        self.faction.growPop(5)
        self.refresh()

    def __init__(self, window):
        super(Assets, self).__init__(window)

        # Bonus Label/Entry

        self.bonus_lbl = Label(self, width=15, text="Money Bonus:")
        self.bonus_lbl.grid(column=0, row=0, sticky=W)

        self.bonus_e = Entry(self, width=15)
        self.bonus_e.insert(0, 0)
        self.bonus_e.grid(column=1, row=0, sticky=W)


        # Calculate Budget button/label

        self.budget_btn = Button(self, width=15, text="Calculate Budget", command=self.budget)
        self.budget_btn.grid(column=2, row=0, sticky=W)

        self.budget_lbl = Label(self, width=15, text="0")
        self.budget_lbl.grid(column=3, row=0, sticky=W)

        # Increase Pop

        self.pop_g = Entry(self, width=15)
        self.pop_g.insert(0, "growth")
        self.pop_g.grid(column=0, row=1, sticky=W)

        self.pop_c = Entry(self, width=15)
        self.pop_c.insert(0, "pop")
        self.pop_c.grid(column=1, row=1, sticky=W)

        self.pop_l = Entry(self, width=15)
        self.pop_l.insert(0, "limit")
        self.pop_l.grid(column=2, row=1, sticky=W)

        self.pop_lbl = Label(self, width=15, text="0")
        self.pop_lbl.grid(column=3, row=1, sticky=W)

        self.pop_btn = Button(self, width=15, text="Grow Population", command=self.pop)
        self.pop_btn.grid(column=4, row=1, sticky=W)

        self.pop_all_btn = Button(self, width=15, text="Grow all Population", command=self.pop_all)
        self.pop_all_btn.grid(column=5, row=1, sticky=W)

        # Refresh Button

        self.refresh_btn = Button(self, width=15, text="Refresh Page", command=self.refresh)
        self.refresh_btn.grid(column=4, row=0, sticky=W)

        # Save button

        self.save_btn = Button(self, width=15, text="Save", command=self.save)
        self.save_btn.grid(column=5, row=0, sticky=W)

        # A line of gray blanks to make it look better

        for i in range(20):
            blank = Label(self, width=20, background="gray")
            blank.grid(column=i, row=2)

        # Labels

        name = Label(self, text="Name", width=15)
        name.grid(column=0, row=3)

        pop = Label(self, text="Population", width=15)
        pop.grid(column=0, row=4)

        limit = Label(self, text="Population Limit", width=15)
        limit.grid(column=0, row=5)

        name = Label(self, text="Name", width=15)
        name.grid(column=1, row=8)

        pop = Label(self, text="Population", width=15)
        pop.grid(column=1, row=9)

        limit = Label(self, text="Population Limit", width=15)
        limit.grid(column=1, row=10)

        ind = Label(self, text="Industry", width=15)
        ind.grid(column=1, row=11)

        inf = Label(self, text="Infrastructure", width=15)
        inf.grid(column=1, row=12)

        sci = Label(self, text="Science", width=15)
        sci.grid(column=1, row=13)

        hea = Label(self, text="Health", width=15)
        hea.grid(column=1, row=14)

        sec = Label(self, text="Security", width=15)
        sec.grid(column=1, row=15)

        dip = Label(self, text="Diplomacy", width=15)
        dip.grid(column=1, row=16)

        gdef = Label(self, text="Ground Defense", width=15)
        gdef.grid(column=1, row=17)

        sdef = Label(self, text="Space Defense", width=15)
        sdef.grid(column=1, row=18)

        # Loads from the file, if it exists

        self.faction = self.load()
        self.refresh()

        # Start the Clock
        self.clock()

if __name__ == "__main__":
    window = Tk()
    window.geometry('1280x720')
    window.title("Tau Empire")

    main = Assets(window)
    main.pack(fill="both", expand=True)

    window.mainloop()