from src.objects import Patient

from src.objects.modes import RespiMode


class Respirator:
    """
    A Respirator object.

    Args:
        patient (Patient): patient used
        mode (RespiMode): respiratory mode used
        t_max (float): duration of the simulation
        t_step (float): step between two time values
    """

    def __init__(self, patient:Patient, mode:RespiMode, t_max:float, t_step:float=0.02):
        self.t = 0
        self.t_max = t_max
        self.t_step = t_step
        self.flow = 0
        self.volume = mode.peep * patient.c
        self.paw = mode.peep

        self.patient = patient
        self.mode = mode


    @property
    def pmus(self):
        return self.patient.pmus.get(self.t)


    def next(self):
        """
        Computes the parameters for the current time.

        Returns:
            list: time, paw, flow, volume and pmus
        """

        # Volume control
        if self.mode.control == "flow":
            flow = self.mode.get(self.t)
            if flow is not None:
                self.flow = flow
            else:
                self.flow = (-self.pmus + self.mode.peep - (self.volume / self.patient.c)) / self.patient.r
                self.mode.process_trigger(self.flow, self.t)
            self.paw = self.pmus + self.patient.r * self.flow + self.volume / self.patient.c
        # Pressure control
        elif self.mode.control == "pressure":
            paw = self.mode.get(self.t)
            if paw is not None:
                self.paw = paw
            else:
                self.paw = self.mode.peep
                self.mode.process_trigger(self.flow, self.t)
            self.flow = (self.paw - self.pmus - (self.volume / self.patient.c)) / self.patient.r
        # Volume
        self.volume += self.flow * self.t_step

        # Next step
        array = self.as_array()
        self.t += self.t_step
        return array


    def as_array(self):
        """
        Returns the values as an array.

        Returns:
            list: time, paw, flow, volume and pmus
        """

        return [self.t, self.paw, self.flow * 60, self.volume * 1000, self.pmus]


    def loop(self):
        """
        Loop over the simulation as a generator.

        Returns:
            list: time, paw, flow volume and pmus
        """

        while self.t < self.t_max:
            yield self.next()
