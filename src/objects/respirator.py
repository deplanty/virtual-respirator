from src.objects import Patient

from src.objects.modes import RespiMode


class Respirator:
    """
    A Respirator object.

    Args:
        patient (Patient): patient used
        mode (RespiMode): respiratory mode used
    """

    def __init__(self, patient:Patient, mode:RespiMode):
        self.t = 0
        self.flow = 0
        self.volume = mode.peep * patient.c
        self.paw = mode.peep

        self.patient = patient
        self.mode = mode


    @property
    def pmus(self):
        return self.patient.pmus.get(self.t)


    def next(self, t_step):
        """
        Computes the parameters for the current time.

        Args:
            t_step (float): time step

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
            self.paw = self.pmus + self.patient.r * self.flow + self.volume / self.patient.c
        # Pressure control
        elif self.mode.control == "pressure":
            paw = self.mode.get(self.t)
            if paw is not None:
                self.paw = paw
            else:
                self.paw = self.mode.peep
            self.flow = (self.paw - self.pmus - (self.volume / self.patient.c)) / self.patient.r
        # Volume
        self.volume += self.flow * t_step
        # Trigger
        self.mode.process_trigger(self.flow, self.t)

        # Next step
        array = self.get_array()
        self.t += t_step
        return array


    def get_array(self):
        """
        Returns the values as an array.

        Returns:
            list: time, paw, flow, volume and pmus
        """

        return [self.t, self.paw, self.flow * 60, self.volume * 1000, self.pmus]


    def get_header(self):
        """
        Returns the header and units of the returned values.

        Returns:
            list: Time, Paw, Flow, Volume and Pmus
        """

        return ["Temps (s)", "Paw (cmH2O)", "Débit (l/min)", "Volume (ml)", "Pmus (cmH2O)"]

    def loop(self, t_max:float, t_step:float=0.02):
        """
        Loop over the simulation as a generator.

        Args:
            t_max (float): duration of the simulation
            t_step (float): time step

        Returns:
            list: time, paw, flow volume and pmus
        """

        while self.t < t_max:
            yield self.next(t_step)
