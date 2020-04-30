from src.objects.modes import RespiMode


class VPC(RespiMode):
    """
    Ventilation Pressure Control

    Args:
        peep (int): positive end-expiratory pressure (cmH2O)
        p_support (int): pressure support (cmH2O)
        ti (float): inpiratory time (s)
        br (int): breath rate (/min)
        trigger (float): inspiratory triggr (l/min)
    """

    def __init__(self, peep:int, p_support:int, ti:float, br:int, trigger:float):

        self.control = "pressure"
        self.peep = peep
        self.p_support = p_support
        self.ti = ti
        self.br = br  # (/min)

        self.trigger = trigger / 60  # (l/s)

        self.t_start_inspi = 0  # (s)
        self.state = "inspi"


    @property
    def period(self):
        """
        unit: s
        """

        return 60 / self.br


    def get(self, t):
        """
        Returns the paramters at time t.

        Args:
            t (float): time of simulation (s)

        Returns:
            float: paw
        """

        # Time from last inspi
        t_cycle = t - self.t_start_inspi

        if t_cycle >= self.period:
            self.state = "inspi"
            self.t_start_inspi = t
            t_cycle = 0

        if self.state == "inspi":
            if t_cycle < self.ti:
                return self.p_support
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
