class LogNone:

    def __init__(self):
        pass

    def write(self, msg):
        pass

    def write_line(self, msg):
        pass


class LogSegundo:

    def __init__(self):
        pass

    def write(self, msg):
        print str(msg)

    def write_line(self, msg):
        print str(msg)+"\n"


class ConsoleLog:

    def __init__(self):
        pass

    def write(self, msg):
        print str(msg)
        # pass

    def write_line(self, msg):
        print str(msg)+"\n"
        # pass
