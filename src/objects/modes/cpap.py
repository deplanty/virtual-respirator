from src.objects.modes import RespiMode


class CPAP(RespiMode):
    """
    Continuous Positive Airway Pressure

    Args:
        peep (int): positive end-expiratory pressure (cmH2O)
    """

    def __init__(self, peep:int):

        self.control = "pressure"
        self.peep = peep


    def get(self, t:float):
        """
        Returns the paramters at time t.

        Args:
            t (float): time of simulation (s)

        Returns:
            float: pressure
        """

        return self.peep


    def process_trigger(self, flow:float, t:float):
        pass
