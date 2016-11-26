import re

pattern = r'(\d+):(\d+):(\d+)'


class Hour:
    def __init__(self, h, m, s):
        self.hour = h
        self.minute = m
        self.second = s
    
    def diference(self, hour2):
        self.second -= hour2.second
        self.minute -= hour2.minute
        self.hour -= hour2.hour

        if self.second < 0:
            self.second += 60
            self.minute -= 1            
        
        if self.minute < 0:
            self.minute += 60
            self.hour -= 1
        
        if self.hour < 0:
            self.second -= 60
            self.second *= -1
            self.minute += 1
            
            self.minute -= 60
            self.minute *= -1
            self.hour += 1

            self.hour *= -1

        return self

    def __str__(self):
        return '{0:02}:{1:02}:{2:02}'.format(self.hour, self.minute, self.second)


def diference(hour1, hour2):

    first = re.match(pattern, hour1)
    second = re.match(pattern, hour2)

    hora1 = Hour(int(first.group(1)), int(first.group(2)), int(first.group(3)))
    hora2 = Hour(int(second.group(1)), int(second.group(2)), int(second.group(3)))

    return str(hora1.diference(hora2))


