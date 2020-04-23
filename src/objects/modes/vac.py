
class VAC:
    """
    Ventilation Volume Control

    Args:
        peep (int): positive end-expiratory pressure (cmH2O)
        vt (int): inpired volume (ml)
        flow (int): given flow (l/min)
        br (int): breath rate (/min)
        pause_inspi (float): end inspiratory pause (s)
        trigger (float): inspiratory triggr (l/min)
    """

    def __init__(self, peep:int, vt:int, flow:int, br:int, pause_inspi:float, trigger:float):

        self.control = "flow"
        self.peep = peep
        self.vt = vt / 1000  # (l)
        self.flow = flow / 60  # (l/s)
        self.br = br  # (/min)

        self.ti = self.vt / self.flow
        self.pause_inspi = pause_inspi

        self.trigger = trigger / 60  # (l/s)

        self.t_start_inspi = 0  # (s)
        self.state = "inspi"


    @property
    def period(self):
        return 60 / self.br


    def get(self, t:float):
        """
        Returns the paramters at time t.

        Args:
            t (float): time of simulation (s)

        Returns:
            float: flow
        """

        # Time from last inspi
        t_cycle = t - self.t_start_inspi

        if t_cycle >= self.period:
            self.state = "inspi"
            self.t_start_inspi = t
            t_cycle = 0

        if self.state == "inspi":
            if t_cycle < self.ti:
                return self.flow
            if t_cycle < self.ti + self.pause_inspi:
                return 0
            else:
                self.state = "expi"
                return None
        else:
            return None


    def process_trigger(self, flow:float, t:float):
        """
        Detects if there is a new effort from the patient.

        Args:
            flow (float): flow (l/min)
            t (float): time of simulation (s)
        """

        if self.state == "expi":
            if flow >= self.trigger:
                self.t_start_inspi = t
                self.state = "inspi"
