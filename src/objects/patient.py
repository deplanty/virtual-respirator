
class Pmus:
    """
    A respiratory effort.

    Args:
        pmus (int): maximum effort (cmH2O)
        period (float): time of a cycle (s)
        ti (float): inspiratory time (s)
    """

    def __init__(self, pmus, period, ti):
        # From patient
        self.pmus = pmus
        self.period = period
        self.ti = ti

        # Internal variables
        self.pmus_inc_percent = 0.7  # % of ti
        self.pmus_dec_percent = 1 - self.pmus_inc_percent  # % of ti
        self.pmus_inc_coeff = [0, 0, 0]
        self.pmus_dec_coeff = [0, 0, 0]

        self.compute_coefficients()


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
        if t <= self.ti * self.pmus_inc_percent:
            a, b, c = self.pmus_inc_coeff
            return a * t**2 + b * t + c
        # Decreasing Pmus
        elif t < self.ti:
            a, b, c = self.pmus_dec_coeff
            return a * t**2 + b * t + c
        # Expiration
        else:
            return 0


    def compute_coefficients(self):
        """
        Computes the coefficients of the effort equation from parameters.
        """

        pt_a = [0, 0]
        pt_a_ = [2 * self.ti * self.pmus_inc_percent, 0]
        pt_b = [self.ti * self.pmus_inc_percent, - self.pmus]
        pt_c = [self.ti * (self.pmus_inc_percent - self.pmus_dec_percent), 0]
        pt_c_ = [self.ti, 0]

        self.pmus_inc_coeff = self.get_coefficients(pt_a, pt_b, pt_a_)
        self.pmus_dec_coeff = self.get_coefficients(pt_c, pt_b, pt_c_)


    def get_coefficients(self, pt_a:list, pt_b:list, pt_c:list):
        """
        Returns the coefficients of a 2nd degree equation from 3 points.
        Equation : ax² + bx + c

        Args:
            pt_a (list): first point (x_1, y_1)
            pt_b (list): second point (x_2, y_2)
            pt_c (list): third point(x_3, y_3)

        Returns:
            list: a, b and c the 3 coefficients
        """

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
        self.ti = ti
        self.pmus = Pmus(pmus, 60/br, ti)
