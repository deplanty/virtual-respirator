
class Respirator:
    def __init__(self, file, mode, patient, t_max, t_step=0.02):
        self.file = file

        self.t = 0
        self.t_max = t_max
        self.t_step = t_step
        self.flow = 0
        self.volume = mode.peep * patient.c
        self.paw = mode.peep

        self.patient = patient
        self.mode = mode

        self.fid = None

    def __enter__(self):
        self.fid = open(self.file, "w")
        print("time", "paw", "flow", "volume", "pmus", sep="\t", file=self.fid)
        print(*self.as_array(), sep="\t", file=self.fid)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fid.close()
        self.fid = None

    @property
    def pmus(self):
        return self.patient.pmus.get(self.t)

    def next(self):
        """
        Computes the parameters for the time
        """

        # Volume control
        if self.mode.control == "flow":
            flow = self.mode.get(self.t)
            if flow is not None:
                self.flow = flow
            else:
                self.flow = (-self.pmus + self.mode.peep - (self.volume / self.patient.c)) / self.patient.r
                self.mode.process_trigger(self.flow, self.t)
            self.paw = self.pmus + self.patient.r * self.flow + self.volume / self.patient.c
        # Pressure control
        elif self.mode.control == "pressure":
            paw = self.mode.get(self.t)
            if paw is not None:
                self.paw = paw
            else:
                self.paw = self.mode.peep
                self.mode.process_trigger(self.flow, self.t)
            self.flow = (self.paw - self.pmus - (self.volume / self.patient.c)) / self.patient.r

        self.volume += self.flow * self.t_step

        if self.fid:
            self.write()

        array = self.as_array()
        self.t += self.t_step
        return array

    def write(self):
        print(
            self.t,
            self.paw,
            self.flow * 60,
            self.volume * 1000,
            self.pmus,
            sep="\t",
            file=self.fid
        )

    def as_array(self):
        """
        Returns the values as an array

        Returns:
            list: time, paw, flow, volume and pmus
        """

        return [self.t, self.paw, self.flow * 60, self.volume * 1000, self.pmus]

    def loop(self):
        """
        Generator
        """

        while self.t < self.t_max:
            yield self.next()
