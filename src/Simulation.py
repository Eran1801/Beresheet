import math
import BershitS
import Moon

class Simulation:

    def __init__(self):
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

        moon_point_x = Moon.real_dest_point.x
        moon_point_y = Moon.real_dest_point.y

        while self.bs.alt > moon_point_y and self.bs.lat < moon_point_x:

            if self.bs.time % 10 == 0 or self.bs.alt < 100:
                ''' Writing the data to an Excel file'''
                output_excel.at[excel_index, 'TIME'] = self.bs.time
                output_excel.at[excel_index, 'VS'] = self.bs.vs
                output_excel.at[excel_index, 'HS'] = self.bs.hs
                output_excel.at[excel_index, 'DIST'] = self.bs.dist
                output_excel.at[excel_index, 'ALT'] = self.bs.alt
                output_excel.at[excel_index, 'ANG'] = self.bs.ang
                output_excel.at[excel_index, 'WEIGHT'] = self.bs.weight
                output_excel.at[excel_index, 'ACC - z'] = self.bs.acc
                output_excel.at[excel_index, 'FUEL'] = self.bs.fuel

                excel_index += 1

            self.bs.NNControl()  # Update the NN value according to the 'vs' and the 'alt' variables
            self.bs.update_engines()  # Update the 8 small engines according to the 'alt' and the 'ang' variables

            ang_rad = math.radians(self.bs.ang)  # Convert the angle to radians
            h_acc = math.sin(ang_rad) * self.bs.acc  # Calculate the horizontal acceleration
            v_acc = math.cos(ang_rad) * self.bs.acc  # Calculate the vertical acceleration
            vacc = Moon.getAcc(self.bs.hs)  # Calculate the vertical acceleration of the moon

            self.bs.timer()  # Update the time
            self.bs.fuel_control()
            v_acc -= vacc  # Calculate the vertical acceleration of the moon
            self.bs.speed_control(h_acc,
                                  v_acc)  # Update the speed according to the horizontal and vertical acceleration
            self.bs.location_update()

        output_excel.to_excel("Results.xlsx", index=False)  # save the Excel file


if __name__ == '__main__':
    Simulation()
    print('hey')