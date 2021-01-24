from functools import partial

import random
import math

from tkinter import *
from tkinter.ttk import *

class entity:
    # Name, x+1 number of dice if there are no subentities, +x to any roll in sub entities/this entity, +10*x% to budget in any sub entities/this entity, +x to the budget, sub entity
    def __init__(self, window, name="New Entity", pop=1, limit=1, control=False, ind=1, inf=1, sci=0, hea=0, sec=0, dip=0, gdef=0, sdef=0, entities=None):
        if entities is None:
            entities = []
        self.window = window
        self.name = name
        self.pop = pop
        self.limit = limit
        self.control = control
        self.ind = ind
        self.inf = inf
        self.sci = sci
        self.hea = hea
        self.sec = sec
        self.dip = dip
        self.gdef = gdef
        self.sdef = sdef
        self.entities = entities

        self.var = IntVar()
        self.var.set(int(self.control))

        # The entries for the entities stats

        self.name_e = Entry(self.window, width=15)
        self.name_e.delete(0, END)
        self.name_e.insert(0, self.name)

        self.pop_e = Entry(self.window, width=15)
        self.pop_e.delete(0, END)
        self.pop_e.insert(0, self.pop)

        self.limit_e = Entry(self.window, width=15)
        self.limit_e.delete(0, END)
        self.limit_e.insert(0, self.limit)

        self.ind_e = Entry(self.window, width=15)
        self.ind_e.delete(0, END)
        self.ind_e.insert(0, self.ind)

        self.inf_e = Entry(self.window, width=15)
        self.inf_e.delete(0, END)
        self.inf_e.insert(0, self.inf)

        self.sci_e = Entry(self.window, width=15)
        self.sci_e.delete(0, END)
        self.sci_e.insert(0, self.sci)

        self.hea_e = Entry(self.window, width=15)
        self.hea_e.delete(0, END)
        self.hea_e.insert(0, self.hea)

        self.sec_e = Entry(self.window, width=15)
        self.sec_e.delete(0, END)
        self.sec_e.insert(0, self.sec)

        self.dip_e = Entry(self.window, width=15)
        self.dip_e.delete(0, END)
        self.dip_e.insert(0, self.dip)

        self.gdef_e = Entry(self.window, width=15)
        self.gdef_e.delete(0, END)
        self.gdef_e.insert(0, self.gdef)

        self.sdef_e = Entry(self.window, width=15)
        self.sdef_e.delete(0, END)
        self.sdef_e.insert(0, self.sdef)

        # The pop limit Checkbutton

        self.control_c = Checkbutton(self.window, width=15, text="Population Control", variable=self.var)

        # The button to create a new entity

        self.add_btn = Button(self.window, width=15, text="Add Entity", command=self.add)

        # Button to remove sub entities

        self.remove_btn = []

        for i in range(len(self.entities)):
            self.remove_btn.append(Button(self.window, width=15, text="Remove Entity", command=partial(self.remove, i)))

    # Appends a new entity/remove button for each entry in data and calls load for each subentity with the data relevant to the current appended entiy
    def load(self, data):
        for i in data:
            self.entities.append(entity(self.window, i['name'], int(i['pop']), int(i['limit']), bool(int(i['contr'])), int(i['ind']), int(i['inf']), int(i['sci']), int(i['hea']), int(i['sec']), int(i['dip']), int(i['gdef']), int(i['sdef'])))
            self.remove_btn.append(Button(self.window, width=15, text="Remove Entity", command=partial(self.remove, len(self.entities)-1)))
            self.entities[-1].load(i['entities'])

    # Appends the current entity to data in a json friendly format, then calls it for each subentity
    def save(self, data):
        data.append({
            'name': '%s' % self.name,
            'pop': '%i' % self.pop,
            'limit': '%i' % self.limit,
            'contr': '%i' % self.control,
            'ind': '%i' % self.ind,
            'inf': '%i' % self.inf,
            'sci': '%i' % self.sci,
            'hea': '%i' % self.hea,
            'sec': '%i' % self.sec,
            'dip': '%i' % self.dip,
            'gdef': '%i' % self.gdef,
            'sdef': '%i' % self.sdef,
            'entities': []
        })
        for i in self.entities:
            i.save(data[-1]['entities'])

    # Calculates the Budget.
    # Adds raw to the current calculated budget
    # If there are no sub entities: roll log 10 (pop) - 3 - sdef dice, add ind + infr - (sci + hea + sec + dip)/2 - gdef + log 100 (pop) + bonus
    # If there are sub entities: calls CalcBudget for each sub entity with the bonus reduced by sdef*0.5
    def calcBudget(self, bonus=0):
        taxes = 0
        if len(self.entities) == 0:
            dice = int(math.log(self.pop,10))-3-self.sdef-int(self.control)*2
            # Lambda function to add free gdef
            gdefl = (lambda x: x-1 if (x>0) else 0)
            boni = int((self.ind+self.inf)*5 - (self.sci + self.hea + self.sec + self.dip*5)/2 - gdefl(self.gdef)*5 +math.log(self.pop,100))+bonus
            multiplier = 1
            if dice < 0:
                dice = dice * (-1)
                multiplier = -1
            for j in range(dice-int(self.control)):
                taxes += (random.randint(1, 20))*multiplier
            return taxes+boni
        else:
            for i in self.entities:
                taxes += i.calcBudget(bonus-(self.sdef*0.5))
            return taxes

    def growPop(self, multipler):
        if len(self.entities)==0 and self.control==False:
            self.pop += int((multipler/100)*int(self.pop)*(1-int(self.pop)/int(self.limit)))
        else:
            for i in self.entities:
                i.growPop(multipler)

    def place(self, col, row):

        # Placing new Entries

        self.name_e = Entry(self.window, width=15)
        self.name_e.delete(0, END)
        self.name_e.insert(0, self.name)
        self.name_e.grid(column=col, row=row)

        self.pop_e = Entry(self.window, width=15)
        self.pop_e.delete(0, END)
        self.pop_e.insert(0, self.pop)
        self.pop_e.grid(column=col, row=row+1)

        self.limit_e = Entry(self.window, width=15)
        self.limit_e.delete(0, END)
        self.limit_e.insert(0, self.limit)
        self.limit_e.grid(column=col, row=row+2)

        if len(self.entities) == 0:
            self.ind_e = Entry(self.window, width=15)
            self.ind_e.delete(0, END)
            self.ind_e.insert(0, self.ind)
            self.ind_e.grid(column=col, row=row+3)

            self.inf_e = Entry(self.window, width=15)
            self.inf_e.delete(0, END)
            self.inf_e.insert(0, self.inf)
            self.inf_e.grid(column=col, row=row+4)

            self.sci_e = Entry(self.window, width=15)
            self.sci_e.delete(0, END)
            self.sci_e.insert(0, self.sci)
            self.sci_e.grid(column=col, row=row+5)

            self.hea_e = Entry(self.window, width=15)
            self.hea_e.delete(0, END)
            self.hea_e.insert(0, self.hea)
            self.hea_e.grid(column=col, row=row+6)

            self.sec_e = Entry(self.window, width=15)
            self.sec_e.delete(0, END)
            self.sec_e.insert(0, self.sec)
            self.sec_e.grid(column=col, row=row+7)

            self.dip_e = Entry(self.window, width=15)
            self.dip_e.delete(0, END)
            self.dip_e.insert(0, self.dip)
            self.dip_e.grid(column=col, row=row+8)

            self.gdef_e = Entry(self.window, width=15)
            self.gdef_e.delete(0, END)
            self.gdef_e.insert(0, self.gdef)
            self.gdef_e.grid(column=col, row=row+9)

            self.sdef_e = Entry(self.window, width=15)
            self.sdef_e.delete(0, END)
            self.sdef_e.insert(0, self.gdef)
            self.sdef_e.grid(column=col, row=row+10)

            # Placing the Checkbutton to Control pop

            self.control_c = Checkbutton(self.window, width=15, text="Population Control", variable=self.var)
            self.control_c.grid(column=col, row=row+11)

            # Placing the button to add new entities

            self.add_btn = Button(self.window, width=15, text="Add Entity", command=self.add)
            self.add_btn.grid(column=col, row=row+12)

        else:

            # Placing the button to add new entities

            self.add_btn = Button(self.window, width=15, text="Add Entity", command=self.add)
            self.add_btn.grid(column=col, row=row+4)

            self.remove_btn = []

            # Remove entity buttons
            for i in range(len(self.entities)):
                self.remove_btn.append(Button(self.window, width=15, text="Remove Entity", command=partial(self.remove, i)))

            # Calls place on any sub entities
            row+=4
            for i in range(len(self.entities)):
                col+=1
                self.remove_btn[i].grid(column=col, row=row)
                col = self.entities[i].place(col, row+1)

        return col

    # Destroys all gui elements, then calls destroy_gui on each sub entity
    def destroy_gui(self):
        self.name_e.destroy()
        self.pop_e.destroy()
        self.limit_e.destroy()
        self.ind_e.destroy()
        self.inf_e.destroy()
        self.sci_e.destroy()
        self.hea_e.destroy()
        self.sec_e.destroy()
        self.dip_e.destroy()
        self.gdef_e.destroy()
        self.sdef_e.destroy()

        self.control_c.destroy()

        self.add_btn.destroy()

        for i in self.remove_btn:
            i.destroy()

        for i in self.entities:
            i.destroy_gui()

    # Updates the entities values with the values in the gui entry fields, then calls update on each sub entity
    def update(self):
        if len(self.entities) == 0:
            self.name = self.name_e.get()
            self.pop = int(self.pop_e.get())
            self.limit = int(self.limit_e.get())
            self.control = bool(int(self.var.get()))
            self.ind = int(self.ind_e.get())
            self.inf = int(self.inf_e.get())
            self.sci = int(self.sci_e.get())
            self.hea = int(self.hea_e.get())
            self.sec = int(self.sec_e.get())
            self.dip = int(self.dip_e.get())
            self.gdef = int(self.gdef_e.get())
            self.sdef = int(self.sdef_e.get())
        else:
            self.name = self.name_e.get()
            self.pop = 0
            self.limit = 0
            self.control = bool(int(self.var.get()))
            for i in self.entities:
                i.update()
                self.pop += i.pop
                self.limit += i.limit


    # Adds a new sub entity
    def add(self):
        self.entities.append(entity(self.window))
        self.remove_btn.append(Button(self.window, width=15, text="Remove Entity", command=partial(self.remove, len(self.entities)-1)))

    # Removes a sub entity
    def remove(self, number):
        for i in range(len(self.remove_btn)):
            if i == number:
                self.destroy_gui()
                self.entities.pop(i)
                self.remove_btn.pop(i)

    # Turn the entity into a human readable String, then does the same for any sub entities
    def toString(self):
        line = "Name: %s, Pop: %i, Limit: %i, Control: %s, Ind: %i, Inf: %i, Sci: %i, Hea: %i, Sec: %i, Dip: %i, GDef: %i, SDef: %i\n" % (self.name, self.pop, self.limit, self.control, self.ind, self.inf, self.sci, self.hea, self.sec, self.dip, self.gdef, self.sdef)
        for i in self.entities:
            line += "    "+i.toString()
        return line
