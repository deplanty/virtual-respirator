
class Pmus:
    """
    A respiratory effort.

    Args:
        pmus (int): maximum effort (cmH2O)
        period (float): time of a cycle (s)
        ti (float): inspiratory time (s)
    """

    def __init__(self, pmus, period, ti):

        self.pmus = pmus
        self.period = period
        self.ti = ti

        self.pmus_inc = 0.7  # % of ti
        self.pmus_dec = 1 - self.pmus_inc  # % of ti


    def get(self, t:float):
        """
        Returns the effort at time t.

        Args:
            t (float): time of simulation (s)

        Returns:
            float: pmus value
        """

        # Current time in cycle
        t %= self.period

        # Increasing Pmus
        if t <= self.ti * self.pmus_inc:
            pt_a = [0, 0]
            pt_b = [self.ti * self.pmus_inc, - self.pmus]
            pt_a_ = [2 * self.ti * self.pmus_inc, 0]
            a, b, c = self.coefficient(pt_a, pt_b, pt_a_)
            return a * t**2 + b * t + c
        # Decreasing Pmus
        elif t < self.ti:
            pt_c = [self.ti * (self.pmus_inc - self.pmus_dec), 0]
            pt_b = [self.ti * self.pmus_inc, - self.pmus]
            pt_c_ = [self.ti, 0]
            a, b, c = self.coefficient(pt_c, pt_b, pt_c_)
            return a * t**2 + b * t + c
        # Expiration
        else:
            return 0


    def coefficient(self, pt_a:list, pt_b:list, pt_c:list):
        x_1, y_1 = pt_a
        x_2, y_2 = pt_b
        x_3, y_3 = pt_c

        a =   y_1 / ((x_1 - x_2) * (x_1 - x_3)) \
            + y_2 / ((x_2 - x_1) * (x_2 - x_3)) \
            + y_3 / ((x_3 - x_1) * (x_3 - x_2))

        b = - y_1 * (x_2 + x_3) / ((x_1 - x_2) * (x_1 - x_3)) \
            - y_2 * (x_1 + x_3) / ((x_2 - x_1) * (x_2 - x_3)) \
            - y_3 * (x_1 + x_2) / ((x_3 - x_1) * (x_3 - x_2))

        c =   y_1 * x_2 * x_3 / ((x_1 - x_2) *( x_1 - x_3)) \
            + y_2 * x_1 * x_3 / ((x_2 - x_1) * (x_2 - x_3)) \
            + y_3 * x_1 * x_2 / ((x_3 - x_1) * (x_3 - x_2))

        return a, b, c


class Patient:
    """
    A patient with his properties.

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
