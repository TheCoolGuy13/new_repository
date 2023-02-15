import sys
from tkinter import *
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen


class AddressException(Exception):
    pass


class TooManyLoadsException(AddressException):
    pass


class MoreTwoTypeOfLoadsException(AddressException):
    pass


class Calculations:
    loads_features = []  # список со всеми нагрузками и их характеристиками
    beam_coordinate = []  # список с координатами опор и длиной балки [длина, коор. неподвижной, коор. подвижной]
    coordinate = []
    moment_load = []
    vert_load = []
    hor_load = []
    distr_load = []

    def cancellation(self):
        self.loads_features.clear()
        self.beam_coordinate.clear()
        self.coordinate.clear()
        self.moment_load.clear()
        self.vert_load.clear()
        self.hor_load.clear()
        self.distr_load.clear()
        self.X_support1 = 0
        self.X_support2 = 0
        self.length = 0
        self.Ha = 0
        self.Ra = 0
        self.Rb = 0
        self.sumY = 0

    def list(self):
        label_list.config(text="")
        label_list.config(text=str(self.loads_features))

    def load_sort(self):  # Сортировка усилий в списки моментов, сил верт., сил гор., распр. нагрузок
        print(1, self.loads_features)
        count_n = len(self.loads_features)
        while count_n > 0:
            load = self.loads_features[count_n - 1]
            count_n -= 1
            if load[0] == "M":
                self.moment_load += [load]
            elif load[0] == 'F':
                self.vert_load += [load]
            elif load[0] == 'H':
                self.hor_load += [load]
            elif load[0] == 'q':
                self.distr_load += [load]
        print(2, self.moment_load, self.vert_load, self.hor_load, self.distr_load)

    def beam_splitting(self):  # метод для разбиения балки на части в соответствии с координатами опор и усилий
        self.coordinate += [self.beam_coordinate[0]]
        self.coordinate += [self.beam_coordinate[1]]
        self.coordinate += [self.beam_coordinate[2]]
        for i in range(1, 5):
            if i == 1:
                m = len(self.moment_load)
                if m == 1:
                    self.coordinate += [self.moment_load[0][2]]
                elif m == 0:
                    pass
                if m == 2:
                    self.coordinate += [self.moment_load[0][2]]
                    self.coordinate += [self.moment_load[1][2]]
            elif i == 2:
                v = len(self.vert_load)
                if v == 1:
                    self.coordinate += [self.vert_load[0][2]]
                elif v == 0:
                    pass
                if v == 2:
                    self.coordinate += [self.vert_load[0][2]]
                    self.coordinate += [self.vert_load[1][2]]
            elif i == 3:
                h = len(self.hor_load)
                if h == 1:
                    self.coordinate += [self.hor_load[0][2]]
                elif h == 0:
                    pass
                if h == 2:
                    self.coordinate += [self.hor_load[0][2]]
                    self.coordinate += [self.hor_load[1][2]]
            elif i == 4:
                q = len(self.distr_load)
                if q == 1:
                    self.coordinate += [self.distr_load[0][2]]
                    self.coordinate += [self.distr_load[0][3]]
                elif q == 0:
                    pass
                elif q == 2:
                    self.coordinate += [self.distr_load[0][2]]
                    self.coordinate += [self.distr_load[0][3]]
                    self.coordinate += [self.distr_load[1][2]]
                    self.coordinate += [self.distr_load[1][3]]
        print(3, self.coordinate)
        coordinate_list = list(set(self.coordinate))
        self.coordinate = coordinate_list
        self.coordinate.sort()
        print(4, self.coordinate)  # по итогу имеем отсортированный по возрастанию список координат

    def load_features(self, checklist):  # сюда передается список со всеми характеристиками усилий из метода characteristic_усилие
        self.loads_features += [checklist]
        print('Список всех сил с характеристиками', self.loads_features)

    def deleting(self, y):  # метод удаления усилия из списка load_features
        self.loads_features.pop(y - 1)
        print('Список всех сил с характеристиками', self.loads_features)

    def printing(self):
        print(self.loads_features)

    def __init__(self):
        self.X_support1 = 0
        self.X_support2 = 0
        self.length = 0
        self.Ha = 0
        self.Ra = 0
        self.Rb = 0
        self.sumY = 0

    def beam_features(self, checklist):  # сюда передается список с координатами опор и длиной
        self.beam_coordinate += [checklist[0]]
        self.beam_coordinate += [checklist[1]]
        self.beam_coordinate += [checklist[2]]
        print('Длина балки равна', checklist[0])
        print('Шарнирно неподвижная опора расположена на расстоянии', checklist[1], 'от левого края')
        print('Шарнирно подвижная опора расположена на расстоянии', checklist[2], 'от левого края')
        self.X_support1 = checklist[1]  # координата шарнирно-неподвижной опоры (A)
        self.X_support2 = checklist[2]  # координата шарнирно-подвижной опоры (B)
        self.length = checklist[0]

    def support_reactions(self):  # при нахождении момента брал по часовой положительно
        self.Ha = 0
        for i in range(0, len(self.hor_load)):
            self.Ha += -self.hor_load[i][1]
        pointA = 0  # сумма моментов усилий относительно точки А
        pointB = 0  # сумма моментов усилий относительно точки B
        for i in range(0, len(self.moment_load)):
            pointA += self.moment_load[i][1]
        pointB = pointA
        ver_force = 0
        for i in range(0, len(self.vert_load)):
            ver_force += self.vert_load[i][1]
            print(ver_force)
            if self.vert_load[i][2] < self.X_support1:
                pointA += self.vert_load[i][1] * (self.X_support1 - self.vert_load[i][2])
            else:
                pointA += -self.vert_load[i][1] * (self.vert_load[i][2] - self.X_support1)
            if self.vert_load[i][2] < self.X_support2:
                pointB += self.vert_load[i][1] * (self.X_support2 - self.vert_load[i][2])
            else:
                pointB += -self.vert_load[i][1] * (self.vert_load[i][2] - self.X_support2)
        for i in range(0, len(self.distr_load)):
            ver_force += self.distr_load[i][1] * (self.distr_load[i][3] - self.distr_load[i][2])
            if self.distr_load[i][2] < self.X_support1 and self.distr_load[i][3] < self.X_support1:
                pointA += self.distr_load[i][1] * (self.distr_load[i][3] - self.distr_load[i][2]) * (
                            (self.distr_load[i][3] - self.distr_load[i][2]) * 0.5 + (
                                self.X_support1 - self.distr_load[i][3]))
            elif self.distr_load[i][2] <= self.X_support1 <= self.distr_load[i][3]:
                pointA += self.distr_load[i][1] * (self.X_support1 - self.distr_load[i][2]) * (
                            (self.X_support1 - self.distr_load[i][2]) * 0.5)
                pointA += -self.distr_load[i][1] * (self.distr_load[i][3] - self.X_support1) * (
                            (self.distr_load[i][3] - self.X_support1) * 0.5)
            elif self.distr_load[i][2] > self.X_support1 and self.distr_load[i][3] > self.X_support1:
                pointA += -self.distr_load[i][1] * (self.distr_load[i][3] - self.distr_load[i][2]) * (
                            (self.distr_load[i][3] - self.distr_load[i][2]) * 0.5 + (
                                self.distr_load[i][2] - self.X_support1))
            if self.distr_load[i][2] < self.X_support2 and self.distr_load[i][3] < self.X_support2:
                pointB += self.distr_load[i][1] * (self.distr_load[i][3] - self.distr_load[i][2]) * (
                            (self.distr_load[i][3] - self.distr_load[i][2]) * 0.5 + (
                                self.X_support2 - self.distr_load[i][3]))
            elif self.distr_load[i][2] <= self.X_support2 <= self.distr_load[i][3]:
                pointB += self.distr_load[i][1] * (self.X_support2 - self.distr_load[i][2]) * (
                            (self.X_support2 - self.distr_load[i][2]) * 0.5)
                pointB += -self.distr_load[i][1] * (self.distr_load[i][3] - self.X_support2) * (
                            (self.distr_load[i][3] - self.X_support2) * 0.5)
            elif self.distr_load[i][2] > self.X_support2 and self.distr_load[i][3] > self.X_support2:
                pointB += -self.distr_load[i][1] * (self.distr_load[i][3] - self.distr_load[i][2]) * (
                            (self.distr_load[i][3] - self.distr_load[i][2]) * 0.5 + (
                                self.distr_load[i][2] - self.X_support2))
        if self.X_support1 < self.X_support2:
            self.Ra = -pointB / abs(self.X_support2 - self.X_support1)
            self.Rb = pointA / abs(self.X_support2 - self.X_support1)
        else:
            self.Ra = pointB / abs(self.X_support2 - self.X_support1)
            self.Rb = -pointA / abs(self.X_support2 - self.X_support1)
        self.Ra = round(self.Ra, 3)
        self.Rb = round(self.Rb, 3)
        self.sumY = ver_force + self.Ra + self.Rb
        self.sumY = round(self.sumY, 3)
        print(pointA, pointB)
        print("Если у силы знак минус, то она направлена вниз(влево), если +, то направлена вверх (вправо)")
        print('Реакция Ra = ', self.Ra)
        print('Реакция Rb = ', self.Rb)
        print('Реакция Ha = ', self.Ha)
        print('Проверка: сумма сил по оси Y равна', self.sumY)

    def message(self):
        text_message.config(state=NORMAL)
        text_message.place(x=1525, y=500, width=375, height=100)
        text_message.insert("1.0", "Если у силы знак минус, то она направлена вниз(влево), если +, то направлена вверх (вправо)")
        text_message.insert(END, "\nРеакция Ra = ")
        text_message.insert(END, str(self.Ra))
        text_message.insert(END, "\nРеакция Rb = ")
        text_message.insert(END, str(self.Rb))
        text_message.insert(END, "\nРеакция Ha = ")
        text_message.insert(END, str(self.Ha))
        text_message.insert(END, "\nПроверка: сумма сил по оси Y равна ")
        text_message.insert(END, str(self.sumY))
        text_message.config(state=DISABLED)

    def drawing_beam(self):
        def opora_a(x):
            turtle.up()
            x = x * 10
            turtle.up()
            turtle.goto(x, 0)
            turtle.down()
            turtle.circle(5)
            turtle.right(60)
            turtle.forward(25)
            turtle.left(180)
            turtle.forward(25)
            turtle.left(120)
            turtle.forward(25)
            turtle.right(60)
            turtle.forward(5)
            turtle.right(180)
            turtle.forward(40)
            turtle.up()

        def opora_b(x):
            turtle.up()
            x = x * 10
            turtle.goto(x, 0)
            turtle.down()
            turtle.circle(5)
            turtle.right(90)
            turtle.forward(11.65)
            turtle.left(90)
            turtle.circle(-5)
            turtle.up()
            turtle.right(90)
            turtle.forward(10)
            turtle.left(90)
            turtle.down()
            turtle.forward(20)
            turtle.left(180)
            turtle.forward(40)
            turtle.up()

        def balka(l):
            turtle.up()
            l = l * 10
            turtle.pensize(3)
            turtle.setposition(0, 10)
            turtle.down()
            turtle.goto(l, 10)
            turtle.up()
            turtle.pensize(0)

        turtle.seth(0)
        balka(self.beam_coordinate[0])
        opora_a(self.beam_coordinate[1])
        opora_b(self.beam_coordinate[2])

    def drawing_load(self):

        def F_down(x):
            turtle.up()
            x = x * 10
            turtle.pencolor("red")
            turtle.setposition(x, 10)
            turtle.down()
            turtle.seth(0)
            turtle.left(60)
            turtle.forward(10)
            turtle.left(180)
            turtle.forward(10)
            turtle.right(120)
            turtle.forward(10)
            turtle.left(180)
            turtle.forward(10)
            turtle.left(150)
            turtle.forward(50)
            turtle.up()
            turtle.pencolor("black")

        def F_up(x):
            turtle.up()
            turtle.pencolor("red")
            x = x * 10
            turtle.setposition(x, -40)
            turtle.down()
            turtle.seth(0)
            turtle.left(90)
            turtle.forward(50)
            turtle.seth(0)
            turtle.right(60)
            turtle.forward(10)
            turtle.right(180)
            turtle.forward(10)
            turtle.left(120)
            turtle.forward(10)
            turtle.right(180)
            turtle.forward(10)
            turtle.up()
            turtle.pencolor("black")

        def q_down(x1, x2):
            turtle.up()
            turtle.pencolor("green")
            x1 = x1 * 10
            x2 = x2 * 10
            turtle.setposition(x1, 10)
            turtle.down()
            turtle.seth(0)
            while x1 < x2:
                if x2 - x1 > 20:
                    turtle.left(60)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.right(120)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.left(150)
                    turtle.forward(20)
                    turtle.right(90)
                    turtle.forward(20)
                    turtle.right(90)
                    turtle.forward(20)
                    turtle.seth(0)
                    turtle.left(60)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.right(120)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.seth(0)
                    x1 += 20
                else:
                    turtle.left(60)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.right(120)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.left(150)
                    turtle.forward(20)
                    turtle.right(90)
                    turtle.forward(x2 - x1)
                    turtle.right(90)
                    turtle.forward(20)
                    turtle.seth(0)
                    turtle.left(60)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.right(120)
                    turtle.forward(10)
                    turtle.left(180)
                    turtle.forward(10)
                    turtle.seth(0)
                    x1 += 20
            turtle.up()
            turtle.pencolor("black")

        def q_up(x1, x2):
            turtle.up()
            x1 = x1 * 10
            x2 = x2 * 10
            turtle.pencolor("green")
            turtle.setposition(x1, 10)
            turtle.down()
            turtle.seth(0)
            while x1 < x2:
                if x2 - x1 > 20:
                    turtle.right(60)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.left(120)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.seth(0)
                    turtle.right(90)
                    turtle.forward(20)
                    turtle.left(90)
                    turtle.forward(20)
                    turtle.left(90)
                    turtle.forward(20)
                    turtle.seth(0)
                    turtle.right(60)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.left(120)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.seth(0)
                    x1 += 20
                else:
                    turtle.right(60)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.left(120)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.seth(0)
                    turtle.right(90)
                    turtle.forward(20)
                    turtle.left(90)
                    turtle.forward(x2 - x1)
                    turtle.left(90)
                    turtle.forward(20)
                    turtle.seth(0)
                    turtle.right(60)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.left(120)
                    turtle.forward(10)
                    turtle.right(180)
                    turtle.forward(10)
                    turtle.seth(0)
                    x1 += 20
            turtle.up()
            turtle.pencolor("black")

        def H_left(h, l):
            turtle.up()
            if h == 1:
                x = l
            else:
                x = 0
            turtle.pencolor("blue")
            x = x * 10
            if x == 0:
                turtle.setposition(x, 10)
            else:
                turtle.setposition(x + 50, 10)
            turtle.down()
            turtle.seth(0)
            turtle.left(180)
            turtle.forward(50)
            turtle.right(150)
            turtle.forward(10)
            turtle.right(180)
            turtle.forward(10)
            turtle.left(120)
            turtle.forward(10)
            turtle.right(180)
            turtle.forward(10)
            turtle.up()
            turtle.pencolor("black")

        def H_right(h, l):
            turtle.up()
            if h == 1:
                x = l
            else:
                x = 0
            x = x * 10
            turtle.pencolor("blue")
            if x == 0:
                turtle.setposition(x - 50, 10)
            else:
                turtle.setposition(x, 10)
            turtle.down()
            turtle.seth(0)
            turtle.forward(50)
            turtle.right(150)
            turtle.forward(10)
            turtle.right(180)
            turtle.forward(10)
            turtle.left(120)
            turtle.forward(10)
            turtle.right(180)
            turtle.forward(10)
            turtle.up()
            turtle.pencolor("black")

        def M_clockwise(x):  # по часовой
            turtle.up()
            x = x * 10
            turtle.pencolor("orange")
            turtle.setposition(x, 10)
            turtle.down()
            turtle.seth(0)
            turtle.left(135)
            turtle.forward(28.28)
            turtle.seth(90)
            turtle.circle(-20, 180)
            turtle.left(165)
            turtle.forward(10)
            turtle.left(180)
            turtle.forward(10)
            turtle.right(120)
            turtle.forward(10)
            turtle.left(180)
            turtle.forward(10)
            turtle.up()
            turtle.pencolor("black")

        def M_counterclockwise(x):  # против часовой
            turtle.up()
            x = x * 10
            turtle.pencolor("orange")
            turtle.setposition(x, 10)
            turtle.down()
            turtle.seth(0)
            turtle.left(45)
            turtle.forward(28.28)
            turtle.seth(90)
            turtle.circle(20, 180)
            turtle.right(165)
            turtle.forward(10)
            turtle.left(180)
            turtle.forward(10)
            turtle.left(120)
            turtle.forward(10)
            turtle.left(180)
            turtle.forward(10)
            turtle.up()
            turtle.pencolor("black")

        for i in range(0, len(self.vert_load)):
            if self.vert_load[i][1] > 0:
                F_up(self.vert_load[i][2])
            else:
                F_down(self.vert_load[i][2])
        for i in range(0, len(self.hor_load)):
            if self.hor_load[i][1] > 0:
                H_right(self.hor_load[i][2], self.length)
            else:
                H_left(self.hor_load[i][2], self.length)
        for i in range(0, len(self.moment_load)):
            if self.moment_load[i][1] > 0:
                M_clockwise(self.moment_load[i][2])
            else:
                M_counterclockwise(self.moment_load[i][2])
        for i in range(0, len(self.distr_load)):
            if self.distr_load[i][1] > 0:
                q_up(self.distr_load[i][2], self.distr_load[i][3])
            else:
                q_down(self.distr_load[i][2], self.distr_load[i][3])


class Beam:  # класс балка, содержит всю характеристику балки (длина, координаты опор)
    __loads = []  # список с перечислением нагрузок без характеристик
    beam_coordinates = []  # список с координатами опор и длины балки

    def __init__(self):
        self.mount = [0, 0, 0, 0]

    def cancellation(self):
        self.__loads.clear()
        self.mount = [0, 0, 0, 0]

    def move_on(self, load):  # метод, благодаря которому происходит размещение нагрузки на балке
        self.__loads += [load]
        load.correct_loads(self.__loads)

    def deleting(self, x):  # метод удаления усилия из списка __loads
        self.__loads.pop(x - 1)
        print('Список всех приложенных сил:', self.__loads)

    def printing(self):
        print(self.__loads)

    def is_applied(self):  # нагружена ли нагрузкой балка?
        return len(self.__loads) > 0

    def characteristic_beam(self, coordinate, l, x1, x2):
        self.beam_coordinates = [l, x1, x2]
        coordinate.beam_features(self.beam_coordinates)


class Load:  # класс нагрузка - общий класс

    def loading(self, beam):  # размещение нагрузки на балке
        beam.move_on(self)

    def __init__(self, a_name):
        self.__features = []
        self.mount = [0, 0, 0, 0]
        self._name = a_name

    def correct_loads(self, list_copy):  # метод проверки ограничений на кол-во приложенных усилий
        if len(list_copy) > 6:
            raise TooManyLoadsException('Более 6 нагрузок')

        else:
            self.mount = [0, 0, 0, 0]
            for i in list_copy:
                if type(i) == Moment:
                    self.mount[0] += 1
                # print('moment: ',self.mount[0])
                elif type(i) == Vert_force:
                    self.mount[1] += 1
                    # print('vert: ',self.mount[1])
                elif type(i) == Hor_force:
                    self.mount[2] += 1
                # print('hor: ',self.mount[2])
                elif type(i) == Distr_load:
                    self.mount[3] += 1
                # print('distr: ',self.mount[3])
            if self.mount[0] > 2 or self.mount[1] > 2 or self.mount[2] > 2 or self.mount[3] > 2:
                raise MoreTwoTypeOfLoadsException('Больше двух нагрузок одного типа')
        print('Список всех приложенных сил:', list_copy)


class Moment(Load):  # класс момент, содержит всю характеристику приложенного сосредоточенного момента
    # (значение, направление, координаты)
    __features = []

    def __repr__(self):
        return "↺(%s)" % self._name

    def characteristic_moment(self, feature, M, x):  # запись всех характеристик момента
        self.__features = ["M", M, x]
        feature.load_features(self.__features)


class Vert_force(Load):  # Класс вертикальная сила, содержит всю характеристику приложенной сосредоточенной верт. силы
    # (значение, направление верх/низ, координаты)
    __features = []

    def __repr__(self):
        return "↑(%s)" % self._name

    def characteristic_vert(self, feature, F, x):  # запись всех характеристик вертикальной силы
        self.__features = ["F", F, x]
        feature.load_features(self.__features)


class Hor_force(Load):  # класс горизонтальная сила, содержит всю характеристику приложенной сосредоточенной
    # гориз. силы (значение, направление право/лево, координаты)
    __features = []

    def __repr__(self):
        return "→(%s)" % self._name

    def characteristic_hor(self, feature, H, x):  # запись всех характеристик горизонтальной силы
        self.__features = ["H", H, x]
        feature.load_features(self.__features)


class Distr_load(Load):  # класс распределенная нагрузка, содержит всю характеристику распределенной нагрузки
    # (координата начала, координата конца, значение, направление)
    __features = []

    def __repr__(self):
        return "↓↓↓↓(%s)" % self._name

    def characteristic_distr(self, feature, q, x1, x2):  # запись всех характеристик распределенной нагрузки
        self.__features = ["q", q, x1, x2]
        feature.load_features(self.__features)


length = 0
X1 = 0
X2 = 0
q_x1 = 0
q_x2 = 0
q_force = 0
F_x = 0
F_force = 0
H_x = 0
H_force = 0
M_x = 0
M_force = 0
delete = 0


def enter_beam():  # метод получения, передачи и визуализации значений длины и координат опор из полей entry
    global length
    length = float(entry_l.get())
    global X1
    X1 = float(entry_1.get())
    global X2
    X2 = float(entry_2.get())
    entry_l.config(state="readonly")
    entry_1.config(state="readonly")
    entry_2.config(state="readonly")
    an_beam.characteristic_beam(calculator, length, X1, X2)
    btn_l.config(state='disabled')
    btn_count.config(state=NORMAL)
    btn_paint.config(state=NORMAL)


def choice_load_q():
    def enter_load_q():
        global q_force
        q_force = float(entry_q.get())
        global q_x1
        q_x1 = float(entry_q_x1.get())
        global q_x2
        q_x2 = float(entry_q_x2.get())
        x = Distr_load("q")
        y = Calculations()
        x.characteristic_distr(y, q_force, q_x1, q_x2)
        x.loading(an_beam)
        entry_q.place_forget()
        entry_q_x1.place_forget()
        entry_q_x2.place_forget()
        btn_enter_q.place_forget()
        label_q.place_forget()
        label_q_x1.place_forget()
        label_q_x2.place_forget()
        btn_F.place(x=1550, y=300)
        btn_H.place(x=1620, y=300)
        btn_q.place(x=1690, y=300)
        btn_M.place(x=1760, y=300)
        btn_delete.place(x=1830, y=300)
        Calculations.list(y)

    def back():
        btn_back.place_forget()
        entry_q.place_forget()
        entry_q_x1.place_forget()
        entry_q_x2.place_forget()
        btn_enter_q.place_forget()
        label_q.place_forget()
        label_q_x1.place_forget()
        label_q_x2.place_forget()
        btn_F.place(x=1550, y=300)
        btn_H.place(x=1620, y=300)
        btn_q.place(x=1690, y=300)
        btn_M.place(x=1760, y=300)
        btn_delete.place(x=1830, y=300)
    btn_F.place_forget()
    btn_H.place_forget()
    btn_M.place_forget()
    btn_q.place_forget()
    btn_delete.place_forget()
    entry_q = Entry(root)
    label_q = Label(root, text="Значение распределенной нагрузки:")
    label_q_x1 = Label(root, text="Координата начала:")
    label_q_x2 = Label(root, text="Координата конца:")
    entry_q_x1 = Entry(root)
    entry_q_x2 = Entry(root)
    entry_q.place(x=1780, y=300)
    label_q.place(x=1560, y=300)
    entry_q_x1.place(x=1780, y=330)
    label_q_x1.place(x=1654, y=330)
    entry_q_x2.place(x=1780, y=360)
    label_q_x2.place(x=1660, y=360)
    btn_enter_q = Button(root, width=8, text="Ввод", command=enter_load_q)
    btn_enter_q.place(x=1765, y=400)
    btn_back = Button(root, text="Назад", width=8, command=back)
    btn_back.place(x=1840, y=400)


def choice_load_M():
    def enter_load_M():
        global M_force
        M_force = float(entry_M.get())
        global M_x
        M_x = float(entry_M_x.get())
        x = Moment("M")
        y = Calculations()
        x.characteristic_moment(y, M_force, M_x)
        x.loading(an_beam)
        back()
        Calculations.list(y)

    def back():
        btn_back.place_forget()
        entry_M.place_forget()
        entry_M_x.place_forget()
        btn_enter_M.place_forget()
        label_M.place_forget()
        label_M_x.place_forget()
        btn_F.place(x=1550, y=300)
        btn_H.place(x=1620, y=300)
        btn_q.place(x=1690, y=300)
        btn_M.place(x=1760, y=300)
        btn_delete.place(x=1830, y=300)
    btn_F.place_forget()
    btn_H.place_forget()
    btn_M.place_forget()
    btn_q.place_forget()
    btn_delete.place_forget()
    entry_M = Entry(root)
    label_M = Label(root, text="Значение сосредоточенного момента:")
    label_M_x = Label(root, text="Координата момента:")
    entry_M_x = Entry(root)
    entry_M.place(x=1780, y=300)
    label_M.place(x=1550, y=300)
    entry_M_x.place(x=1780, y=330)
    label_M_x.place(x=1644, y=330)
    btn_enter_M = Button(root, width=8, text="Ввод", command=enter_load_M)
    btn_enter_M.place(x=1765, y=400)
    btn_back = Button(root, text="Назад", width=8, command=back)
    btn_back.place(x=1840, y=400)


def choice_load_F():
    def enter_load_F():
        global F_force
        F_force = float(entry_F.get())
        global F_x
        F_x = float(entry_F_x.get())
        x = Vert_force("F")
        y = Calculations()
        x.characteristic_vert(y, F_force, F_x)
        x.loading(an_beam)
        back()
        Calculations.list(y)

    def back():
        btn_back.place_forget()
        entry_F.place_forget()
        entry_F_x.place_forget()
        btn_enter_F.place_forget()
        label_F.place_forget()
        label_F_x.place_forget()
        btn_F.place(x=1550, y=300)
        btn_H.place(x=1620, y=300)
        btn_q.place(x=1690, y=300)
        btn_M.place(x=1760, y=300)
        btn_delete.place(x=1830, y=300)
    btn_F.place_forget()
    btn_H.place_forget()
    btn_M.place_forget()
    btn_q.place_forget()
    btn_delete.place_forget()
    entry_F = Entry(root)
    label_F = Label(root, text="Значение вертикальной силы:")
    label_F_x = Label(root, text="Координата вертикальной силы:")
    entry_F_x = Entry(root)
    entry_F.place(x=1780, y=300)
    label_F.place(x=1596, y=300)
    entry_F_x.place(x=1780, y=330)
    label_F_x.place(x=1584, y=330)
    btn_enter_F = Button(root, width=8, text="Ввод", command=enter_load_F)
    btn_enter_F.place(x=1765, y=400)
    btn_back = Button(root, text="Назад", width=8, command=back)
    btn_back.place(x=1840, y=400)


def choice_load_H():
    def enter_load_H():
        global H_force
        H_force = float(entry_H.get())
        global H_x
        H_x = float(entry_H_x.get())
        x = Hor_force("H")
        y = Calculations()
        x.characteristic_hor(y, H_force, H_x)
        x.loading(an_beam)
        back()
        Calculations.list(y)

    def back():
        btn_back.place_forget()
        entry_H.place_forget()
        entry_H_x.place_forget()
        btn_enter_H.place_forget()
        label_H.place_forget()
        label_H_x.place_forget()
        btn_F.place(x=1550, y=300)
        btn_H.place(x=1620, y=300)
        btn_q.place(x=1690, y=300)
        btn_M.place(x=1760, y=300)
        btn_delete.place(x=1830, y=300)
    btn_F.place_forget()
    btn_H.place_forget()
    btn_M.place_forget()
    btn_q.place_forget()
    btn_delete.place_forget()
    entry_H = Entry(root)
    label_H = Label(root, text="Значение горизонтальной силы силы:")
    label_H_x = Label(root, text="Точка приложения(1-справа, 2-слева):")
    entry_H_x = Entry(root)
    entry_H.place(x=1780, y=300)
    label_H.place(x=1550, y=300)
    entry_H_x.place(x=1780, y=330)
    label_H_x.place(x=1550, y=330)
    btn_enter_H = Button(root, width=8, text="Ввод", command=enter_load_H)
    btn_enter_H.place(x=1765, y=400)
    btn_back = Button(root, text="Назад", width=8, command=back)
    btn_back.place(x=1840, y=400)


def deleting_load():
    def enter_del():
        global delete
        delete = int(entry_del.get())
        y = Calculations()
        an_beam.deleting(delete)
        calculator.deleting(delete)
        back()
        Calculations.list(y)

    def back():
        btn_back.place_forget()
        entry_del.place_forget()
        btn_enter_del.place_forget()
        label_del.place_forget()
        btn_F.place(x=1550, y=300)
        btn_H.place(x=1620, y=300)
        btn_q.place(x=1690, y=300)
        btn_M.place(x=1760, y=300)
        btn_delete.place(x=1830, y=300)
    btn_F.place_forget()
    btn_H.place_forget()
    btn_M.place_forget()
    btn_q.place_forget()
    btn_delete.place_forget()
    entry_del = Entry(root)
    label_del = Label(root, text="Введите порядковый номер усилия")
    entry_del.place(x=1780, y=300)
    label_del.place(x=1567, y=300)
    btn_back = Button(root, text="Назад", width=8, command=back)
    btn_back.place(x=1840, y=330)
    btn_enter_del = Button(root, width=8, text="Ввод", command=enter_del)
    btn_enter_del.place(x=1765, y=330)


def painting_all():
    Calculations.drawing_beam(calculator)
    Calculations.drawing_load(calculator)


def counting_all():
    Calculations.load_sort(calculator)
    Calculations.beam_splitting(calculator)
    Calculations.support_reactions(calculator)
    Calculations.message(calculator)
    btn_H.config(state='disabled')
    btn_M.config(state='disabled')
    btn_F.config(state='disabled')
    btn_q.config(state='disabled')
    btn_delete.config(state='disabled')
    btn_count.config(state='disabled')


def exit():
    sys.exit()


def restart():
    btn_l.config(state="normal")
    entry_l.config(state="normal")
    entry_1.config(state="normal")
    entry_2.config(state="normal")
    entry_l.delete(0, 'end')
    entry_1.delete(0, 'end')
    entry_2.delete(0, 'end')
    label_list.config(text="Нагрузок пока нет")
    Calculations.cancellation(calculator)
    Beam.cancellation(an_beam)
    turtle.clear()
    btn_M.config(state="normal")
    btn_q.config(state="normal")
    btn_F.config(state="normal")
    btn_H.config(state="normal")
    btn_delete.config(state="normal")
    btn_count.config(state="normal")
    text_message.config(state=NORMAL)
    text_message.delete('1.0', END)
    text_message.place_forget()


if __name__ == '__main__':
    an_beam = Beam()
    calculator = Calculations()
    root = Tk()
    root.title('Вычисление внутренних напряжений')
    root.geometry('1920x1080')
    root.resizable(width=False, height=False)
    root.config(bg='gray')
    canvas = ScrolledCanvas(root, width=1500, height=900)
    canvas.pack(side=LEFT)
    screen = TurtleScreen(canvas)
    turtle = RawTurtle(canvas)
    turtle.ht()
    turtle.speed(0)
    turtle.up()
    entry_l = Entry(root)  # поле ввода длины
    entry_1 = Entry(root)  # поле ввода координаты неподвижной опоры
    entry_2 = Entry(root)  # поле ввода координаты подвижной опоры
    text_rules = Text(root)
    text_rules.place(x=1525, y=610, width=375, height=360)
    text_rules.insert("1.0", "Правила использования программы:")
    text_rules.insert(END, "\n1) Вначале заполняется характеристика балки")
    text_rules.insert(END, "\n2) После нажмите кнопку 'Ввод' ниже. После нажатия изменить характеристики балки уже нельзя")
    text_rules.insert(END, "\n3) Выберите силу, которую хотите приложить на балку")
    text_rules.insert(END, "\n4) Направления усилий соответствуют знаку, с которым написано значение нагрузки")
    text_rules.insert(END, "\n   Если значение положительное, то усилие направлено вверх/по часовой стрелке/вправо")
    text_rules.insert(END, "\n   Если значение отрицательное, то усилие направлено вниз/против часовой стрелке/влево")
    text_rules.insert(END, "\n4) Заполните все характеристики усилия и нажмите кнопку 'Ввод'")
    text_rules.insert(END, "\n5) Вы можете наложить не более 6 нагрузок на одну балку, а также не более 2 нагрузок одного вида")
    text_rules.insert(END, "\n6) В нижней части экрана отображаются все усилия, которые приложены к балке")
    text_rules.insert(END, "\n7) После нагружения балки выбранными усилиями нажмите кнопку 'Вычисления'")
    text_rules.insert(END, "\n8) Нажмите кнопку 'Рисование'")
    text_rules.config(state=DISABLED)
    label_text = Label(root, text="Перечисление приложенных нагрузок:")
    label_text.place(x=600, y=1000)
    label_list = Label(root, text="Нагрузок пока нет")
    label_list.place(x=430, y=1025)
    label1 = Label(root, text="Программа для вычисления внутренних усилий балок", font=("Calibri", 16))
    label1.place(x=800, y=10)
    entry_l.place(x=1780, y=100)
    label2 = Label(root, text="Длина вашей балки:")
    label2.place(x=1650, y=100)
    entry_1.place(x=1780, y=130)
    label3 = Label(root, text="Координата шарнирно неподвижной опоры:")
    label3.place(x=1515, y=130)
    entry_2.place(x=1780, y=160)
    label4 = Label(root, text="Координата шарнирно подвижной опоры:")
    label4.place(x=1527, y=160)
    btn_l = Button(root, width=8, text='Ввод', command=enter_beam)  # кнопка для запоминания
    btn_l.place(x=1840, y=190)
    label5 = Label(root, text="Характеристика балки", font=("Calibri", 14))
    label5.place(x=1650, y=60)
    label6 = Label(root, text="Характеристика усилий", font=("Calibri", 14))
    label6.place(x=1650, y=230)
    label7 = Label(root, text="Выберите усилие, которое хотите приложить", font=("Calibri", 12))
    label7.place(x=1580, y=265)
    btn_M = Button(root, width=6, text='↺M', command=choice_load_M)
    btn_q = Button(root, width=6, text='↓↓↓↓q', command=choice_load_q)
    btn_F = Button(root, width=6, text='↑F', command=choice_load_F)
    btn_H = Button(root, width=6, text='→H', command=choice_load_H)
    btn_delete = Button(root, width=8, text='Удаление', command=deleting_load)
    btn_delete.place(x=1830, y=300)
    btn_count = Button(root, width=12, text='1. Вычисление', command=counting_all)
    btn_count.place(x=1500, y=1000)
    btn_count.config(state=DISABLED)
    btn_paint = Button(root, width=12, text='2. Нарисовать', command=painting_all)
    btn_paint.place(x=1600, y=1000)
    btn_paint.config(state=DISABLED)
    btn_exit = Button(root, width=12, text='4. Выход', command=exit)
    btn_exit.place(x=1800, y=1000)
    btn_reset = Button(root, width=12, text='3. Сброс', command=restart)
    btn_reset.place(x=1700, y=1000)
    text_message = Text(root)
    btn_F.place(x=1550, y=300)
    btn_H.place(x=1620, y=300)
    btn_q.place(x=1690, y=300)
    btn_M.place(x=1760, y=300)
    screen.mainloop()
    """
    # ограничения: 1) все нагрузки располагаются только в пределах длины балки
    # 2) не больше 6 нагрузок
    # 3) не больше 2 нагрузок одного вида
    # 4) значения должны быть только положительными
    """
