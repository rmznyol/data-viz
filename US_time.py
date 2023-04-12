class ComputeUSTime:
    def __init__(self, time):
        self.time = time
    
    def compute_US_time(self):
        """
        compute_US_time(time): returns the time in US time (am/pm)

        Parameters:
        -----------
        self:
            Instance of class which has the class attribute time

        Returns:
        --------
        US_time: str
            String of  self.time in US time (am/pm)

        Example:
        --------
        time = 14
        compute_US_time(time) = '2pm'
        """

        if self.time == 0:
            US_time = '12am'
        elif 0 < self.time < 12:
            US_time = '{}am'.format(self.time)
        elif self.time == 12:
            US_time = "{}pm".format(self.time)
        elif 12 < self.time <= 23:
            US_time = "{}pm".format(self.time%12)

        return US_time