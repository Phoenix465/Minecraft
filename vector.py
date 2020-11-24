"""
Handles For Vectors Types

Class
----
Vector2 - 2D Vector
Vector3 - 3D Vector
"""

from dataclasses import dataclass
from math import sqrt
from errors import VectorError


@dataclass()
class Vector2:
    """
    2D Vector

    Parameters
    ----------
    X : float
        X Pos of the Vector2

    Y : float
        Y Pos of the Vector2

    Attributes
    ----------
    _X : float
        Hidden X Pos

    _Y : float
        Hidden Y Pos

    _observers : list
        A list containing functions which are called when the pos's are updated

    list : list
        A List Version of the Vector

    tuple : tuple
        A Tuple Version of the Vector

    magnitude : tuple
        The Length of the Vector

    _unit : tuple
        The Tuple Form of the Normalised Vector
    """

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
        """
        To Bind Functions which update the Other Attributes

        Parameters
        ----------
        callback : function
            A Function Name Not being Called Yet

        Returns
        -------
        None
        """
        self._observers.append(callback)

    def operationHandler(self, other, operation):
        """
        Returns a New Vector Which is Adjusted

        Parameters
        ----------
        other : any
            The new type that is adjusted to the Vector2

        operation : str
            The str that is used for the function adjustment

        Returns
        -------
        Vector2
        """

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
    """
    3D Vector

    Parameters
    ----------
    X : float
        X Pos of the Vector3

    Y : float
        Y Pos of the Vector3

    Z : float
        Z Pos of the Vector3

    Attributes
    ----------
    _X : float
        Hidden X Pos

    _Y : float
        Hidden Y Pos

    _Z : float
        Hidden Z Pos

    _observers : list
        A list containing functions which are called when the pos's are updated

    list : list
        A List Version of the Vector

    tuple : tuple
        A Tuple Version of the Vector

    magnitude : tuple
        The Length of the Vector

    _unit : tuple
        The Tuple Form of the Normalised Vector
    """

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
        """
         To Bind Functions which update the Other Attributes

         Parameters
         ----------
         callback : function
             A Function Name Not being Called Yet

         Returns
         -------
         None
         """

        #print("Binding")
        self._observers.append(callback)

    def operationHandler(self, other, operation):
        """
        Returns a New Vector Which is Adjusted

        Parameters
        ----------
        other : any
            The new type that is adjusted to the Vector3

        operation : str
            The str that is used for the function adjustment

        Returns
        -------
        Vector3
        """

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
    
    def __key(self):
        return self.tuple

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.__key() == other.__key()
        return NotImplemented


if __name__ == "__main__":
    newVector = Vector3(5, 2, 8)
    print(newVector.magnitude)
    print(newVector)

    newVector.X = 10
    print(newVector.magnitude)
    print(newVector)
