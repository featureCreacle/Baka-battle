import json
from random import *
from math import *

from cell_class import *
from brain_class import *



class universe_abstract():
    def __init__(self, N=40, M=40, mode='BakaFight',  sizeOfCell=5, chanceHaveTail = 50, lifeDensity=50,
                 mapFullness=1000, staminaLevel = 100,
                 numberOfGroups=10, conwayRules='B3/S23'):
        rand = Random()
        self.N = N - 1
        self.M = M - 1
        self.map = []
        self.cell_size = sizeOfCell
        self.color_list = []
        self.groups_count = numberOfGroups
        self.have_tail = True
        self.mode = mode
        if mode == 'ClrSeg':
            # Заполняем вектов цветов
            self.color_list.append(self.get_color())
            i = 1
            while (i < self.groups_count):
                self.color_list.append(self.get_random_color())
                i += 1
            # Заполняем поле клетками
            self.freeplace_count = 0
            self.freeplace = []
            i = 0
            while (i < N):
                j = 0
                row = []
                while (j < M):
                    groupNum = rand.randint(0, self.groups_count - 1)
                    if groupNum == 0:
                        self.freeplace_count += 1
                        self.freeplace.append((i, j))
                    clr = self.color_list[groupNum]
                    row.append(cell_abstact(self, (i, j), clr, groupNum))
                    j += 1
                self.map.append(row)
                i += 1
            if self.freeplace_count == 0:
                self.freeplace_count += 1
                self.freeplace.append((0, 0))
                cell00 = self.get_cell(0, 0)
                cell00.set_groupNum(0)
                cell00.set_color(self.color_list[0])
        elif mode == 'BakaFight':
            # Заполняем вектов цветов
            self.color_list.append(self.get_color(150, 150, 150))  # wall
            self.colorWallNum = 0
            self.color_list.append(self.get_color(255, 255, 255))  # background
            self.colorBgrNum = 1
            self.color_list.append(self.get_color(0, 150, 10))  # food_vegan
            self.colorVeganFoodNum = 2
            self.color_list.append(self.get_color(100, 0, 250))  # food_so-so
            self.colorMcDFoodNum = 3
            self.color_list.append(self.get_color(150, 0, 0))  # complex_meal
            self.colorMeatFoodNum = 4
            self.color_list.append(self.get_color(255, 200, 0))  # body (black) (no racist)
            self.colorBodyNum = 5
            self.color_list.append(self.get_color(250, 130, 50))  # head
            self.colorHeadNum = 6
            self.color_list.append(self.get_color(250, 40, 60))  # head tailless
            self.colorHeadNumTailless = 7
            self.groups_count = 8
            self.universe_on_fire = False
            self.staminaMax = staminaLevel
            self.baka_list = []
            self.worm = []
            self.wormhead = cell_abstact(self)
            self.wormhead_cord = (0, 0)
            self.baka_counter = 0
            self.baka_envNum = 0
            self.desire_cord = (0,0)
            self.deadworm_enviroments = []
            #Делаем стенки
            i = 0
            while (i < N):
                j = 0
                row = []
                while (j < M):
                    isWall = (randint(0, 10000) < mapFullness)
                    if isWall:
                        tmp_cell = cell_abstact(self, (i, j), color=self.color_list[self.colorWallNum],
                                                groupNumber=self.colorWallNum)
                    else:
                        tmp_cell = cell_abstact(self, (i, j), color=self.color_list[self.colorBgrNum],
                                                groupNumber=self.colorBgrNum)
                    row.append(tmp_cell)
                    j += 1
                self.map.append(row)
                i += 1

            i = 0
            while (i < N):
                j = 0
                while (j < M):
                    bornBakaBorn = False
                    if i % 3 == 2 and j % 3 == 2:
                        bornBakaBorn = (randint(0, 99) < lifeDensity)

                    if bornBakaBorn:
                        self.worm = []
                        self.baka_counter += 1
                        delta_x = randint(0, 2)
                        delta_y = randint(0, 2)
                        tmp_head = self.get_cell(i - delta_x, j - delta_y)

                        tailed = randint(0, 99) < chanceHaveTail
                        if tailed:
                            tmp_head.become_baka(self.baka_counter, self.colorHeadNum)
                            tail_preset_x = 0
                            tail_preset_y = 0
                            if randint(0, 1) == 1:
                                if delta_x == 0 or delta_x == 2:
                                    tail_preset_x = 1
                                else:
                                    tail_preset_x = 0 if randint(0, 1) == 1 else 2
                                tmp_cell = self.get_cell(i - tail_preset_x, j - delta_y)
                                baka_azimuth = 0 if tail_preset_x > delta_x else 2
                            else:
                                if delta_y == 0 or delta_y == 2:
                                    tail_preset_y = 1
                                else:
                                    tail_preset_y = 0 if randint(0, 1) == 1 else 2
                                tmp_cell = self.get_cell(i - delta_x, j - tail_preset_y)
                                baka_azimuth = 1 if tail_preset_y < delta_y else 3
                            tmp_head.set_azimuth(baka_azimuth)
                            tmp_cell.become_baka(self.baka_counter, self.colorBodyNum)
                            self.worm.append(tmp_cell)
                            self.set_wormhead(tmp_head)
                        else:
                            tmp_head.become_baka(self.baka_counter, self.colorHeadNumTailless)
                            self.set_wormhead(tmp_head)

                        self.desire_cord = tmp_head.get_cord()
                        self.have_tail = tailed
                        self.watch_first = not tailed
                        self.uroboros_level = -1
                        self.SmartStepCounter = 0
                        self.SmartStep = False
                        self.satiety = 0
                        self.stamina = self.staminaMax
                        self.worm_alive = True
                        self.age = 0
                        self.eaten_food_counter = [0] * 5
                        self.baka_brain = brain_abstract()
                        self.lasts_brainOut = [[1,1], [1,1], [1,1]]
                        self.saveBakaEnviroment()
                    j += 1
                i += 1

            self.food_list = []
            self.food_generate()
            self.baka_envNum = self.baka_counter
            self.DE_learning = True
            self.F = 0.5
            self.CR = 0.9
            self.gen_number = 0
            self.die_age = 300

        elif mode == 'Conway':
            # Заполняем вектов цветов
            self.color_list.append(self.get_color(255, 255, 255))  # Dead
            self.colorDeadNum = 0
            self.color_list.append(self.get_color())  # Alive
            self.colorAliveNum = 1
            self.groups_count = 2

            ruleList = conwayRules.split('/', 1)

            self.bornRule = ruleList[0][1:]
            self.survRule = ruleList[1][1:]

            self.changing_cells = []
            self.changing_cells_count = 0

            self.changed_cells = []
            self.changed_cells_count = 0

            i = 0
            while (i < N):
                j = 0
                row = []
                while (j < M):
                    dice = randint(0, 99)
                    if dice > mapFullness:
                        tmp_cell = cell_abstact(self, (i, j),
                                                color=self.color_list[self.colorDeadNum],
                                                groupNumber=self.colorDeadNum)
                        row.append(tmp_cell)
                    else:
                        tmp_cell = cell_abstact(self, (i, j),
                                                color=self.color_list[self.colorAliveNum],
                                                groupNumber=self.colorAliveNum)
                        row.append(tmp_cell)
                        self.changed_cells.append(tmp_cell)
                        self.changed_cells_count += 1
                    j += 1
                self.map.append(row)
                i += 1
        else:
            pass

    def saveBakaEnviroment(self, envNum = 1, isNew = True):
        tmpEnv = { 'worm': self.worm,
                   'wormhead': self.wormhead,
                   'wormhead_cord': self.wormhead_cord,
                   'have_tail': self.have_tail,
                   'watch_first': self.watch_first,
                   'uroboros_level': self.uroboros_level,
                   'SmartStepCounter': self.SmartStepCounter,
                   'SmartStep': self.SmartStep,
                   'satiety': self.satiety,
                   'stamina': self.stamina,
                   'worm_alive': self.worm_alive,
                   'age': self.age,
                   'desire_cord': self.desire_cord,
                   'eaten_food_counter':self.eaten_food_counter,
                   'baka_brain':self.baka_brain,
                   'lasts_brainOut':self.lasts_brainOut
                   }
        if isNew:
            self.baka_list.append(tmpEnv)
        else:
            self.baka_list[envNum-1].update(tmpEnv)

    def updateBakaEnvitoment(self, envNum, envDict):
        self.baka_list[envNum-1].update(envDict)

    def getBakaEnviroment(self,envNum):
        return self.baka_list[envNum-1]

    def setBakaEnviroment(self, envNum = 1):
        tmpEnv = self.baka_list[envNum-1]
        self.worm = tmpEnv['worm']
        self.wormhead = tmpEnv['wormhead']
        self.wormhead_cord = tmpEnv['wormhead_cord']
        self.have_tail = tmpEnv['have_tail']
        self.watch_first = tmpEnv['watch_first']
        self.uroboros_level = tmpEnv['uroboros_level']
        self.SmartStepCounter = tmpEnv['SmartStepCounter']
        self.SmartStep = tmpEnv['SmartStep']
        self.satiety = tmpEnv['satiety']
        self.stamina = tmpEnv['stamina']
        self.worm_alive = tmpEnv['worm_alive']
        self.age = tmpEnv['age']
        self.desire_cord = tmpEnv['desire_cord']
        self.eaten_food_counter = tmpEnv['eaten_food_counter']
        self.baka_brain = tmpEnv['baka_brain']
        self.lasts_brainOut = tmpEnv['lasts_brainOut']
        self.baka_envNum = envNum

    def changeBakaEnviroment(self, envNum):
        self.saveBakaEnviroment(self.baka_envNum, isNew=False)
        self.setBakaEnviroment(envNum )

    def clearAllBakaEnviroment(self):
        self.baka_list.clear()
        self.baka_counter = 0
        self.baka_envNum = -1

    def step_ClrSeg(self, threshold=100, count=4):
        i = 0
        while (i <= self.N):
            j = 0
            while (j <= self.M):
                cord = self.get_random_cord()
                cell = self.get_cell(cord[0], cord[1])
                if cell.get_groupNum() == 0:
                    j += 1
                    continue
                if cell.decision_to_move(cell.quality_of_neighbors_by_color(), threshold, count):
                    self.move_cell_to_random_freeplace(cell)
                j += 1
            i += 1

    def step_Worm(self, cord=(0,0), justWatch=False, sphere = True):
        global last_button
        headCell = self.get_wormhead()
        headCellCord = self.get_wormhead_cord()
        newHeadCord = cord

        if sphere:
            if newHeadCord[0] > self.N:
                newHeadCord = (0, newHeadCord[1])
            elif newHeadCord[1] > self.M:
                newHeadCord = (newHeadCord[0], 0)
            elif newHeadCord[0] < 0:
                newHeadCord = (self.N, newHeadCord[1])
            elif newHeadCord[1] < 0:
                newHeadCord = (newHeadCord[0], self.M)
        else:
            if newHeadCord[0] > self.N or newHeadCord[1] > self.M:
                return False
            if newHeadCord[0] < 0 or newHeadCord[1] < 0:
                return False

        eaten_cell = self.get_cell(newHeadCord[0], newHeadCord[1])
        isAliveBaka = eaten_cell.isAlive
        eaten_cell_baka_num = eaten_cell.get_bakaNum()
        baka_num = self.baka_envNum
        if eaten_cell.color_is_num(self.colorBgrNum):
            if justWatch:
                self.desire_cord = newHeadCord
                return True
            if self.have_tail:
                eaten_cell.become_baka(baka_num, self.colorBodyNum)
                self.turn_Worm(headCell, headCellCord, newHeadCord)
            else:
                eaten_cell.kill()
                eaten_cell.become_alien(self.colorBgrNum)

            headCell.swap_to_cord(newHeadCord)
            self.set_wormhead_by_cord(newHeadCord)
            exTail = []
            if self.satiety == 0:
                exTail.append(self.worm[0])
                self.worm = self.worm[1:]
            elif self.satiety > 0:
                self.satiety -= 1
            else:
                exTail.append(self.worm[0])
                if len(self.worm) == 2:
                    self.worm_alive = False
                    self.deadworm_enviroments.append(baka_num)
                    self.worm[1].kill()
                    self.worm = self.worm[1:]
                else:
                    exTail.append(self.worm[1])
                    self.worm = self.worm[2:]
                self.satiety += 1
            if self.have_tail:
                for tail_part in exTail:
                    if self.worm.count(tail_part) == 0:
                        if tail_part.get_bakaNum() == baka_num:
                            tail_part.kill()
                            tail_part.become_alien(self.colorBgrNum)
            self.uroboros_level = -1
            return True

        elif eaten_cell.color_is_num(self.colorWallNum):
            return False

        elif eaten_cell.color_is_num(self.colorBodyNum):
            if justWatch:
                self.desire_cord = newHeadCord
                return True
            else:
                if baka_num != eaten_cell_baka_num or not isAliveBaka:

                    self.uroboros_level = -1
                    self.stamina = self.staminaMax
                    self.satiety += 1
                    #self.eaten_food_counter[3] += 1

                    if self.have_tail:
                        eaten_cell.become_baka(baka_num, self.colorBodyNum)
                        self.turn_Worm(headCell, headCellCord, newHeadCord)
                    else:
                        eaten_cell.kill()
                        eaten_cell.become_alien(self.colorBgrNum)

                    if isAliveBaka:
                        baka_env = self.getBakaEnviroment(eaten_cell_baka_num)

                        baka_env['uroboros_level'] = -1
                        enemy_worm = baka_env['worm']
                        cl_count = enemy_worm.count(eaten_cell)
                        if cl_count > 1:
                            reverse_enemy_worm = enemy_worm.copy()
                            reverse_enemy_worm.reverse()
                            revers_bite_place = reverse_enemy_worm.index(eaten_cell)
                            bite_place =len(enemy_worm) - (revers_bite_place + 1)
                            #reverse_enemy_worm = 0
                        elif cl_count == 1:
                            bite_place = enemy_worm.index(eaten_cell)
                        else:
                            bite_place = 0
                        new_enemy_worm = enemy_worm[bite_place+1:]
                        if bite_place > 0:
                            bited_part = enemy_worm[:bite_place]
                            for peace in bited_part:
                                if peace.get_bakaNum() == eaten_cell_baka_num\
                                    and not self.isBakahead(peace):
                                    peace.kill()
                        enemy_worm = 0
                        baka_env['worm'] = new_enemy_worm
                        self.updateBakaEnvitoment(eaten_cell_baka_num, baka_env)

                    headCell.swap_to_cord(newHeadCord)
                    self.set_wormhead_by_cord(newHeadCord)
                    return True
                else:
                    if self.have_tail:
                        eaten_cell.become_baka(baka_num, self.colorBodyNum)
                        self.turn_Worm(headCell, headCellCord, newHeadCord)
                    else:
                        a = 1
                    headCell.swap_to_cord(newHeadCord)
                    self.set_wormhead_by_cord(newHeadCord)
                    if self.worm.count(self.worm[0]) == 1:
                        self.worm[0].become_alien(self.colorBgrNum)
                        self.worm[0].kill()
                    self.worm.pop(0)
                    return True
                    #if self.uroboros_level < -1:
                     #   eaten_cord = eaten_cell.get_cord()
                     #   neck_cord = self.worm[self.uroboros_level - 1].get_cord()
                     #   if eaten_cord[0] == neck_cord[0] and eaten_cord[1] == neck_cord[1]:
                     #       return self.step_Uroboros(eaten_cell, baka_num)
                     #   else:
                     #       eaten_cord = eaten_cell.get_cord()
                     #       neck_cord = self.worm[-2].get_cord()
                     #       if eaten_cord[0] == neck_cord[0] and eaten_cord[1] == neck_cord[1]:
                     #           self.uroboros_level = -1
                     #           return self.step_Uroboros(eaten_cell, baka_num)
                     #       else:
                     #           return False
                    #elif self.uroboros_level == -1:
                     #   eaten_cord = eaten_cell.get_cord()
                     #   neck_cord = self.worm[self.uroboros_level - 1].get_cord()
                     #   if eaten_cord[0] == neck_cord[0] and eaten_cord[1] == neck_cord[1]:
                     #       return self.step_Uroboros(eaten_cell, baka_num)
                     #   else:
                     #       return False

        elif self.isFood(eaten_cell):
            if  justWatch:
                self.desire_cord = newHeadCord
                return True
            self.uroboros_level = -1
            self.stamina = self.staminaMax
            food_type = self.food_list.index(eaten_cell)
            self.satiety += food_type
            self.eaten_food_counter[food_type] += 1

            if self.have_tail:
                eaten_cell.become_baka(baka_num, self.colorBodyNum)
                self.turn_Worm(headCell, headCellCord, newHeadCord)
            else:
                eaten_cell.kill()
                eaten_cell.become_alien(self.colorBgrNum)
            self.set_wormhead_by_cord(newHeadCord)
            headCell.swap_to_cord(newHeadCord)
            self.food_generate(food_type)
            return True

        elif self.isBakahead(eaten_cell):

            if baka_num != eaten_cell_baka_num:

                if justWatch:
                    self.desire_cord = newHeadCord
                    return True
                self.uroboros_level = -1
                self.stamina = self.staminaMax
                self.satiety += 2
                self.eaten_food_counter[4] += 1
                if self.have_tail:
                    eaten_cell.become_baka(baka_num,self.colorBodyNum)
                    self.turn_Worm(headCell, headCellCord, newHeadCord)
                else:
                    eaten_cell.kill()
                    eaten_cell.become_alien(self.colorBgrNum)
                self.set_wormhead_by_cord(newHeadCord)
                baka_env = self.getBakaEnviroment(eaten_cell_baka_num)
                if baka_env['worm_alive'] == True:
                    baka_env['worm_alive'] = False
                    self.deadworm_enviroments.append(eaten_cell_baka_num)
                    if baka_env['have_tail']:
                        enemy_worm = baka_env['worm']
                        for peace in enemy_worm:
                            if peace.get_bakaNum() == eaten_cell_baka_num:
                                peace.kill()
                            else:
                                a = 1
                        baka_env['worm'] = enemy_worm[:-1]
                    self.updateBakaEnvitoment(eaten_cell_baka_num,baka_env)

                headCell.swap_to_cord(newHeadCord)
                return True
            else:
                False

        else:
            return False

    def turn_Worm(self, wormhead, wormhead_cord, desire_cord):
        if wormhead_cord[0] > desire_cord[0]:
            wormhead.set_azimuth(2)
        elif wormhead_cord[1] > desire_cord[1]:
            wormhead.set_azimuth(1)
        elif wormhead_cord[0] < desire_cord[0]:
            wormhead.set_azimuth(0)
        elif wormhead_cord[1] < desire_cord[1]:
            wormhead.set_azimuth(3)
        return True

    def turnOrStep(self, wormhead, desire_cord, justWatch=False):
        wormhead_cord = wormhead.get_cord()
        wormhead_azimuth = wormhead.get_azimuth()

        if wormhead_azimuth == 0:
            if wormhead_cord[0] < desire_cord[0]:
                return self.step_Worm(cord=desire_cord)
            else:
                return self.turn_Worm(wormhead, wormhead_cord, desire_cord)

        elif wormhead_azimuth == 1:
            if wormhead_cord[1] > desire_cord[1]:
                return self.step_Worm(cord=desire_cord)
            else:
                return self.turn_Worm(wormhead, wormhead_cord, desire_cord)

        elif wormhead_azimuth == 2:
            if wormhead_cord[0] > desire_cord[0]:
                return self.step_Worm(cord=desire_cord)
            else:
                return self.turn_Worm(wormhead, wormhead_cord, desire_cord)

        elif wormhead_azimuth == 3:
            if wormhead_cord[1] < desire_cord[1]:
                return self.step_Worm(cord=desire_cord)
            else:
                return self.turn_Worm(wormhead, wormhead_cord, desire_cord)

    def step_Uroboros(self, eaten_cell, bakaNum = 0):
        wh_cord = self.get_wormhead_cord()
        eaten_cell.swap_to_cord(wh_cord)
        self.set_wormhead(eaten_cell)
        if self.have_tail:
            self.turn_Worm(eaten_cell, wh_cord, eaten_cell.get_cord())
        exTail = []
        if self.satiety == 0:
            exTail.append(self.worm[0])
            self.worm = self.worm[1:]
        elif self.satiety > 0:
            self.satiety -= 1
        else:
            exTail.append(self.worm[0])
            if len(self.worm) == 2:
                self.worm_alive = False
                self.deadworm_enviroments.append(bakaNum)
                self.worm[1].kill()
                self.worm = self.worm[1:]
            else:
                exTail.append(self.worm[1])
                self.worm = self.worm[2:]
            self.satiety += 1
        if self.have_tail:
            for tail_part in exTail:
                if self.worm.count(tail_part) == 0:
                    tail_part.kill()
                    tail_part.become_alien(self.colorBgrNum)

        self.uroboros_level -= 2
        if abs(self.uroboros_level) >= len(self.worm):
            self.uroboros_level = -1
        return True

    def step_Conway(self):
        self.changing_cells = list(set(self.check_changes_near_every_changed_cell()))
        self.changing_cells_count = len(self.changing_cells)
        i = 0
        while i < self.changing_cells_count:
            cell_for_cahnge = self.changing_cells[i]
            cell_alive = cell_for_cahnge.checkIsAlive(mode)
            if cell_alive:
                cell_for_cahnge.become_alien(self.colorDeadNum)
            else:
                cell_for_cahnge.become_alien(self.colorAliveNum)
            i += 1
        self.changed_cells = self.changing_cells
        self.changed_cells_count = self.changing_cells_count
        self.changing_cells = []
        self.changing_cells_count = 0

    def food_generate(self, food_type=-1):
        if food_type < 0:
            food_type = 0
            self.food_list = []
            while food_type != 3:
                self.generate_food_by_type(food_type)
                food_type += 1
        else:
            self.generate_food_by_type(food_type)

    def generate_food_by_type(self, food_type):
        foodx = randint(0, self.N)
        foody = randint(0, self.M)
        cell = self.get_cell(foodx, foody)
        while (cell.get_groupNum() != self.colorBgrNum):
            foodx = randint(0, self.N)
            foody = randint(0, self.M)
            cell = self.get_cell(foodx, foody)
        cell.become_alien(self.colorVeganFoodNum + food_type)
        self.set_foodcell(cell, food_type)

    def isFood(self, food_candidat):
        if self.food_list.count(food_candidat) >= 1:
            return True
        return False

    def isBakahead(self, cell):
        cell_type = cell.get_groupNum()
        if cell_type == self.colorHeadNum or cell_type == self.colorHeadNumTailless:
            return True
        return False
        
    def choose_one_food(self):
        allFood_cord = self.get_all_foodcell_cord()
        wormHdCrd = self.get_wormhead_cord()
        solution_list = []
        food_type = 0
        for foodCrd in allFood_cord:
            food_type += 1
            delta_x = wormHdCrd[0] - foodCrd[0]
            dist_to_food_x = (abs(delta_x), -1 if delta_x < 0 else 1)
            delta_y = wormHdCrd[1] - foodCrd[1]
            dist_to_food_y = (abs(delta_y), -1 if delta_y < 0 else 1)
            max_len = sqrt(self.N ** 2 + self.M ** 2)
            dist_len = sqrt(delta_x ** 2 + delta_y ** 2)
            food_atract = ((max_len - dist_len) / max_len) + (0.09 * food_type)
            solution_list.append((dist_to_food_x, dist_to_food_y, foodCrd, food_atract))

        max_atract = solution_list[0][3]
        pos = 0
        i = len(solution_list)

        while i != 0:
            i -= 1
            if solution_list[i][3] > max_atract:
                pos = i
                max_atract = solution_list[i][3]

        return solution_list[pos]

    def wormVSsansara(self):
        if not self.worm_alive:
            return True
        self.age += 1
        self.stamina -= 1
        if self.stamina <= 0:
            self.stamina = self.staminaMax
            self.satiety -= 1

        WHcord = self.get_wormhead().get_cord()
        in_position = self.desire_cord[0] == WHcord[0] and self.desire_cord[1] == WHcord[1]
        if not self.have_tail and not in_position:
            return self.step_Worm(self.desire_cord)

        dist_to_food = self.choose_one_food()

        dist_to_food_x = dist_to_food[0]
        dist_to_food_y = dist_to_food[1]
        food_cord = dist_to_food[2]

        if self.SmartStepCounter > 0:
            sucTry = self.trySmartStep(dist_to_food_x, dist_to_food_y, food_cord, justWatch=self.watch_first)
        else:
            dice = randint(0, 1)
            if dice == 0:
                sucTry = self.tryStepToFoodX(dist_to_food_x, food_cord, justWatch=self.watch_first)
                if not sucTry:
                    sucTry = self.tryStepToFoodY(dist_to_food_y, food_cord, justWatch=self.watch_first)
            else:
                sucTry = self.tryStepToFoodY(dist_to_food_y, food_cord, justWatch=self.watch_first)
                if not sucTry:
                    sucTry = self.tryStepToFoodX(dist_to_food_x, food_cord, justWatch=self.watch_first)

            if not sucTry:
                self.SmartStep = True
                sucTry = self.trySmartStep(dist_to_food_x, dist_to_food_y, food_cord, justWatch=self.watch_first)

        if self.watch_first:
            return self.turnOrStep(self.get_wormhead(), self.desire_cord)
        else:
            return sucTry

    def tryStepToFoodX(self, dist_to_dest, target_cord, justWatch=False):
        dest = dist_to_dest[0] - 1
        if dest == -1:
            return False
        sign = dist_to_dest[1]
        food_cord = target_cord
        head_cord = self.get_wormhead_cord()
        new_headcord = (food_cord[0] + (dest * sign), head_cord[1])
        succ = self.step_Worm(new_headcord, justWatch=justWatch)
        if succ:
            self.learn_baka_brain(new_headcord)
        return succ

    def tryStepToFoodY(self, dist_to_dest, target_cord, justWatch=False):
        dest = dist_to_dest[0] - 1
        if dest == -1:
            return False
        sign = dist_to_dest[1]
        food_cord = target_cord
        head_cord = self.get_wormhead_cord()
        new_headcord = (head_cord[0], food_cord[1] + (dest * sign))
        succ = self.step_Worm(new_headcord, justWatch=justWatch)
        if succ:
            self.learn_baka_brain(new_headcord)
        return  succ

    def trySmartStep(self, dist_to_food_x, dist_to_food_y, target_cord, justWatch=False):
        if self.SmartStep == True:
            self.SmartStepCounter = 6
            self.SmartStep = False
        self.SmartStepCounter -= 1

        # doSteps = True
        destX = dist_to_food_x[0] + 1
        if destX == 1:
            dice = randint(0, 1)
            signX = -1 if dice == 0 else 1
        else:
            signX = dist_to_food_x[1]
        destY = dist_to_food_y[0] + 1
        if destY == 1:
            dice = randint(0, 1)
            signY = -1 if dice == 0 else 1
        else:
            signY = dist_to_food_y[1]
        head_cord = self.get_wormhead_cord()
        food_cord = target_cord
        WatWay = randint(0, 1)
        new_cord = []
        new_cord.append((food_cord[0] + (destX * signX), head_cord[1]))

        if new_cord[0][0] > self.N:
            new_cord[0] = (self.N, new_cord[0][1])
        elif new_cord[0][0] < 0:
            new_cord[0] = (0, new_cord[0][1])

        new_cord.append((head_cord[0], food_cord[1] + (destY * signY)))

        if new_cord[1][1] > self.M:
            new_cord[1] = (new_cord[1][0], self.M)
        elif new_cord[1][1] < 0:
            new_cord[1] = (new_cord[1][0], 0)

        if WatWay == 0:
            stepSuc = self.step_Worm(new_cord[0], justWatch=justWatch)
            if not stepSuc:
                stepSuc = self.step_Worm(new_cord[1], justWatch=justWatch)
        else:
            stepSuc = self.step_Worm(new_cord[1], justWatch=justWatch)
            if not stepSuc:
                stepSuc = self.step_Worm(new_cord[0], justWatch=justWatch)

        if not stepSuc:
            self.SmartStepCounter = 0  # сдались нахер так умно ходить
            return True
        else:
            return stepSuc

    def baka_baka(self):
        i = 1
        while i <= self.baka_counter:
            if i not in self.deadworm_enviroments:
                self.changeBakaEnviroment(i)
                self.wormVSsansara()
            i += 1
        return True

    def differential_evolution(self, F = 0.5, CR = 0.9, NP = 50, chanceHaveTail = 50, mapFullness = 1000):
        worms_move = False
        i = 1
        while i <= self.baka_counter:
            if i not in self.deadworm_enviroments:
                self.changeBakaEnviroment(i)
                if not self.worm_alive:
                    return True
                self.age+=1
                self.stamina -= 1
                if self.stamina <= 0:
                    self.stamina = self.staminaMax
                    self.satiety -= 1
                enviroment = self.see_around()
                decision  = self.baka_brain.guess(enviroment)
                succ = False
                #if decision[0] == self.lasts_brainOut[-2] and \
                #        self.lasts_brainOut[-1] == self.lasts_brainOut[-3] and \
                #        not self.lasts_brainOut[-1] == self.lasts_brainOut[-2]:
                #    pass
                #else:
                cord = self.thought_to_action(decision)
                succ = self.move_body(cord)

                bakeuper1 = self.get_last_step(-3)
                bakeuper2 = self.get_last_step(-1)
                if bakeuper1.__eq__(bakeuper2):
                    a = 1
                if succ:
                    worms_move = succ
                    self.memorize_step(decision[0])
                else:
                    new_decision = decision
                    ch_cord = randint(0,1)
                    new_decision[0][ch_cord] = 0 if new_decision[0][ch_cord] == 1 else 1
                    cord = self.thought_to_action(new_decision[0])
                    #bakeuper = self.get_last_step(-2)
                    while self.get_cell(cord[0],cord[1]).get_groupNum == 0:# or bakeuper.__eq__(new_decision[0]):
                        ch_cord = randint(0, 1)
                        new_decision[0][ch_cord] = 0 if new_decision[0][ch_cord] == 1 else 1
                        cord = self.thought_to_action(new_decision[0])
                    #self.desire_cord = cord
                    self.baka_brain.learn(input= enviroment, output= new_decision, maxSteps=10)
                    #check_decision = self.baka_brain.guess(enviroment)
                    #self.memorize_step(check_decision[0])
            i += 1

        if len(self.deadworm_enviroments) == (self.baka_counter-1) or self.age > self.die_age:
                #or not worms_move \
            self.generate_new_generation(chanceHaveTail = chanceHaveTail, mapFullness = mapFullness,
                                                            F = F, CR = CR, NP = NP, fromBests = True)
        return  True

    def move_body(self, cord = (0,0)):
        if self.have_tail:
            succ = self.step_Worm(cord=cord)
        else:
            succ = self.step_Worm(cord, justWatch=True)
            if succ:
                succ = self.turnOrStep(self.get_wormhead(), cord)
            #WHcord = self.get_wormhead_cord()
            #in_position = self.desire_cord[0] == WHcord[0] and self.desire_cord[1] == WHcord[1]
            #if in_position:
            #    succ = self.turnOrStep(self.get_wormhead(), cord)
            #else:
            #    succ = self.step_Worm(self.desire_cord, justWatch=False)
        return  succ

    def thought_to_action(self, decision):
        wormhead_cord = self.get_wormhead_cord()
        cord = (wormhead_cord[0], wormhead_cord[1])

        #if decision[0] == [0, 1, 1] or decision[0] == [1, 0, 0]:  # лево
        #    cord = (wormhead_cord[0] + 1, wormhead_cord[1])
        #elif decision[0] == [1, 1, 0] or decision[0] == [0, 0, 1]:  # право
        #    cord = (wormhead_cord[0] - 1, wormhead_cord[1])
        #elif decision[0] == [1, 0, 1] or decision[0] == [1, 1, 1]:  # вверх
        #    cord = (wormhead_cord[0], wormhead_cord[1] - 1)
        #elif decision[0] == [0, 1, 0] or decision[0] == [0, 0, 0]:  # вниз
        #    cord = (wormhead_cord[0], wormhead_cord[1] + 1)
        if decision[0] == [0, 1]:  # лево
            cord = (wormhead_cord[0] + 1, wormhead_cord[1])
        elif decision[0] == [1, 0]:  # право
            cord = (wormhead_cord[0] - 1, wormhead_cord[1])
        elif decision[0] == [1, 1]:  # вверх
            cord = (wormhead_cord[0], wormhead_cord[1] - 1)
        elif decision[0] == [0, 0]:  # вниз
            cord = (wormhead_cord[0], wormhead_cord[1] + 1)

        return  cord

    def cord_to_thought(self, cord = (0,0)):
        wormhead_cord = self.get_wormhead_cord()
        decision = []

        if cord == (wormhead_cord[0] + 1, wormhead_cord[1]):
            decision.append([0, 1])
        elif  cord == (wormhead_cord[0] - 1, wormhead_cord[1]):
            decision.append([1, 0]) # право
        elif cord == (wormhead_cord[0], wormhead_cord[1] - 1):
            decision.append([1, 1]) # вверх
        elif cord == (wormhead_cord[0], wormhead_cord[1] + 1):
            decision.append([0, 0]) # вниз
        return  decision

    def generate_new_generation(self, chanceHaveTail = 50, mapFullness = 1000, F = 0.5, CR = 0.9, NP = 50, fromBests = False):
        self.F = F
        self.CR = CR
        self.gen_number+=1
        lifeDensity = round(NP*100 / ((self.N * self.M) / 9))
        tailed_bastards = self.get_best_tailed_bastards(bastardsCount = 5, aliveOnly=False)
        tailless_bastards = self.get_best_tailless_bastards(bastardsCount = 5, aliveOnly=False)

        #переписать потом, унести в функцию с генерацие рандомных возмущений в весах, если мозгов меньше чем надо.
        if fromBests:
            #tailed_bastards = tailed_bastards[0:round(len(tailed_bastards))]
            while len(tailed_bastards)<3:
                tailed_bastards.append(tailed_bastards[0])
            #tailless_bastards = tailless_bastards[0:round(len(tailless_bastards))]
            while len(tailless_bastards)<3:
                tailless_bastards.append(tailless_bastards[0])
        #конец

        self.generate_map(chanceHaveTail = chanceHaveTail, mapFullness = mapFullness, lifeDensity = lifeDensity,
                          tailed_brains = tailed_bastards, tailless_brains = tailless_bastards)
        self.food_generate()

    def generate_map(self, chanceHaveTail = 50, mapFullness = 1000, lifeDensity = 50, tailed_brains = [], tailless_brains = []):
        map = []
        self.universe_on_fire = False
        self.baka_list = []
        self.worm = []
        self.wormhead = cell_abstact(self)
        self.wormhead_cord = (0, 0)
        self.baka_counter = 0
        self.baka_envNum = 0
        self.desire_cord = (0, 0)
        self.deadworm_enviroments = []
        N = self.N + 1
        M = self.M + 1
        # Делаем стенки
        i = 0
        while (i < N):
            j = 0
            row = []
            while (j < M):
                isWall = (randint(0, 10000) < mapFullness)
                if isWall:
                    tmp_cell = cell_abstact(self, (i, j), color=self.color_list[self.colorWallNum],
                                            groupNumber=self.colorWallNum)
                else:
                    tmp_cell = cell_abstact(self, (i, j), color=self.color_list[self.colorBgrNum],
                                            groupNumber=self.colorBgrNum)
                row.append(tmp_cell)
                j += 1
            map.append(row)
            i += 1

        i = 0
        while (i < N):
            j = 0
            while (j < M):
                bornBakaBorn = False
                if i % 3 == 2 and j % 3 == 2:
                    bornBakaBorn = (randint(0, 99) < lifeDensity)

                if bornBakaBorn:
                    self.worm = []
                    self.baka_counter += 1
                    delta_x = randint(0, 2)
                    delta_y = randint(0, 2)
                    tmp_head = map[i - delta_x][j - delta_y]

                    tailed = randint(0, 99) < chanceHaveTail
                    if tailed:
                        tmp_head.become_baka(self.baka_counter, self.colorHeadNum)
                        tail_preset_x = 0
                        tail_preset_y = 0
                        if randint(0, 1) == 1:
                            if delta_x == 0 or delta_x == 2:
                                tail_preset_x = 1
                            else:
                                tail_preset_x = 0 if randint(0, 1) == 1 else 2
                            tmp_cell = map[i - tail_preset_x][j - delta_y]
                            baka_azimuth = 0 if tail_preset_x > delta_x else 2
                        else:
                            if delta_y == 0 or delta_y == 2:
                                tail_preset_y = 1
                            else:
                                tail_preset_y = 0 if randint(0, 1) == 1 else 2
                            tmp_cell = map[i - delta_x][j - tail_preset_y]
                            baka_azimuth = 1 if tail_preset_y < delta_y else 3
                        tmp_head.set_azimuth(baka_azimuth)
                        tmp_cell.become_baka(self.baka_counter, self.colorBodyNum)
                        self.worm.append(tmp_cell)
                        self.set_wormhead(tmp_head)
                    else:
                        tmp_head.become_baka(self.baka_counter, self.colorHeadNumTailless)
                        self.set_wormhead(tmp_head)

                    self.desire_cord = tmp_head.get_cord()
                    self.have_tail = tailed
                    self.watch_first = not tailed
                    self.uroboros_level = -1
                    self.SmartStepCounter = 0
                    self.SmartStep = False
                    self.satiety = 0
                    self.stamina = self.staminaMax
                    self.worm_alive = True
                    self.age = 0
                    self.eaten_food_counter = [0] * 5
                    if tailed:
                        brains_count = len(tailed_brains)
                    else:
                        brains_count = len(tailless_brains)
                    brainNum1 = randint(0, brains_count - 1)
                    brainNum2 = randint(0, brains_count - 1)
                    brainNum3 = randint(0, brains_count - 1)
                    if tailed:
                        self.baka_brain = self.cross_brain(tailed_brains[brainNum1][1],
                                                           tailed_brains[brainNum3][1],
                                                           tailed_brains[brainNum2][1])
                    else:
                        self.baka_brain = self.cross_brain(tailless_brains[brainNum1][1],
                                                           tailless_brains[brainNum3][1],
                                                           tailless_brains[brainNum2][1])
                    self.lasts_brainOut = [[1,1], [1,1], [1,1]]
                    self.saveBakaEnviroment()
                j += 1
            i += 1
        self.food_list = []
        self.food_generate()
        self.baka_envNum = self.baka_counter
        self.map = map

    def get_best_tailed_bastards(self, bastardsCount = -1, aliveOnly = True):
        bests_bakas = []
        for baka in self.baka_list:
            if baka['have_tail']:
                if aliveOnly and baka['worm_alive'] == True:
                    baka_food_counter = baka['eaten_food_counter']
                    food_coeff = baka_food_counter[0]+baka_food_counter[1]+baka_food_counter[2]+\
                                 baka_food_counter[3]*2+baka_food_counter[4]*25
                    bests_bakas.append((food_coeff, baka['baka_brain']))
                elif not aliveOnly:
                    baka_food_counter = baka['eaten_food_counter']
                    food_coeff = baka_food_counter[0] + baka_food_counter[1] + baka_food_counter[2] + \
                                 baka_food_counter[3] * 2 + baka_food_counter[4] * 25
                    bests_bakas.append((food_coeff, baka['baka_brain']))
        bests_bakas.sort()

        if bastardsCount <= len(bests_bakas):
            return bests_bakas[0:bastardsCount]
        else:
            return bests_bakas

    def get_best_tailless_bastards(self, bastardsCount = -1, aliveOnly = True):
        bests_bakas = []
        for baka in self.baka_list:
            if not baka['have_tail']:
                if aliveOnly and baka['worm_alive'] == True:
                    baka_food_counter = baka['eaten_food_counter']
                    food_coeff = baka_food_counter[0] + baka_food_counter[1] + baka_food_counter[2] + \
                                 baka_food_counter[3] * 2 + baka_food_counter[4] * 5
                    bests_bakas.append((food_coeff, baka['baka_brain']))
                elif not aliveOnly:
                    baka_food_counter = baka['eaten_food_counter']
                    food_coeff = baka_food_counter[0] + baka_food_counter[1] + baka_food_counter[2] + \
                                 baka_food_counter[3] * 2 + baka_food_counter[4] * 5
                    bests_bakas.append((food_coeff, baka['baka_brain']))
        bests_bakas.sort()

        if bastardsCount <= len(bests_bakas):
            return bests_bakas[0:bastardsCount]
        else:
            return bests_bakas

    def cross_brain(self, brain1 = brain_abstract(), brain2 = brain_abstract(), brain3 = brain_abstract()):
        connectome1 = brain1.get_all_synapse_weight()
        connectome2 = brain2.get_all_synapse_weight()
        connectome3 = brain3.get_all_synapse_weight()
        result_connectome = connectome1.copy()
        i = 0
        conn_size = len(connectome1)
        while i < conn_size:
            if random() > self.CR:
                result_connectome[i] = connectome1[i] + self.F * (connectome2[i] - connectome3[i])
            i+=1

        new_brain = brain_abstract()
        new_brain.load_consciousness(result_connectome)
        return  new_brain

    def learn_baka_brain(self, cord, steps = 10):
        enviroment = self.see_around()
        decision = self.baka_brain.guess(enviroment)
        guess_cord = self.thought_to_action(decision)
        if guess_cord[0] != cord[0] or guess_cord[1] != cord[1]:
            new_decision = self.cord_to_thought(cord)
            self.baka_brain.learn(input=enviroment, output=new_decision, maxSteps=steps)

    def fireShow(self):
        if self.universe_on_fire:
            conflag_cord_beg = (self.conflagration_cord[0][0] - 1, self.conflagration_cord[0][1] - 1)
            conflag_cord_end = (self.conflagration_cord[1][0] + 1, self.conflagration_cord[1][1] + 1)
            bound_collision_count = 0
            if conflag_cord_beg[0] < 0:
                conflag_cord_beg = (0, conflag_cord_beg[1])
                bound_collision_count += 1
            if conflag_cord_beg[1] < 0:
                conflag_cord_beg = (conflag_cord_beg[0], 0)
                bound_collision_count += 1
            if conflag_cord_end[0] > self.N:
                conflag_cord_end = (self.N, conflag_cord_end[1])
                bound_collision_count += 1
            if conflag_cord_end[1] > self.M:
                conflag_cord_end = (conflag_cord_end[0], self.M)
                bound_collision_count += 1
            self.conflagration_cord = (conflag_cord_beg, conflag_cord_end)

            i = conflag_cord_beg[0]
            while i <= conflag_cord_end[0]:
                j = conflag_cord_beg[1]
                while j <= conflag_cord_end[1]:
                    self.get_cell(i, j).set_color(self.get_random_color())
                    j += 1
                i += 1
            return bound_collision_count == 4

        else:
            wormhead = self.get_wormhead()
            wormhead_cord = wormhead.get_cord()
            self.conflagration_cord = (wormhead_cord, wormhead_cord)
            self.universe_on_fire = True
            wormhead.set_color(self.get_random_color())
            return False

    def see_around(self):
        surrounding_space = [[0] * 25, [0] * 3]
        worm_head = self.get_wormhead()
        worm_head_cord = worm_head.get_cord()
        i = worm_head_cord[0]-2 if worm_head_cord[0]-2 > -1 else 0
        j = worm_head_cord[1]-2 if worm_head_cord[1]-2 > -1 else 0
        goal_i = worm_head_cord[0] + 2 if worm_head_cord[0] + 2 < self.N else self.N
        goal_j = worm_head_cord[1] + 2 if worm_head_cord[1] + 2 < self.M else self.M
        n = 0
        while i <= goal_i:
            jj = j
            while jj <= goal_j:
                tmp_cell = self.get_cell(i,j)
                cell_type = tmp_cell.get_groupNum()
                surrounding_space[0][n] = cell_type
                if cell_type == self.colorHeadNum:
                    surrounding_space[1][0] += 1
                    surrounding_space[1][1] += 1
                    surrounding_space[0][n] += tmp_cell.get_azimuth()
                elif cell_type > self.colorBgrNum:
                    surrounding_space[1][0] += 1
                n+=1
                jj+=1
            i+=1
        surrounding_space[0][12] = worm_head.get_azimuth()
        surrounding_space[1][2] = worm_head.get_azimuth()
        #mem = self.get_last_step()
        #surrounding_space[1][3] = mem[0]
        #surrounding_space[1][4] = mem[1]
        #surrounding_space[1][5] = mem[2]
        return surrounding_space

    def save_all_brains_to_file(self, filename = 'frozen_minds.txt'):
        brains = []
        f = open(filename, 'w')
        iter = len(self.baka_list)
        i = 0
        while i < iter:
            if self.baka_list[i]['worm_alive'] == True or True:
                brains.append(self.baka_list[i]['baka_brain'].frozed_mind())
            i+=1
        f.write(json.dumps(brains))
        f.close()
    
    def load_brains_from_file(self, filename = 'frozen_minds.txt'):
        frozen_brains = []
        f = open(filename, 'r')
        json_brains = f.read()
        f.close()
        frozen_brains = json.loads(json_brains)
        i = 0
        min_iter = min(len(frozen_brains), len(self.baka_list))
        while i < min_iter:
            env = self.getBakaEnviroment(i+1)
            env['baka_brain'].unfrozed_mind(frozen_brains[i])
            self.updateBakaEnvitoment(i+1, env)     
            i+=1       
    
    def check_changes_near_every_changed_cell(self):
        changing_cells = []
        changing_cells_count = 0
        ch = 0
        while ch < self.changed_cells_count:
            cell_cord = self.changed_cells[ch].get_cord()
            i = -1
            while i <= 1:
                j = -1
                while j <= 1:
                    cell_condidat = self.get_cell(cell_cord[0] + i, cell_cord[1] + j)
                    changed = cell_condidat.predict_future()
                    if changed:
                        changing_cells.append(cell_condidat)
                        changing_cells_count += 1
                    j += 1
                i += 1
            ch += 1

        return changing_cells

    def move_cell_to_random_freeplace(self, cell):
        rand_place_cord = self.get_random_freeplace()
        cord_of_cell = cell.get_cord()
        self.set_freeplace(rand_place_cord['placeNum'], cord_of_cell)
        cell.swap_to_cord(rand_place_cord['cord'])

    def get_cell(self, N=0, M=0):
        if N > self.N:
            N = 0
        if M > self.M:
            M = 0
        return self.map[N][M]

    def get_cell_size(self):
        return self.cell_size

    def get_color(self, r=0, g=0, b=0):
        clr = ((r * 1.0, g * 1.0, b * 1.0),
               '#' + r.to_bytes(1, 'little').hex().__str__()
               + g.to_bytes(1, 'little').hex().__str__()
               + b.to_bytes(1, 'little').hex().__str__())
        return clr

    def get_random_color(self):
        rand = Random()
        r = rand.randint(0, 255)
        g = rand.randint(0, 255)
        b = rand.randint(0, 255)
        rand_color = ((r * 1.0, g * 1.0, b * 1.0),
                      '#' + r.to_bytes(1, 'little').hex().__str__()
                      + g.to_bytes(1, 'little').hex().__str__()
                      + b.to_bytes(1, 'little').hex().__str__())
        return rand_color

    def get_color_by_num(self, colorNum):
        if colorNum < self.groups_count:
            return self.color_list[colorNum]
        else:
            return self.get_color()

    def get_freeplace(self, placeNum):
        if placeNum >= self.freeplace_coun:
            placeNum = 0
        return self.freeplace[placeNum]

    def get_random_freeplace(self):
        rand_placeNum = randint(0, self.freeplace_count - 1)
        return {'placeNum': rand_placeNum, 'cord': self.freeplace[rand_placeNum]}

    def get_random_cord(self):
        return (randint(0, self.N), randint(0, self.M))

    def get_wormhead_cord(self):
        return self.wormhead.get_cord()

    def get_wormhead(self):
        return self.wormhead

    def get_foodcell(self, food_type):
        return self.food_list.at(food_type)

    def get_foodcell_cord(self, food_type):
        return self.food_list.at(food_type).get_cord()

    def get_all_foodcell_cord(self):
        cord_list = []
        for food in self.food_list:
            cord_list.append(food.get_cord())
        return cord_list

    def get_bgr_color(self):
        if self.mode == 'BakaFight':
            return self.color_list[self.colorBgrNum][1]
        else:
            return self.color_list[1][1]

    def get_agent_color(self):
        return self.color_list[self.colorHeadNum][1]

    def get_last_step(self, depth = -1):
        if abs(depth) > len(self.lasts_brainOut):
            depth = 0
        return self.lasts_brainOut[depth]

    def get_baka_brain(self):
        return self.baka_brain

    def set_cell(self, cell, N=0, M=0):
        if N <= self.N and M <= self.M:
            self.map[N][M] = cell

    def set_cell_size(self, size=5):
        self.cell_size = size

    def set_freeplace(self, placeNum, cord):
        if placeNum >= self.freeplace_count:
            placeNum = 0
        self.freeplace[placeNum] = cord

    def set_wormhead_by_cord(self, cord):
        self.wormhead_cord = cord
        self.wormhead = self.get_cell(self.wormhead_cord[0], self.wormhead_cord[1])
        self.worm.append(self.wormhead)

    def set_wormhead(self, cell):
        self.wormhead_cord = cell.get_cord()
        self.wormhead = cell
        self.worm.append(cell)

    def set_foodcell(self, cell, food_type):
        if (len(self.food_list) - 1) >= food_type:
            self.food_list[food_type] = cell
        else:
            self.food_list.append(cell)

    def memorize_step(self, step_move = [0] * 3):
        self.lasts_brainOut.append(step_move)
        if len(self.lasts_brainOut) > 4:
            self.lasts_brainOut.pop(0)

    def set_die_age(self, age):
        self.die_age = age
    
