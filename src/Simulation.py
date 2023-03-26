import math
import BershitS
import Moon


class Simulation:

    def _init_(self):
        self.bs = BershitS.Bershit()  # create a new instance of the Bershit class
        self.x = int(self.bs.location.x)  # get the x coordinate of the location
        self.y = int(self.bs.location.y)  # get the y coordinate of the location
        self.lastALT = 0.0
        self.lastHS = 0.0
        self.lastVS = 0.0
        self.loop()

    def loop(self) -> None:

        output_excel = self.bs.creating_excel()  # create an Excel file
        excel_index = 0

        self.lastALT = self.bs.alt
        self.lastHS = self.bs.hs

        dvs = self.bs.desired_vs(self.bs.alt)
        dhs = self.bs.desired_hs(self.bs.alt)

        moon_point_x = Moon.real_dest_point.x
        moon_point_y = Moon.real_dest_point.y

        while self.bs.alt > moon_point_y and self.bs.lat < moon_point_x:

            if self.bs.time % 10 == 0 or self.bs.alt < 100:
                ''' Writing the data to an Excel file'''
                output_excel.at[excel_index, 'TIME'] = self.bs.time
                output_excel.at[excel_index, 'NN'] = self.bs.NN
                output_excel.at[excel_index, 'VS'] = self.bs.vs
                output_excel.at[excel_index, 'DVS'] = dvs
                output_excel.at[excel_index, 'HS'] = self.bs.hs
                output_excel.at[excel_index, 'DHS'] = dhs
                output_excel.at[excel_index, 'DIST'] = self.bs.dist
                output_excel.at[excel_index, 'ALT'] = self.bs.alt
                output_excel.at[excel_index, 'ANG'] = self.bs.ang
                output_excel.at[excel_index, 'WEIGHT'] = self.bs.weight
                output_excel.at[excel_index, 'ACC - z'] = self.bs.acc
                output_excel.at[excel_index, 'FUEL'] = self.bs.fuel

                excel_index += 1

        output_excel.to_excel("Results.xlsx", index=False)  # save the Excel file


if _name_ == '_main_':
    Simulation()
