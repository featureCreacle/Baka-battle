# #режим приблуды: 'ClrSeg', 'Worm', 'Conway'
gm = 1
if gm == 1:
    game_mode = 'BakaFight'
elif gm == 2:
    game_mode = 'ClrSeg'
elif gm == 3:
    game_mode = 'Conway'


field_width = 50  # клеток по иксу
field_height = 30  # клеток по ваю (y)
size_of_cell = 13  # размер квадратика
# константы для ClrSeg
number_of_groups = 20  # количество цветов/групп
# константы для Conway
conway_rules = 'B3/S23'  # после B идет перечисление необходимого кол-ва живых клеток рядом с текущей чтобы она родилась
# после S - чтобы выжила

# константы для червячка
global gc_stamina_level
global wall_count  # x из 10000

gc_stamina_level = 60
gc_burn_snake_after_dead = False
wall_count = 100
gc_diff_evolve = 1

import tkinter
from tkinter import *
from math import *
from random import *

from universe_class import *
from cell_class import *

# global lst_button
lst_button = 'r'

class main():
    def __init__(self, N=50, M=50, cellSize=5, numberOfGroups=10, mode='BakaFight', conwayRules='B3/S23'):
        self.root = tkinter.Tk()
        self.doShits = False
        self.frameDropping = 2
        self.root.title("Bakas BATTLE")
        self.mapFrame = Frame(self.root, width=N * cellSize, height=M * cellSize, bg='gray')
        self.universe = universe_abstract(N, M, sizeOfCell=cellSize, numberOfGroups=numberOfGroups, mode=mode,
                                          staminaLevel=gc_stamina_level, conwayRules=conwayRules)
        self.canvas = Canvas(self.mapFrame, width=N * cellSize, height=M * cellSize, bg='white')

        if mode == 'ClrSeg':
            self.lblTolerance = Label(self.root, text='Толерантность клетки:')
            self.sclTolerance = Scale(self.root, orient=HORIZONTAL, length=500, from_=0, to=450, tickinterval=50,
                                      resolution=1)
            self.sclTolerance.set(200)
            self.lblNeighbors = Label(self.root, text='Кол-во х-вых соседей:')
            self.sclNeighbors = Scale(self.root, orient=HORIZONTAL, length=200, from_=0, to=8, tickinterval=1,
                                      resolution=1)
            self.sclNeighbors.set(4)
            self.bStop = Button(self.root, text="Кончить", command=self.stop)
            self.bStart = Button(self.root, text="Начать", command=self.color_segregation)
        elif mode == 'Conway':
            self.lblFullness = Label(self.root, text='Плотность жизни:')
            self.sclFullness = Scale(self.root, orient=HORIZONTAL, length=500, from_=0, to=100, tickinterval=25,
                                     resolution=1)
            self.sclFullness.set(33)
            self.bSow = Button(self.root, text="Засеять", command=self.new_conway_field)
            self.bStart = Button(self.root, text="Начать", command=self.cycle_of_life)
            self.bStop = Button(self.root, text="Кончить", command=self.stop)
        elif mode == 'BakaFight':
            self.chbDE_alg = Checkbutton(self.root, text='Differential evolution',
                                                    var=gc_diff_evolve, command=self.togleDE)
            self.chbDE_alg.toggle()
            self.chbOnOff = Checkbutton(self.root, text='On/Off:', command=self.OnOff)
            self.chbOnOff.toggle()
            self.lblDE = Label(self.root, text='Diff Evolve: Gn = G1 + F x (G2 - G3)')
            self.lblTail_chance = Label(self.root, text='Tail chance:')
            self.lblMapFullness = Label(self.root, text='Walls:')
            self.lblAge = Label(self.root, text='Age: 0')
            self.lblGenNum = Label(self.root, text='Gen: 0')
            self.lblDE_F = Label(self.root, text='F:') # Ф - фокусы
            self.lblDE_CR = Label(self.root, text='CR:') # мутабельность
            self.lblDE_NP = Label(self.root, text='NP:') # Размер популяции
            self.lblDie_age = Label(self.root, text='Die age:') # Возраст смерти
            
            self.bDE_sow_gen = Button(self.root, text="Generation N", command=self.generate_new_gen)
            self.bDraw_brain = Button(self.root, text="Brain scheme", command=self.draw_brain_scheme)
            self.bSave_brains = Button(self.root, text="Save brains", command=self.save_brains)
            self.bLoad_brains = Button(self.root, text="Load brains", command=self.load_brains)
            
            self.sclTail_chance = Scale(self.root, orient=HORIZONTAL, length=100, from_=0, to=100, resolution=1, tickinterval=100)
            self.sclTail_chance.set(50)
            self.sclMapFullness = Scale(self.root, orient=HORIZONTAL, length=100, from_=0, to=50, resolution=1, tickinterval=50)
            self.sclMapFullness.set(10)
            self.sclDE_F = Scale(self.root, orient=HORIZONTAL, length=100, from_=0, to=2, resolution=0.01, tickinterval=2)
            self.sclDE_F.set(0.5)
            self.sclDE_CR = Scale(self.root, orient=HORIZONTAL, length=100, from_=0, to=1, resolution=0.05, tickinterval=1)
            self.sclDE_CR.set(0.9)
            self.sclDE_NP = Scale(self.root, orient=HORIZONTAL, length=100, from_=1, to=250, resolution=5, tickinterval=125)
            self.sclDE_NP.set(75)
            self.sclDie_age = Scale(self.root, orient=HORIZONTAL, length=100, from_=1, to=1000, resolution=5, tickinterval=1000)
            self.sclDie_age.set(300)

            self.valWormStamina = Label(self.root, text='')
            self.valWormLenght = Label(self.root, text='')


        self.mapFrame.grid(row=0, column=0, columnspan=10)
        self.canvas.grid(row=0, column=0, columnspan=10)

        if mode == 'BakaFight':

            self.chbDE_alg.grid(row=1, column=1, columnspan=3)
            self.bDraw_brain.grid(row=1, column=4, columnspan=1)
            #self.lblDE.grid(row=1, column=3, columnspan=4)
            self.lblTail_chance.grid(row=1, column=5, columnspan=1)
            self.sclTail_chance.grid(row=1, column=6, columnspan=1)

            self.lblMapFullness.grid(row=1, column=7, columnspan=1)
            self.sclMapFullness.grid(row=1, column=8, columnspan=1)

            self.chbOnOff.grid(row=1, column=9, columnspan=1)

            self.lblAge.grid(row=2, column=1, columnspan=1)
            self.lblGenNum.grid(row=2, column=2, columnspan=1)
            #self.lblDE_F.grid(row=2, column=3, columnspan=1)
            #self.sclDE_F.grid(row=2, column=4, columnspan=1)

            #self.lblDE_CR.grid(row=2, column=5, columnspan=1)
            #self.sclDE_CR.grid(row=2, column=6, columnspan=1)

            self.lblDE_NP.grid(row=2, column=5, columnspan=1)
            self.sclDE_NP.grid(row=2, column=6, columnspan=1)

            self.bDE_sow_gen.grid(row=2, column=9, columnspan=1)
            
            self.lblDie_age.grid(row=2, column=3, columnspan=1)
            self.sclDie_age.grid(row=2, column=4, columnspan=1)
            
            self.bLoad_brains.grid(row=2, column=7, columnspan=1)
            self.bSave_brains.grid(row=2, column=8, columnspan=1)

            self.baka_battle()

        elif mode == 'ClrSeg':
            self.lblTolerance.grid(row=1, column=1, columnspan=1)
            self.sclTolerance.grid(row=1, column=2, columnspan=4)
            self.lblNeighbors.grid(row=2, column=1, columnspan=1)
            self.sclNeighbors.grid(row=2, column=2, columnspan=2)
            self.bStart.grid(row=2, column=4, columnspan=1)
            self.bStop.grid(row=2, column=5, columnspan=1)
            self.draw_universe(self.universe)
            # self.color_segregation()
        elif mode == 'Conway':
            self.lblFullness.grid(row=1, column=1, columnspan=1)
            self.sclFullness.grid(row=1, column=2, columnspan=4)
            self.bSow.grid(row=2, column=2, columnspan=1)
            self.bStart.grid(row=2, column=4, columnspan=1)
            self.bStop.grid(row=2, column=5, columnspan=1)
            self.draw_universe(self.universe)
            # self.cycle_of_life()

        self.root.mainloop()

    def draw_universe(self, universe):
        cell_size = universe.get_cell_size()
        self.canvas.delete('all')
        bgr_color = self.universe.get_bgr_color()
        self.canvas.create_rectangle(0, 0, self.universe.N, self.universe.M, fill=bgr_color, outline=bgr_color)
        i = 0
        if self.universe.mode != 'BakaFight':  # coz til
            while i <= universe.N:
                j = 0
                while j <= universe.M:
                    color = universe.get_cell(i, j).get_colorName()
                    if color != bgr_color:
                        self.canvas.create_rectangle(i * cell_size + 2, j * cell_size + 2, (i + 1) * cell_size + 1,
                                                     (j + 1) * cell_size + 1,
                                                     fill=color, outline=color)
                    j += 1
                i += 1
        else:
            #agent_color = self.universe.get_agent_color()
            while i <= universe.N:
                j = 0
                while j <= universe.M:
                    cell = universe.get_cell(i, j)
                    color = cell.get_colorName()
                    if not cell.isAlive: #color != bgr_color and color != agent_color:
                        self.canvas.create_rectangle(i * cell_size + 2, j * cell_size + 2, (i + 1) * cell_size + 1,
                                                     (j + 1) * cell_size + 1,
                                                     fill=color, outline=color)
                    else:
                        if self.universe.isBakahead(cell): #color == agent_color:
                            extent = 240
                            azimut = 0
                            if self.universe.age % 10 > 4:
                                extent = 300
                                azimut = -30
                            azimut += (cell.get_azimuth() * 90 + 60)
                        else:
                            extent = 359
                            azimut = 1
                        self.canvas.create_arc(i * cell_size + 1, j * cell_size + 1, (i + 1) * cell_size + 2,
                                                       (j + 1) * cell_size + 2, start=azimut, extent=extent,
                                                       fill=color, outline=color)



                    j += 1
                i += 1
        self.canvas.update()

    def draw_brain_scheme(self):
        worm_brain = self.universe.get_baka_brain()
        worm_brain.draw_brain_scheme(root_win = self.root, width = 800, height = 600)

    def color_segregation(self):
        self.doShits = True
        refresh = 0
        while self.doShits:
            threshold = self.sclTolerance.get()
            neig_count = self.sclNeighbors.get()
            self.universe.step_ClrSeg(threshold, neig_count)
            if refresh % self.frameDropping == 0:
                self.draw_universe(self.universe)
            refresh += 1

    def worm_caretaker(self):
        self.doShits = True
        while self.doShits:
            self.draw_universe(self.universe)
            self.refresh_wormStat()
            self.doShits = self.universe.wormVSsansara()
            if not self.doShits:
                self.refresh_wormStat(final=True)
                isAllBurn = True
                while isAllBurn:
                    isAllBurn = not self.universe.fireShow()
                    self.draw_universe(self.universe)
                self.universe = universe_abstract(N=field_width, M=field_height, sizeOfCell=size_of_cell,
                                                  numberOfGroups=field_width * field_height)
                self.color_segregation()

    def baka_battle(self):
        self.doShits = True
        self.draw_universe(self.universe)
        while self.doShits:
            if gc_diff_evolve:
                self.doShits = self.universe.differential_evolution(chanceHaveTail = self.sclTail_chance.get(),
                                                                    mapFullness = self.sclMapFullness.get() * 100,
                                                                    F=self.sclDE_F.get(), CR = self.sclDE_CR.get(),
                                                                    NP = self.sclDE_NP.get())
            else:
                self.doShits = self.universe.baka_baka()
            self.lblAge['text'] = 'Age: ' + str(self.universe.age)
            self.lblGenNum['text'] = 'Gen: ' + str(self.universe.gen_number)
            self.draw_universe(self.universe)
            #self.root.after(100)

    def cycle_of_life(self):
        self.doShits = True
        refresh = 0
        while self.doShits:
            self.universe.step_Conway()
            if refresh % self.frameDropping == 0:
                self.draw_universe(self.universe)
            refresh += 1

    def new_conway_field(self):
        self.stop()
        fullness = self.sclFullness.get()
        old_universe = self.universe
        self.universe = universe_abstract(N=old_universe.N + 1, M=old_universe.M + 1,
                                          sizeOfCell=old_universe.cell_size, mode='Conway',
                                          mapFullness=fullness, conwayRules=conway_rules)
        self.draw_universe(self.universe)

    def refresh_game(self, N=50, M=50, cellSize=5, numberOfGroups=10, mode='ClrSeg', conwayRules='B3/S23'):
        self.__init__(N=N, M=M, cellSize=cellSize,
                      numberOfGroups=numberOfGroups, mode=mode, conwayRules=conwayRules)

    def refresh_wormStat(self, final=False):
        if final:
            self.lblWormStamina['text'] = 'Age:'
            self.lblWormLenght['text'] = 'IntegralLenght:'
            self.valWormStamina['text'] = str(self.universe.age)
            integral_lenght = 0
            for eaten_food in self.universe.eaten_food_counter:
                integral_lenght += eaten_food
            self.valWormLenght['text'] = str(integral_lenght)
        else:
            self.valWormStamina['text'] = str(self.universe.stamina)
            self.valWormLenght['text'] = str(len(self.universe.worm))
            self.valWormEatingFood1['text'] = str(self.universe.eaten_food_counter[0])
            self.valWormEatingFood2['text'] = str(self.universe.eaten_food_counter[1])
            self.valWormEatingFood3['text'] = str(self.universe.eaten_food_counter[2])

    def togleDE(self):
        global  gc_diff_evolve
        if gc_diff_evolve:
            self.universe.DE_learning = True
            gc_diff_evolve = 0
        else:
            self.universe.DE_learning = False
            gc_diff_evolve = 1

    def generate_new_gen(self):
        self.doShits = False
        self.universe.set_die_age(self.sclDie_age.get())
        self.universe.generate_new_generation(chanceHaveTail = self.sclTail_chance.get(),
                                                mapFullness = self.sclMapFullness.get() * 100,
                                                F=self.sclDE_F.get(), CR = self.sclDE_CR.get(),
                                                NP = self.sclDE_NP.get())
        self.baka_battle()

    def stop(self):
        self.doShits = False

    def OnOff(self):
        if self.doShits == True:
            self.doShits = False
        else:
            self.baka_battle()

    def save_brains(self):
        self.universe.save_all_brains_to_file()
        
    def load_brains(self):
        self.universe.load_brains_from_file()

# Погнале!
MainWin = main(N=field_width, M=field_height, cellSize=size_of_cell,
               numberOfGroups=number_of_groups, mode=game_mode, conwayRules=conway_rules)
