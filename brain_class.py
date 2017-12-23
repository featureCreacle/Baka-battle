import tkinter
import json
from math import *
from random import *
from tkinter import *

class brain_abstract():
    ''' # один слой это лист туплов: колво нейронов в группе,
                                        # плюс(True) или минус(False) на выходе нейронов группы,
                                        # номер функции нейронов группы,
                                        # дискретный выход у нейронов или нет (True - да)
                                        # тулпа с номерами inputs-групп, с которыми связанна нейронная группа
                                        # длинна входного input-вектора группы
                                        # коэф нормализации вывода группы
            laysConfigs = [ [(15, True, 1, False,  (0,), 25, 10),  (5, True,  1, False, (1,),   6, 10)],
                            [( 7, True, 0, True, (0,1), 20,  10),  (4, True,  1, False, (0,1), 20, 10)],
                            [( 5, True, 1, False, (0,1), 11,  5),  (15, False, 0, False, (0,1), 11,  5)],
                            [( 6, True, 1, False, (0,1), 20, 10)],
                            [( 2, True, 1, True,  (0,), 6,  0)]                                        ]'''
    def __init__(self, laysConfigs = [], NNtemp = 70, cooldownTemp = 50):
        self.lays = []
        self.lay_counts = 0
        self.NN_learning_temp = NNtemp
        self.NN_cooldown_temp = cooldownTemp
        if not laysConfigs:
            # один слой это лист туплов: колво нейронов в группе,
                                        # плюс(True) или минус(False) на выходе нейронов группы,
                                        # номер функции нейронов группы,
                                        # дискретный выход у нейронов или нет (True - да)
                                        # тулпа с номерами inputs-групп, с которыми связанна нейронная группа
                                        # длинна входного input-вектора группы
                                        # коэф нормализации вывода группы
            laysConfigs = [ [(10, True, 1, False, (0,),   25, 10), (7, False, 1, False, (0,),   25, 10), (3, True,  1, False, (1,),  3, 10)],
                            [(10, False, 0, True, (0,1),17, 0),  (7, True,  1, True, (0,1,2), 20, 0)],
                            #[( 5, True, 1, False, (0,1), 14,  5),  (15, False, 0, False, (0,1), 14,  5)],
                            [( 5, True, 1, False, (0,1), 17, 10)],
                            [( 2, True, 1, True,  (0,), 5,  0)]                                        ]

        for lay_conf in laysConfigs:
            self.lays.append(lay_abstact(lay_conf))
            
        self.frozen_mind = {'scheme':laysConfigs, 'weights' :self.get_all_synapse_weight()}

    def train(self, input = [], output = []):
        lays_output = []
        lays_output.append(input)
        lay_input = input
        for lay in self.lays:
            lays_output.append( lay.get_excited(lay_input) )
            lay_input = lays_output[-1]

        desire_lay_output = output
        i = len(self.lays)
        j = 0
        while i > 0:
            lay_out = lays_output[i]
            lay_in = lays_output[i-1]
            lay_temp = self.NN_learning_temp - (j*self.NN_cooldown_temp)
            changingNeuronsCount = round(self.lays[i-1].neuron_count * lay_temp  / 100)
            Mu = lay_temp / ( len(self.lays) * 100 )
            changingNeuronsWeightCount = round(self.lays[i-2].neuron_count * (self.NN_learning_temp - (j*self.NN_cooldown_temp) )  / 100)

            cool_inp = self.lays[i-1].fcingCooldown(lay_in, lay_out, desire_lay_output,
                                                    changingNeuronsCount, changingNeuronsWeightCount, Mu)
            desire_lay_output = cool_inp
            i-=1
            j+=1

    def get_err_out(self, input = [[],], output = [[],]):
        return (1,1)

    def guess(self, input = []):
        lay_output = []
        lay_input = input

        for lay in self.lays:
            lay_output = lay.get_excited(lay_input)
            lay_input = lay_output

        return  lay_output

    def learn(self, input = [], output = [], maxSteps = 3):
        desire_lay_output = output
        net_output = self.guess(input)
        i = 0
        while not self.isEqualOuts(net_output, desire_lay_output) and i < maxSteps:
            self.train(input, output)
            net_output = self.guess(input)
            i+=1

    def think(self):
        pass
        
    def isEqualOuts(self, out1, out2):
        try:
            len1 = len(out1)
            i = 0
            while i < len1:
                len2 = len(out1[i])
                j = 0
                while j < len2:
                    if out1[i][j] != out2[i][j]:
                        return False
                    j+=1
                i+=1
        finally:
            return False

        return True

    def get_lay_ref(self, layNum = 0):
        return self.lays[layNum]

    def get_all_synapse_weight(self):
        synapse_weight = []
        for lay in self.lays:
            for lay_group in lay.neuronGroups_list:
                for neuron in lay_group:
                    synapse_weight.extend(neuron.get_weights())
        return synapse_weight

    def load_consciousness(self, consciousness = [0]*100):
        neuron_weights = []
        shift = 0
        for lay in self.lays:
            for lay_group in lay.neuronGroups_list:
                for neuron in lay_group:
                    neuron_weights = consciousness[shift:shift+neuron.weightsCount]
                    neuron.set_weights(neuron_weights)
                    shift += neuron.weightsCount

    def get_draw_scheme(self):
        draw_scheme = []
        for lay in self.lays:
            draw_scheme.append(lay.get_draw_scheme())
        return draw_scheme

    def draw_brain_scheme(self, root_win = None, width = 800, height = 600):
        worm_brain = self
        brain_scheme_width = width
        brain_scheme_height = height
        if root_win == None:
            self.scheme_window = Tk()
            self.scheme_window.title("Brain scheme")
        else:
            self.scheme_window = Toplevel(root_win)
        self.canvas_brain = Canvas(self.scheme_window, width=brain_scheme_width + 60, height=brain_scheme_height + 40,
                                   bg='white')
        self.canvas_brain.pack()

        # draw_scheme pattern [[ (Ncount, sign, links), ],]
        brain_draw_scheme = worm_brain.get_draw_scheme()

        color_lay = self.get_color(200, 200, 200)[1]
        color_pos_group = self.get_color(150, 250, 150)[1]
        color_neg_group = self.get_color(250, 150, 150)[1]
        color_digital_neuron = self.get_color(120, 110, 120)[1]
        color_analog_neuron = self.get_color(130, 170, 130)[1]
        color_input = self.get_color(250, 250, 60)[1]
        color_output = self.get_color(60, 250, 250)[1]
        color_inside = self.get_color(250, 200, 120)[1]

        lay_width = round(brain_scheme_width / len(brain_draw_scheme))
        lay_height = brain_scheme_height
        layNum = 0
        dec_lay_height = brain_scheme_height / (2.5 * len(brain_draw_scheme) )
        group_out_cord = []
        prev_lay_group_out_cord = []
        for lay_scheme in brain_draw_scheme:
            group_count = len(lay_scheme)
            group_height = round(lay_height / group_count)
            groups_heights = []
            for group in lay_scheme:
                groups_heights.append(group[0])
            groups_heights =  self.get_proportion(groups_heights)
            max_group_height = max(groups_heights)
            min_group_height = min(groups_heights)
            while (max_group_height - min_group_height) > 2 * min_group_height:
                minNum = groups_heights.index(min_group_height)
                maxNum = groups_heights.index(max_group_height)
                delta = groups_heights[maxNum] * 0.1
                groups_heights[maxNum] -= delta
                groups_heights[minNum] += delta
                max_group_height = max(groups_heights)
                min_group_height = min(groups_heights)

            x_preset = 30 + layNum * lay_width
            y_preset = 20 + layNum * dec_lay_height
            lay_thicc = lay_width/3

            self.canvas_brain.create_rectangle(x_preset+lay_thicc, y_preset, x_preset+lay_thicc*2,
                                         lay_height-y_preset, fill=color_lay, outline=color_lay)
            gr_bound = 10
            lay_h = lay_height - 2 * y_preset
            gr_preset = y_preset + gr_bound
            gNum = 0
            for group_h in groups_heights:
                group_h *= lay_h
                color_group = color_pos_group if lay_scheme[gNum][1] > 0 else color_neg_group
                n_count = lay_scheme[gNum][0]
                #lay
                x_group_preset = x_preset + lay_thicc + gr_bound
                self.canvas_brain.create_rectangle(x_group_preset,
                                                   gr_preset,
                                                   x_group_preset + lay_thicc - 2 * gr_bound,
                                                   group_h+gr_preset - 2 * gr_bound,
                                                   fill=color_group, outline=color_group)#"#000000")
                #in
                x_input_vec_preset = x_preset + lay_thicc/2
                x_inp_vec_width = lay_thicc/10
                self.canvas_brain.create_rectangle(x_input_vec_preset,
                                                   gr_preset,
                                                   x_input_vec_preset + x_inp_vec_width,
                                                   group_h + gr_preset - 2 * gr_bound,
                                                   fill=color_input, outline="#000000")

                #in vector
                weight_count = lay_scheme[gNum][4]
                weight_height = (group_h - 2 * gr_bound)/weight_count               
                for i in range(0,weight_count):
                    self.canvas_brain.create_line(x_input_vec_preset,
                                                  gr_preset + i*weight_height,
                                                  x_input_vec_preset + x_inp_vec_width,
                                                  gr_preset + i*weight_height,
                                                  fill='#000000')
                #in link
                for link in lay_scheme[gNum][3]:
                    if brain_draw_scheme.index(lay_scheme) == 0:
                        break
                    cord = prev_lay_group_out_cord[link]
                    self.canvas_brain.create_line(cord[0],
                                                  cord[1],
                                                  x_input_vec_preset,
                                                  gr_preset + (group_h - 2 * gr_bound) / 2,
                                                  fill='#000000', arrow=LAST)

                #out
                x_output_vec_preset = x_input_vec_preset + 2* lay_thicc
                x_out_vec_width = lay_thicc/10
                self.canvas_brain.create_rectangle(x_output_vec_preset,
                                                   gr_preset,
                                                   x_output_vec_preset + x_out_vec_width,
                                                   group_h + gr_preset - 2 * gr_bound,
                                                   fill=color_output, outline="#000000")

                group_out_cord.append((x_output_vec_preset + x_out_vec_width,
                                       gr_preset + (group_h - 2 * gr_bound) / 2))
                                       
                #out vector
                out_height = (group_h - 2 * gr_bound)/n_count
                for i in range(0,n_count):
                    self.canvas_brain.create_line(x_output_vec_preset,
                                                  gr_preset + i*out_height,
                                                  x_output_vec_preset + x_inp_vec_width,
                                                  gr_preset + i*out_height,
                                                  fill='#000000')

                nr_preset = gr_preset
                nr_bound_w = 4
                nr_bound_h = 4
                neuron_draw_size = (group_h - 2 * gr_bound) / n_count
                neuron_area_width = lay_thicc - 2 * gr_bound
                min_neuron_draw_size = (lay_thicc - 2 * gr_bound)/2
                gr_h = (group_h - 2 * gr_bound)
                column_count = 1
                n_in_col = n_count
                neuron_area = 0
                down_shift = 0
                if neuron_draw_size > neuron_area_width:
                    nr_bound_w = 4
                    neuron_draw_size = neuron_area_width - 2 * nr_bound_w
                    nr_bound_h = (gr_h - (neuron_draw_size * n_count)) / (2 * n_count)
                elif neuron_draw_size < neuron_area_width:
                    if neuron_draw_size < min_neuron_draw_size:
                        neuron_area = sqrt((neuron_area_width * gr_h) / (n_count*1.5) )
                        column_count = ceil((n_count * neuron_area) / gr_h)
                        n_in_col = round(n_count / column_count)
                        column_count += 0 if n_count % column_count == 0 else 1
                        if neuron_area_width/column_count < neuron_area:
                            neuron_draw_size = neuron_area_width/column_count
                            column_count = ceil((n_count * neuron_draw_size) / gr_h)
                            n_in_col = round(n_count / column_count)
                            column_count += 0 if n_count % column_count == 0 else 1
                        else:
                            neuron_draw_size = neuron_area

                        nr_bound_w = (neuron_area_width - (neuron_draw_size * column_count)) / (column_count + 1)
                        nr_bound_h = (gr_h - (neuron_draw_size * n_in_col)) / (2 * n_in_col)
                        if nr_bound_w < 1:
                            nr_bound_w = 1
                            nr_bound_h = 1
                            neuron_draw_size = (neuron_area_width - (nr_bound_w * (column_count + 1))) / column_count

                        if neuron_draw_size < 2:
                            nr_bound_w = 1
                            nr_bound_h = 1
                            neuron_draw_size = 2
                            neuron_area = neuron_draw_size+nr_bound_w+nr_bound_h
                            n_count = round((neuron_area_width/neuron_area) * (gr_h/neuron_area))
                            column_count = ceil((n_count * neuron_area) / gr_h)
                            n_in_col = round(n_count / column_count)
                            n_count = column_count * n_in_col
                            
                        down_shift = (gr_h - ((neuron_draw_size + 2*nr_bound_h) * (n_in_col)))/2
                        
                    else:
                        nr_bound_h = neuron_draw_size*0.1
                        neuron_draw_size = neuron_draw_size - 2 * nr_bound_h
                        nr_bound_w = (neuron_area_width - neuron_draw_size ) / 2

                colNum = 0
                nrNum = 0
                draw_neuron = 0
                while draw_neuron < n_count:
                    nrNum+=1
                    if lay_scheme[gNum][2]:
                        color_neuron = color_digital_neuron
                    else:
                        color_neuron = color_analog_neuron
                    # neuron
                    self.canvas_brain.create_arc(x_group_preset + nr_bound_w + colNum * (neuron_draw_size + nr_bound_w),
                                                 nr_preset + down_shift + nr_bound_h,
                                                 x_group_preset + nr_bound_w + colNum * (
                                                         neuron_draw_size + nr_bound_w) + neuron_draw_size,
                                                 nr_preset + down_shift + neuron_draw_size + nr_bound_h,
                                                 start=1, extent=359, fill=color_neuron, outline=color_neuron)

                    if lay_scheme[gNum][2]:
                        #center
                        self.canvas_brain.create_rectangle(x_group_preset + nr_bound_w + colNum * (
                                                           neuron_draw_size + nr_bound_w) + neuron_draw_size / 3,
                                                           nr_preset + down_shift + nr_bound_h + neuron_draw_size / 3,
                                                           x_group_preset + nr_bound_w + colNum * (
                                                                   neuron_draw_size + nr_bound_w) + 2 * neuron_draw_size / 3,
                                                           nr_preset + down_shift + 2 * neuron_draw_size / 3 + nr_bound_h,
                                                           fill=color_inside, outline=color_inside)

                    else:
                        #center
                        self.canvas_brain.create_arc(x_group_preset + nr_bound_w + colNum * (
                                                     neuron_draw_size + nr_bound_w) + neuron_draw_size / 3,
                                                     nr_preset + down_shift + nr_bound_h + neuron_draw_size / 3,
                                                     x_group_preset + nr_bound_w + colNum * (
                                                             neuron_draw_size + nr_bound_w) + 2 * neuron_draw_size / 3,
                                                     nr_preset + down_shift + 2 * neuron_draw_size / 3 + nr_bound_h,
                                                     start=1, extent=359, fill=color_inside, outline=color_inside)


                    self.canvas_brain.create_arc(x_group_preset + nr_bound_w + colNum * (neuron_draw_size + nr_bound_w) + neuron_draw_size / 3,
                                                 nr_preset + down_shift + nr_bound_h + neuron_draw_size / 3,
                                                 x_group_preset + nr_bound_w + colNum * (
                                                        neuron_draw_size + nr_bound_w) + 2 * neuron_draw_size / 3,
                                                 nr_preset + down_shift + 2 * neuron_draw_size / 3 + nr_bound_h,
                                                 start=1, extent=359, fill=color_inside, outline=color_inside)

                    if colNum == 0:
                        #input
                        self.canvas_brain.create_line(x_input_vec_preset + x_inp_vec_width,
                                                      gr_preset + (group_h - 2 * gr_bound) / 2,
                                                      x_group_preset,
                                                      nr_preset + down_shift + nr_bound_h + neuron_draw_size/2,
                                                      fill='#000000', arrow=LAST)
                        #output
                        self.canvas_brain.create_line(x_group_preset + lay_thicc - 2 * gr_bound,
                                                      nr_preset + down_shift + nr_bound_h + neuron_draw_size/2,
                                                      x_output_vec_preset,
                                                      nr_preset + down_shift + nr_bound_h + neuron_draw_size/2,
                                                      fill='#000000', arrow=LAST)
                        #self.canvas_brain.create_line(x_output_vec_preset,
                        #                              nr_preset,
                        #                              x_output_vec_preset + x_out_vec_width,
                        #                              nr_preset,
                        #                              fill='#000000')

                    nr_preset = nr_preset + neuron_draw_size + 2 * nr_bound_h
                    if nrNum == n_in_col:
                        colNum+=1
                        nrNum = 0
                        if colNum % 2 == 0:
                            nr_preset = gr_preset
                        else:
                            nr_preset = gr_preset
                    draw_neuron+=1
                gr_preset = group_h+gr_preset
                gNum+=1
            layNum+=1
            prev_lay_group_out_cord = group_out_cord
            group_out_cord = []
        self.scheme_window.mainloop()

    def get_proportion(self, vector = []):
        sum = 0
        for el in vector:
            sum += el
        out_vector = []
        for el in vector:
            out_vector.append(el / sum)
        return out_vector

    def get_color(self, r=0, g=0, b=0):
        clr = ((r * 1.0, g * 1.0, b * 1.0),
               '#' + r.to_bytes(1, 'little').hex().__str__()
               + g.to_bytes(1, 'little').hex().__str__()
               + b.to_bytes(1, 'little').hex().__str__())
        return clr

    def frozed_mind(self):
        build_scheme = []
        for lay in self.lays:
            build_scheme.append(lay.get_build_scheme())
        consciousness = self.get_all_synapse_weight()
        self.frozen_mind = {'scheme': build_scheme, 'weights': consciousness}
        return self.frozen_mind
                        
    def unfrozed_mind(self, ice_piece):
        self.__init__(laysConfigs = ice_piece['scheme'])
        self.load_consciousness(consciousness = ice_piece['weights'])

    def save_to_file(self, filename = 'frozen_mind.txt'):
        self.frozed_mind()
        f = open(filename, 'w')
        f.write(json.dumps(self.frozen_mind))
        f.close()
        
    def load_from_file(self, filename = 'frozen_mind.txt'):
        f = open(filename, 'r')
        json_mind = f.read()
        self.unfrozed_mind(ice_piece = json.loads(json_mind))
        f.close()
        
    def __gt__(self, other):
        return self.NN_learning_temp > other.NN_learning_temp
    def __lt__(self, other):
        return self.NN_learning_temp < other.NN_learning_temp
    def __ge__(self, other):
        return self.NN_learning_temp >= other.NN_learning_temp
    def __le__(self, other):
        return self.NN_learning_temp <= other.NN_learning_temp

class lay_abstact():
    '''layConfig = [ (0, True, 0, (0,), 25, 0), ]
     лист туплов: колво нейронов в группе,
                # плюс(True) или минус(False) на выходе нейронов группы,
                # номер функции нейронов группы,
                # дискретный выход у нейронов или нет (True - да)
                # тулпа с номерами inputs-групп, с которыми связанна нейронная группа
                # длинна входного input-вектора группы
                # коэф нормализации вывода группы'''
    def __init__(self, layConfig = [ (0, True, 0, True, (0,), 25, 0), ]):
        self.neuronGroups_count = len(layConfig)
        self.neuronGroups_list = []
        self.neuronGroups_inputs_link = []
        self.groupsNormalization_coeff = []
        self.neuron_count = 0
        if layConfig[0][0] == 0:
            pass
        else:
            for neuron_group in layConfig:
                neuton_with_pos_out = neuron_group[1]
                lay_temp = []
                i = 0
                while i < neuron_group[0]:
                    neuron = neuron_abstact(generateWeightsCount=neuron_group[5],
                                            positiveOutput=neuton_with_pos_out,
                                            funcNum=neuron_group[2],
                                            digitalOut=neuron_group[3] )
                    lay_temp.append(neuron)
                    self.neuron_count+=1
                    i+=1
                self.neuronGroups_list.append(lay_temp)
                self.neuronGroups_inputs_link.append(neuron_group[4])
                self.groupsNormalization_coeff.append(neuron_group[6])

    def get_excited(self, inputsGoups = [[],]):
        output_groups = []
        i=0
        while i<self.neuronGroups_count:
            group_input = []
            neurou_group_output = []
            for inputgroupNum in self.neuronGroups_inputs_link[i]:
                group_input.extend(inputsGoups[inputgroupNum])
            for neuron in self.neuronGroups_list[i]:
                neurou_group_output.append(neuron.spike( group_input ))
            if self.groupsNormalization_coeff[i] != 0:
                neurou_group_output = self.normalize_vector(neurou_group_output, self.groupsNormalization_coeff[i])
            output_groups.append(neurou_group_output)
            i+=1
        return  output_groups

    def normalize_vector(self, inputVector = [], norm_coeff = 1):
        min_val = min(inputVector)
        max_val = max(inputVector)
        delitel = max_val - min_val
        normalOutputVector = []
        if delitel == 0:
            for x_val in inputVector:
                norm_x_val = 0
                normalOutputVector.append(norm_x_val)
        else:
            for x_val in inputVector:
                norm_x_val = ( (x_val - min_val) * norm_coeff )/delitel
                normalOutputVector.append(norm_x_val)

        return  normalOutputVector

    def fcingCooldown(self, inputGroups = [[],], output = [[],], desire_out = [[],],
                            changingNeuronsCount = 1, changingNeuronsWeightCount = 1, Lwa = 1):
        errOuts = self.get_err_out(output, desire_out)
        errOuts.sort()
        changing_errOuts = []
        changing_neuron_weights_info = []
        inputs = []
        len_groupinput = []
        i = 0
        while i < self.neuronGroups_count:
            group_input = []
            for inputgroupNum in self.neuronGroups_inputs_link[i]:
                group_input.extend(inputGroups[inputgroupNum])
            inputs.append(group_input)
            i+=1
        i = 0
        while i < changingNeuronsCount and i < len(errOuts):
            changing_errOuts.append(errOuts[i])
            i+=1

        for err_out in changing_errOuts:
            err_neuron = self.neuron_at(err_out[2])
            err_neuron_vector = err_neuron.learning_spike(inputs[err_out[2][0]])
            err_neuron_vector.sort()
            i = 0
            Nwa = Lwa
            while i < changingNeuronsWeightCount:
                if err_out[1] == 1:#надо увеличить выход нейрона

                    if err_neuron_vector[i][1] < err_out[1]: #вес нейрона находится на отрицательном ребре
                        Nwa = - Lwa
                        self.neuron_at(err_out[2]).adjust_weight(err_neuron_vector[i][2], Nwa)
                    else: #вес нейрона находится на положительном ребре
                        Nwa = Lwa
                        self.neuron_at(err_out[2]).adjust_weight(err_neuron_vector[i][2], Nwa)

                else: #надо уменьшить выход

                    if err_neuron_vector[i][1] < err_out[1]: #вес нейрона находится на отрицательном ребре
                        Nwa = Lwa
                        self.neuron_at(err_out[2]).adjust_weight(err_neuron_vector[i][2], Nwa)
                    else:  #вес нейрона находится на положительном ребре
                        Nwa = - Lwa
                        self.neuron_at(err_out[2]).adjust_weight(err_neuron_vector[i][2], Nwa)

                changing_neuron_weights_info.append( (err_out, err_neuron_vector[i], Nwa) )
                i+=1

        input_group_len = []
        for input in inputGroups:
            input_group_len.append(len(input))

        for ch_neur in changing_neuron_weights_info:
            #изменить инпут пропорионально аджастам весов нейронов
            Gnum = 0
            Nnum = ch_neur[1][2]
            for link in self.neuronGroups_inputs_link[Gnum]:
                if Nnum >= input_group_len[link]:
                    Nnum -= input_group_len[link]
                else:
                    Gnum = link
                    break
            inputGroups[Gnum][Nnum] += inputGroups[Gnum][Nnum] * ch_neur[2]

        return inputGroups

    def get_err_out(self, list, example_list):
        '''На входе лист листов с интами'''
        err_elements = []
        try:
            len1 = len(list)
            i = 0
            while i < len1:
                len2 = len(list[i])
                j = 0
                while j < len2:
                    if list[i][j] != example_list[i][j]:
                        diff = example_list[i][j] - list[i][j]
                        delta = abs(diff)
                        sign = 1 if diff > 0 else -1
                        er_element = (delta, sign, (i,j))
                        err_elements.append(er_element)
                    j+=1
                i+=1
        finally:
            return err_elements

        return err_elements

    def neuron_at(self, coord):
        '''coord = (groupNum, neuronNum)'''
        return self.neuronGroups_list[coord[0]][coord[1]]

    def get_neuron_group_ref(self, NgNum = 0):
        return self.neuronGroups_list[NgNum]

    def get_draw_scheme(self):
        draw_scheme = []
        for group in self.neuronGroups_list:
            neuron_count = len(group)
            sigh = group[0].output_sign
            digital_out = group[0].digital_out
            links = self.neuronGroups_inputs_link[self.neuronGroups_list.index(group)]
            weights_count = group[0].weightsCount
            draw_scheme.append((neuron_count, sigh, digital_out, links, weights_count))
        return draw_scheme

    def get_build_scheme(self):
        build_scheme = []
        for group in self.neuronGroups_list:
            neuron_count = len(group)
            sigh = True if group[0].output_sign == 1 else False
            digital_out = group[0].digital_out
            links = self.neuronGroups_inputs_link[self.neuronGroups_list.index(group)]
            weights_count = group[0].weightsCount
            func_num = group[0].funcNum
            normal_coef = self.groupsNormalization_coeff[self.neuronGroups_list.index(group)]
            build_scheme.append((neuron_count, sigh, func_num, digital_out, links, weights_count, normal_coef))
        return build_scheme

class neuron_abstact():
    '''funcNum: 0 - сумматор (если цифровой выход, то пороговый сумматор
                        1 - рациональная сигмоида
                threshold  порог срабатывания для цифрового выхода'''
    def __init__(self, weights = [], generateWeightsCount = 0, positiveOutput = True, funcNum = 0,
                                        digitalOut = True):

        if generateWeightsCount > 0:
            self.weights = []
            self.set_random_weights(weights, generateWeightsCount)
        else:
            self.weights = weights
            self.weightsCount = len(self.weights)

        self.output_sign = 1 if positiveOutput else -1
        self.digital_out = digitalOut
        self.funcNum = funcNum
        self.threshold = round(generateWeightsCount/2)
        self.recurrent_mem = []

    def set_random_weights(self, weights = [], weightsCount = 25,):
        if len(weights) == 0:
            self.weights = [(9.9 + x - x) / randint(1, 100) + 0.1 for x in range(weightsCount)]
        else:
            self.weights = weights.copy()
        self.weightsCount = len(self.weights)

    def set_funcNum(self,funcNum):
        self.funcNum = funcNum

    def set_weights(self, weights = []):
        self.weights = weights
        self.weightsCount = len(self.weights)
        if self.funcNum == 1:
            for weight in self.weights:
                if weight == 0:
                    weights = self.get_random_weight(from_=0.1,to=10)

    def get_weights(self):
        return self.weights

    def get_random_weight(self, from_ = 0, to = 10):
        return (to - from_) / randint(1, 100) + from_

    def spike(self, input = []):
        if self.funcNum == 0: #linear sum
            output = 0
            i = 0
            while i < self.weightsCount:
                output += ( input[i] * self.weights[i] )
                i+=1
            if self.digital_out:
                return 1 if output > self.threshold else 0
            else:
                return output * self.output_sign
        
        elif self.funcNum == 1: #rational sig
            output = 0
            i = 0
            while i < self.weightsCount:
                abs_inp = abs(input[i])
                output +=  abs_inp / ( abs_inp + abs(self.weights[i]) )
                i+=1
            if self.digital_out:
                return 1 if output > self.threshold else 0
            else:
                return output * self.output_sign
        
        elif self.funcNum == 2: #RelU
            output = 0
            i = 0
            while i < self.weightsCount:
                output += ( input[i] + self.weights[i] ) * self.weights[i] #закоментить, если черви сойдут с ума
                i+=1
            output = max([0, output])
            if self.digital_out:
                return 1 if output > self.threshold else 0
            else:
                return output * self.output_sign
            
        else:
            pass

    def learning_spike(self, input = []):
        '''output = [(x,y,z),] x - input*weight, y - output sigh, z - weight number'''
        output = []
        i = 0
        if self.funcNum == 1:
            while i < self.weightsCount:
                abs_inp = abs(input[i])
                output.append(  ( abs_inp/(abs_inp + self.weights[i]), self.output_sign, i ) )
                i+=1
        else:
            while i < self.weightsCount:
                output.append(  (input[i] * self.weights[i], self.output_sign, i) )
                i+=1
        return output
        
    def adjust_weight(self, weightNum = 0, Nwa = 0 ):
        if self.funcNum == 1:
            self.weights[weightNum] -= Nwa * self.weights[weightNum]
            if self.weights[weightNum] == 0:
                self.weights[weightNum] = self.get_random_weight(from_=0.1,to=10)
        else:
            self.weights[weightNum] += Nwa * self.weights[weightNum]
