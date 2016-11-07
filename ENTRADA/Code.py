class Code:

    def __init__(self, groups):
        self.groups = groups
        self.byte_array = Code.get_byte_array(groups)

    @staticmethod
    def get_byte_array(groups):
        return [groups]
