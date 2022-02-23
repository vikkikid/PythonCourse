import os
import numpy as np
import numbers


class MatrixOne:
    '''
    task one
    '''
    def __init__(self, x):
        self.x = []
        self.h = len(x[0])
        self.w = len(x)
        for row in x:
            if len(row) != self.h:
                raise Exception("Wrong matrices size")
            self.x.append(list(row))

    def __str__(self):
        return "[" + ",\n".join(str(i) for i in self.x) + "]"

    def __add__(self, other):
        if self.w != other.w or self.h != other.h:
            raise Exception("Wrong matrices size")
        output = [list(map(sum, zip(*w))) for w in zip(self.x, other.x)]
        return MatrixOne(output)

    def __mul__(self, other):
        if self.w != other.w or self.h != other.h:
            raise Exception("Wrong matrices size")
        output = [[i * j for i, j in zip(*w)] for w in zip(self.x, other.x)]
        return MatrixOne(output)

    def __matmul__(self, other):
        if self.h != other.w:
            raise Exception("Wrong matrices size")
        output = [[sum(i * j for i, j in zip(one, two))
                   for two in zip(*other.x)]
                  for one in self.x]
        return MatrixOne(output)


def save(x, filename):
    with open(filename, "w") as file:
        file.write(str(x))
        file.close()


class MixinShow:
    def __str__(self):
        return "[" + "\n".join(map(str, map(list, self.value))) + "]"


class MixinVal:
    def __init__(self, value):
        self.value = np.asarray(value)

    @property
    def data(self):
        return self.value

    @data.setter
    def data(self, new_value):
        self.value = new_value


class MixinSave:
    def write_to_file(self, file_name):
        with open(file_name, "w") as file:
            file.write(self.__str__())
            file.close()


class MatrixTwo(np.lib.mixins.NDArrayOperatorsMixin, MixinShow, MixinVal, MixinSave):
    '''
    task two

    more info: 
    https://numpy.org/doc/stable/reference/generated/numpy.lib.mixins.NDArrayOperatorsMixin.html?highlight=numpy%20ndarray
    '''
    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (MatrixTwo,)):
                return NotImplemented
            
        inputs = tuple(x.data if isinstance(x, MatrixTwo) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(x.data if isinstance(x, MatrixTwo) else x
                                  for x in out)
            
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        
        elif method == 'at':
            return None
        
        else:
            return type(self)(result)
        

class MixinHashing:
    def __hash__(self):
        return sum([sum(r) for r in self.x])


class MatrixThree(MatrixOne, MixinHashing):
    '''
    task 3
    '''
    _matmul_hashes = {}

    def __matmul__(self, other):
        key = (self.__hash__(), other.__hash__())
        
        if key in self._matmul_hashes:
            return self._matmul_hashes[key]
        
        matmul = MatrixThree(super().__matmul__(other).x)
        self._matmul_hashes[key] = matmul
        return matmul

    

if __name__ == '__main__':
    path = 'artifacts'
    easy = path + '/easy'
    medi = path + '/medium'
    hard = path + '/hard'
    os.makedirs(easy, exist_ok=True)
    os.makedirs(medi, exist_ok=True)
    os.makedirs(hard, exist_ok=True) 
    
    np.random.seed(0)
    # easy part
    m11 = MatrixOne(np.random.randint(0, 10, (10, 10)))
    m21 = MatrixOne(np.random.randint(0, 10, (10, 10)))
    save((m11 + m21).__str__(), f"{easy}/matrix+.txt")
    save((m11 * m21).__str__(), f"{easy}/matrix*.txt")
    save((m11 @ m21).__str__(), f"{easy}/matrix@.txt")
    
    np.random.seed(0)
    # medium part
    m12 = MatrixTwo(np.random.randint(0, 10, (10, 10)))
    m22 = MatrixTwo(np.random.randint(0, 10, (10, 10)))
    save((m12 + m22).__str__(), f"{medi}/matrix+.txt")
    save((m12 * m22).__str__(), f"{medi}/matrix*.txt")
    save((m12 @ m22).__str__(), f"{medi}/matrix@.txt")

    # hard part
    B = MatrixThree([[1, 3], [5, 4]])
    D = MatrixThree([[1, 3], [5, 4]])
    A = MatrixThree([[9, 2], [7, 3]])
    C = MatrixThree([[7, 5], [6, 8]])
    all_operations = [A, B, C, D, A @ B, C @ D]
    all_files = ["A.txt", "B.txt", "C.txt", "D.txt", "AB.txt", "CD.txt"]
    for m, n in zip(all_operations, all_files):
        save(m, f"{hard}/{n}")
        
    save(f"{hash(A @ B)}, {hash(C @ D)}", f"{hard}/hash.txt")   
    