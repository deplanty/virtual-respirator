
class Pmus:
    """
    A respiratory effort

    Args:
        pmus (int): maximum effort (cmH2O)
        period (float): time of a cycle (s)
        ti (float): inspiratory time (s)
    """

    def __init__(self, pmus, period, ti):

        self.pmus = pmus
        self.period = period
        self.ti = ti

    def get(self, t):
        """
        Return the effort at time t

        Args:
            t (float): time of simulation (s)

        Returns:
            float: pmus value
        """

        t %= self.period

        if t <= self.ti * 0.6:
            a = -self.pmus/(self.ti * 0.6)
            return a * t
        elif t < self.ti:
            a = self.pmus/(self.ti * 0.4)
            b = -a * self.ti
            return a * t + b
        else:
            return 0


class Patient:
    """
    A patient with his properties

    Args:
        r (int): airway resistances (cmH2O/(l/s))
        c (int): pulmonary compliance (ml/cmH2O)
        br (int): breath rate (/min)
        ti (float): inspiratory time (s)
        pmus (int): muscular pressure (cmH2O)
    """

    def __init__(self, r, c, br, ti, pmus):

        self.r = r  # (cmH2O/(l/s))
        self.c = c / 1000  # (l/cmH2O)
        self.br = br
        self.pmus = Pmus(pmus, 60/br, ti)
