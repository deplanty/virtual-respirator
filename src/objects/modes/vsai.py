
class VSAI:
    """
    Respiratory mode : Ventilation Volume Control.

    Args:
        peep (int): positive end-expiratory pressure (cmH2O)
        ai (int): pressure support (cmH2O)
        ti (float): inpiratory time (s)
        trigger (float): inspiratory triggr (l/min)
    """

    def __init__(self, peep:int, ai:int, ti:float, trigger:float):

        self.control = "pressure"
        self.peep = peep
        self.ai = ai
        self.ti = ti

        self.trigger = trigger / 60  # (l/s)

        self.t_start_inspi = 0  # (s)
        self.state = "inspi"


    def get(self, t:float):
        """
        Returns the paramters at time t.

        Args:
            t (float): time of simulation (s)

        Returns:
            float: paw
        """

        # Time from last inspi
        t_cycle = t - self.t_start_inspi

        if self.state == "inspi":
            if t_cycle < self.ti:
                return self.ai
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
