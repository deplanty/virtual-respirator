

class Simulation:
    """
    A simulation with the settings

    Args:
        t_max (int): simulation duration
        t_step (float): step between 2 samples
    """

    def __init__(self, t_max:int, t_step:float):
        self.t_max = t_max
        self.t_step = t_step


    def get_dict(self):
        """
        Returns the simulation parameters as a dict.

        Returns:
            dict: simulation parameters
        """

        return {
            "t max": self.t_max,
            "t step": self.t_step
        }
