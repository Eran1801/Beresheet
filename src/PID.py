class PID:

    def _init_(self, P: float, I: float, D: float, max: int, min: int):
        """

        :param P: This variable determines the proportion of the error that should be applied to the output of the PID controller
        :param I: This variable determines how much past error should be accumulated and used to adjust the output of the PID controller.
        :param D: This variable determines how much the rate of change of the error should be used to adjust the output of the PID controller
        :param max: This variable sets the maximum output value that the controller can produce
        :param min: This variable sets the minimum output value that the controller can produce
        """
        self.P = P
        self.I = I
        self.D = D
        self.max = max
        self.min = min
        self.last_error = 0  # This variable holds the previous error value from the last iteration of the controller
        self.sum_integral = 0  # This variable holds the accumulated error over time

    def control(self, dt: float, error: float) -> float:
        self.sum_integral += self.I * error * dt
        difference = (error - self.last_error) / dt

        if self.sum_integral < self.min:
            const_integral = self.min
        elif self.sum_integral > self.max:
            const_integral = self.max
        else:
            const_integral = self.sum_integral

        output = self.P * error + self.D * difference + const_integral
        self.last_error = error
        return output 
