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
