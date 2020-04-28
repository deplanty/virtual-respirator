from src.objects.modes import RespiMode


class VSAI(RespiMode):
    """
    Respiratory mode : Ventilation Spontannée avec Aide Inspiratoire.

    Args:
        peep (int): positive end-expiratory pressure (cmH2O)
        ai (int): pressure support (cmH2O)
        ti (float): inpiratory time (s)
        trigger (float): inspiratory triggr (l/min)
    """

    def __init__(self, peep:int, ai:int, trigger_inspi:float, trigger_expi:float, ti_max:float):

        self.control = "pressure"
        self.peep = peep
        self.ai = ai
        self.ti_max = ti_max
        self.trigger_inspi = trigger_inspi / 60  # (l/s)
        self.trigger_expi = trigger_expi / 100  # %

        self.flow_max = 0
        self.t_start_inspi = 0  # (s)
        self.state = "expi"


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
            if t_cycle < self.ti_max:
                return self.ai
            else:
                self.state = "expi"
                return None
        else:
            return None


    def process_trigger(self, flow:float, t:float):
        """
        Detects if there is a new effort from the patient.
        And detects the ending of a n insufflation cycle.

        Args:
            flow (float): flow (l/min)
            t (float): time of simulation (s)
        """

        if self.state == "inspi":
            # Get flow peak
            if flow > self.flow_max:
                self.flow_max = flow
            # Get 25% of flow peak
            else:
                # TODO: Find a better way to end expi
                if flow <= self.trigger_expi * self.flow_max:
                    self.t_start_inspi = -float("inf")
                    self.state = "expi"

        elif self.state == "expi":
            if flow >= self.trigger_inspi:
                self.t_start_inspi = t
                self.flow_max = 0
                self.state = "inspi"
