
class ArrayTools:
    def __init__(self):
        pass

    @staticmethod
    def sub_array(lista, start, size, step=1):
        novalista = []
        for i in range(start, start + size, step):
            novalista.append(lista[i])

        return novalista

    @staticmethod
    def append_array(src, dest, offset, size):
        if offset + size > len(dest):
            raise Exception("Array out of bounds")
        i = 0
        while i < size:
            dest[offset+i] = src[i]
            i += 1
