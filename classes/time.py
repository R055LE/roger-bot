class Time():
    def __init__(self, time_dict):
        if time_dict.get('zone', 0) in range(1, 5):
            self.__apply_zone(time_dict)
        self.second = time_dict.get('second', 0)
        self.minute = time_dict.get('minute', 0)
        self.hour = time_dict.get('hour', 0)
        self.day = time_dict.get('day', 0)
        self.offset = time_dict.get('offset', 0)
        self.name = time_dict.get('name', 0)
        self.__apply_offset()

    def __str__(self):
        return f"<{self.name} {self.second} {self.minute} {self.hour} {self.day}>"

    def __repr__(self):
        return f"{self.name}"

    def __apply_offset(self):
        if type(self.minute) is not str:
            self.minute -= self.offset
            if type(self.hour) is not str and self.minute < 0:
                self.minute += 60
                self.hour -= 1
                if type(self.day) is not str and self.hour < 0:
                    self.hour += 24
                    self.day -= 1
                    if self.day < 0:
                        self.day += 7
        return self

    def __apply_zone(self, time_dict):
        self.zone = time_dict.get('zone')
