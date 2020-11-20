from dataclasses import dataclass
from math import sqrt
from errors import *


@dataclass()
class Vector2:
    def __init__(self, X, Y):
        if type(X) != int and type(X) != float:
            raise VectorError("X Has To Be Of Class int/float")
        if type(Y) != int and type(Y) != float:
            raise VectorError("Y Has To Be Of Class int/float")

        self._X = X
        self._Y = Y

        self._observers = []

        self.list = [self.X, self.Y]
        self.tuple = tuple(self.list)

        self.magnitude = sqrt(sum(map(lambda num: num**2, self.list)))
        self._unit = tuple(map(lambda num: num / self.magnitude, self.list)) if self.magnitude != 0 else tuple([0, 0])

        self.bindTo(self.updateList)
        self.bindTo(self.updateUnit)
        self.bindTo(self.updateMagnitude)
        self.bindTo(self.updateTuple)

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def unit(self):
        return Vector2(*self._unit)

    @X.setter
    def X(self, newVal):
        self._X = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._X)

    @Y.setter
    def Y(self, newVal):
        self._Y = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._Y)

    def bindTo(self, callback):
        #print("Binding")
        self._observers.append(callback)

    def operationHandler(self, other, operation):
        functionDict = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

        operationText = {
            "+": ["Added", "Addition"],
            "-": ["Subtracted", "Subtraction"],
            "*": ["Multiplied", "Multiplication"],
            "/": ["Divided", "Division"],
        }

        endVector = Vector2(0, 0)
        if type(other) == int or type(other) == float:
            endVector.X = functionDict[operation](self.X, other)
            endVector.Y = functionDict[operation](self.Y, other)

        elif type(other) == Vector2:
            endVector.X = functionDict[operation](self.X, other.X)
            endVector.Y = functionDict[operation](self.Y, other.Y)

        elif type(other) == list or type(other) == tuple:
            if len(other) == 2:
                endVector.X = functionDict[operation](self.X, other[0])
                endVector.Y = functionDict[operation](self.Y, other[1])
            else:
                raise VectorError(f"List/Tuple Being {operationText[operation][0]} Needs To Have Length 2")

        else:
            raise VectorError(f"{type(other)} Is Not Supported For Vector {operationText[operation][1]}")

        return endVector

    def __add__(self, other):
        return self.operationHandler(other, "+")

    def __sub__(self, other):
        return self.operationHandler(other, "-")

    def __mul__(self, other):
        return self.operationHandler(other, "*")

    def __truediv__(self, other):
        return self.operationHandler(other, "/")

    def __repr__(self):
        return f"Vector2 X:{self.X} Y:{self.Y}"

    def updateList(self,  *args):
        self.list = [self.X, self.Y]

    def updateTuple(self, *args):
        self.tuple = tuple(self.list)

    def updateMagnitude(self, *args):
        self.magnitude = sqrt(sum(map(lambda num: num**2, self.list)))

    def updateUnit(self, *args):
        self._unit = tuple(map(lambda num: num / self.magnitude, self.list)) if self.magnitude != 0 else tuple([0, 0])


@dataclass()
class Vector3(object):
    def __init__(self, X, Y, Z):
        if type(X) != int and type(X) != float:
            raise VectorError("X Has To Be Of Class int/float")
        if type(Y) != int and type(Y) != float:
            raise VectorError("Y Has To Be Of Class int/float")
        if type(Z) != int and type(Z) != float:
            raise VectorError("Z Has To Be Of Class int/float")

        self._X = X
        self._Y = Y
        self._Z = Z

        self._observers = []

        self.list = [self.X, self.Y, self.Z]
        self.tuple = tuple(self.list)

        self.magnitude = sqrt(sum(map(lambda num: num**2, self.list)))
        self._unit = tuple(map(lambda num: num / self.magnitude, self.list)) if self.magnitude != 0 else tuple([0, 0, 0])

        self.bindTo(self.updateList)
        self.bindTo(self.updateUnit)
        self.bindTo(self.updateMagnitude)
        self.bindTo(self.updateTuple)

    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def Z(self):
        return self._Z

    @property
    def unit(self):
        return Vector3(*self._unit)

    @X.setter
    def X(self, newVal):
        self._X = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._X)

    @Y.setter
    def Y(self, newVal):
        self._Y = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._Y)

    @Z.setter
    def Z(self, newVal):
        self._Z = newVal

        for callback in self._observers:
            #print("Changed")
            callback(self._Z)

    def bindTo(self, callback):
        #print("Binding")
        self._observers.append(callback)

    def operationHandler(self, other, operation):
        functionDict = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }

        operationText = {
            "+": ["Added", "Addition"],
            "-": ["Subtracted", "Subtraction"],
            "*": ["Multiplied", "Multiplication"],
            "/": ["Divided", "Division"],
        }

        endVector = Vector3(0, 0, 0)
        if type(other) == int or type(other) == float:
            endVector.X = functionDict[operation](self.X, other)
            endVector.Y = functionDict[operation](self.Y, other)
            endVector.Z = functionDict[operation](self.Z, other)

        elif type(other) == Vector3:
            endVector.X = functionDict[operation](self.X, other.X)
            endVector.Y = functionDict[operation](self.Y, other.Y)
            endVector.Z = functionDict[operation](self.Z, other.Z)

        elif type(other) == list or type(other) == tuple:
            if len(other) == 3:
                endVector.X = functionDict[operation](self.X, other[0])
                endVector.Y = functionDict[operation](self.Y, other[1])
                endVector.Z = functionDict[operation](self.Z, other[2])
            else:
                raise VectorError(f"List/Tuple Being {operationText[operation][0]} Needs To Have Length 3")

        else:
            raise VectorError(f"{type(other)} Is Not Supported For Vector {operationText[operation][1]}")

        return endVector

    def __add__(self, other):
        return self.operationHandler(other, "+")

    def __sub__(self, other):
        return self.operationHandler(other, "-")

    def __mul__(self, other):
        return self.operationHandler(other, "*")

    def __truediv__(self, other):
        return self.operationHandler(other, "/")

    def __repr__(self):
        return f"Vector3 X:{self.X} Y:{self.Y} Z:{self.Z}"

    def updateList(self,  *args):
        self.list = [self.X, self.Y, self.Z]

    def updateTuple(self, *args):
        self.tuple = tuple(self.list)

    def updateMagnitude(self, *args):
        self.magnitude = sqrt(sum(map(lambda num: num**2, self.list)))

    def updateUnit(self, *args):
        self._unit = tuple(map(lambda num: num / self.magnitude, self.list)) if self.magnitude != 0 else tuple([0, 0, 0])


if __name__ == "__main__":
    newVector = Vector3(5, 2, 8)
    print(newVector.magnitude)
    print(newVector)

    newVector.X = 10
    print(newVector.magnitude)
    print(newVector)
