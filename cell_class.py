from random import *
from math import *

class cell_abstact():
    def __init__(self, parent, cord=(0, 0), color=((255, 255, 255), '#ffffff'), groupNumber=0, bakaNumber=0):
        self.parent = parent
        self.set_cord(cord)
        self.set_color(color)
        self.group_number = groupNumber
        self.isAlive = bakaNumber > 0
        self.baka_number = bakaNumber
        self.azimuth = 0

    def quality_of_neighbors_by_color(self):
        q_list = []
        i = -1
        while i <= 1:
            q_list.append([])
            j = -1
            while j <= 1:
                q_list[i + 1].append(
                    self._color_distance(
                        self.get_colorRGB(),
                        self.parent.get_cell(self.x + i, self.y + j).get_colorRGB()
                    )
                )
                j += 1
            i += 1
        return q_list

    def decision_to_move(self, qual_neig_list, threshold, count):
        decicion = 0
        for list_x in qual_neig_list:
            for list_y in list_x:
                if list_y > threshold:
                    decicion += 1

        if decicion >= count:
            return True
        else:
            return False

    def _color_distance(self, c1, c2):
        return sqrt(((c1[0] - c2[0]) ** 2) +
                    ((c1[1] - c2[1]) ** 2) +
                    ((c1[2] - c2[2]) ** 2))

    def predict_future(self):
        cell_cord = self.get_cord()
        cell_group = self.get_groupNum()
        alive_neighbors = 0
        changed = False
        i = -1
        while i <= 1:
            j = -1
            while j <= 1:
                cell_tmp = self.parent.get_cell(cell_cord[0] + i, cell_cord[1] + j)
                alive_neighbors += cell_tmp.get_groupNum()
                j += 1
            i += 1
        if (cell_group == self.parent.colorDeadNum) and (self.parent.bornRule.find(str(alive_neighbors)) != -1):
            return True
        elif cell_group == self.parent.colorAliveNum and self.parent.survRule.find(str(alive_neighbors)) == -1:
            return True
        return False

    def checkIsAlive(self, mode):
        if mode == 'BakaFight':
            return self.isAlive
        elif mode == 'Conway':
            return self.get_groupNum() == self.parent.colorAliveNum

    def move_to_random_freeplace(self):
        self.parent.move_cell_to_random_freeplace(self)

    def move_to_neighbors(self):
        pass

    def swap_to_cord(self, cord):
        foreign_cell = self.parent.get_cell(cord[0], cord[1])

        foreign_cell.color, self.color = self.color, foreign_cell.color
        foreign_cell.group_number, self.group_number = self.group_number, foreign_cell.group_number
        foreign_cell.azimuth, self.azimuth = self.azimuth, foreign_cell.azimuth
        foreign_cell.isAlive, self.isAlive = self.isAlive, foreign_cell.isAlive
        foreign_cell.baka_number, self.baka_number = self.baka_number, foreign_cell.baka_number

    def become_alien(self, colorNum):
        clr = self.parent.get_color_by_num(colorNum)
        self.set_groupNum(colorNum)
        self.set_color(clr)
        self.baka_number = 0

    def kill(self):
        self.isAlive = False

    def become_baka(self, bakaNum, colorNum):
        self.become_alien(colorNum)
        self.isAlive = bakaNum > 0
        self.baka_number = bakaNum

    def color_is_num(self, colorNum):
        return self.parent.get_color_by_num(colorNum)[1] == self.get_color()[1]

    def color_is(self, color):
        return color[1] == self.get_color()[1]

    def set_cord(self, cord=(0, 0)):
        self.x = cord[0]
        self.y = cord[1]

    def set_color(self, color):
        self.colorRGB = color[0]
        self.color = color[1]

    def set_groupNum(self, groupNum):
        self.group_number = groupNum

    def set_azimuth(self, azimuth):
        self.azimuth = azimuth

    def get_cord(self):
        return (self.x, self.y)

    def get_color(self):
        return (self.colorRGB, self.color)

    def get_colorRGB(self):
        return self.colorRGB

    def get_colorName(self):
        return self.color

    def get_groupNum(self):
        return self.group_number

    def get_azimuth(self):
        return self.azimuth

    def get_bakaNum(self):
        return self.baka_number
