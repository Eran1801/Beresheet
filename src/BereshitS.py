import pandas
import Moon
from Engines import Engines
from PID import PID
from Point import Point

class Bershit:
    def __init__(self):
        # ---- CONSTANTS ----
        self.WEIGHT_EMP = 165  # kg
        self.WEIGHT_FULE = 420  # kg
        self.WEIGHT_FULL = self.WEIGHT_EMP + self.WEIGHT_FULE  # kg
        self.MAIN_ENG_F = 430  # N
        self.SECOND_ENG_F = 25  # N
        self.MAIN_BURN = 0.15  # liter per sec, 12 liter per m'
        self.SECOND_BURN = 0.009  # liter per sec 0.6 liter per m'
        self.ALL_BURN = self.MAIN_BURN + 8 * self.SECOND_BURN

        # ---- VARIABLES ----
        self.vs = 24.8  # vertical speed
        self.hs = 932  # horizontal speed
        self.ang = 58.3  # angle
        self.alt = 13748  # 30 km
        self.lat = 0
        self.dist = (Point(self.lat, self.alt).distance(Moon.real_dest_point))  # distance from destination
        self.time = 0
        self.dt = 1
        self.acc = 0
        self.fuel = 121
        self.weight = self.WEIGHT_EMP + self.fuel

        self.pid = PID(0.7, 1, 0.01, 1, 0)
        self.NN = 0.7  # power gas, rate[0,1]

        self.location = Point(0, 0)

        engine_name = ['North1', 'North2', 'East1', 'East2', 'South1', 'South2', 'West1', 'West2']
        self.engines = [Engines(name, 0) for name in engine_name]

    def creating_excel(self) -> pandas.DataFrame:
        # Create an Excel file
        writer = pandas.ExcelWriter('../../Spacex1/Results.xlsx', engine='xlsxwriter')

        # Set the column names
        data = {'TIME': [], 'VS': [], 'HS': [], 'DIST': [], 'ALT': [], 'ANG': [], 'WEIGHT': [], 'ACC - z': [],
                'FUEL': []}

        # Convert the dataframe to an XlsxWriter Excel object.
        output_excel = pandas.DataFrame(data)
        output_excel.to_excel(writer, sheet_name='Sheet1', index=False)

        return output_excel

    def accMax(self, weight: float) -> float:
        return self.acc_fun(weight, 8)

    def acc_fun(self, weight: float, seconds: int) -> float:
        t = 0
        t += self.MAIN_ENG_F
        t += seconds * self.SECOND_ENG_F
        return t / weight
    
        def engine_power(self) -> float:
        """returns all engines power combined"""
        sum = 0
        for engine in self.engines:
            sum += engine.power
        return sum

    def update_engines(self):
        """update all engines power"""
        if self.alt < 2000 and self.ang > 0:
            for i in range(8):
                if i == 1 or i == 5:
                    self.engines[i].power = 0.5

                elif i == 6 or i == 7:
                    self.engines[i].power = 1

                else:
                    self.engines[i].power = 0

            self.ang -= self.engine_power() * self.dt

            if self.ang < 1:
                self.ang = 0

    def timer(self) -> None:
        """update time"""
        self.time += self.dt
        
        def location_update(self) -> None:
        self.alt = (self.alt - self.dt * self.vs)  # Y
        self.lat = (self.lat + self.dt * self.hs)  # X
        self.dist = (Point(self.lat, self.alt).distance(Moon.real_dest_point))

    def speed_control(self, h_acc: float, v_acc):
        if self.hs > 0:
            self.hs = 0.1 if self.hs - h_acc * self.dt < 0 else self.hs - h_acc * self.dt

        if self.hs < 2 and self.alt <= 2000:
            self.hs = 0

        self.vs = 0.4 if self.vs - v_acc * self.dt < 2 else self.vs - v_acc * self.dt

        if self.alt < 15 and self.vs > 2:
            self.vs = 0.3 if self.vs - 2 < 2 else self.vs - 2

    def fuel_control(self) -> None:
        diff_in_weight = self.dt * self.ALL_BURN * self.NN  # difference in weight

        if self.fuel > 0:
            self.fuel -= diff_in_weight  # update fuel
            self.weight = self.WEIGHT_EMP + self.fuel  # update weight
            self.acc = self.NN * self.accMax(self.weight)  # update acceleration
        else:
            self.acc = 0
            
    def constraint(self, x: float) -> float:
        x = 1 if x > 1 else x
        return 0 if x < 0 else x

    def NNControl(self):
        if self.alt > 2000:  # 2KM
            if self.vs > 25:
                self.NN = self.constraint(self.NN + 0.003 * self.dt)

            if self.vs < 20:
                self.NN = self.constraint(self.NN - 0.003 * self.dt)

        else:
            self.NN = self.constraint(self.pid.control(self.dt, 0.5 - self.NN))

            if self.alt < 5:
                self.NN = 0.4

            if self.alt < 4:
                self.NN = 0

            elif self.alt < 125:
                self.NN = 1

                if self.vs < 5:
                    self.NN = 0.7
    def desired_hs(self, alt: float) -> float:
        min_alt = 2000  # 2KM
        max_alt = 30000  # 30KM

        if alt < min_alt:
            return 0

        if alt > max_alt:
            return Moon.EQ_SPEED

        norm = (alt - min_alt) / (max_alt - min_alt)  # normalize
        norm = math.pow(norm, 0.70)
        return norm * Moon.EQ_SPEED

    def desired_vs(self, alt: float) -> float:
        max_alt = 30000  # 30KM

        if alt > max_alt:
            return 0

        if alt > 1000:
            return 23

        if alt > 500:
            return 13 + 10 * (alt - 500) / 500

        if alt > 70:
            return 5 + 8 * (alt - 70) / 430
    



