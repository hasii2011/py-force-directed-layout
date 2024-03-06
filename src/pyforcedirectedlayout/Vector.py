
from logging import Logger
from logging import getLogger

from math import atan2
from math import cos
from math import isclose
from math import pi
from math import sin
from math import sqrt

from pyforcedirectedlayout.Point import Point

PI_180: float = pi / 180.0


class Vector:
    RELATIVE_TOLERANCE: float = 0.01

    """
    Represents a vector whose magnitude and direction are both expressed as a float

    Automatically simplifies the representation to ensure a positive magnitude and a sub-circular angle.
    
    Vector addition and scalar multiplication are supported.
    """
    def __init__(self, magnitude: float, direction: float):

        self.logger: Logger = getLogger(__name__)

        self._magnitude: float = magnitude
        self._direction: float = direction

        # resolve negative magnitude by reversing direction
        if self._magnitude < 0:
            self._magnitude = -self._magnitude
            self._direction = (180.0 + self._direction) % 360

        # resolve negative direction
        if self._direction < 0:
            self._direction = (360.0 + self._direction)

    @property
    def magnitude(self) -> float:
        return self._magnitude

    @magnitude.setter
    def magnitude(self, magnitude: float):
        self._magnitude = magnitude

    @property
    def direction(self) -> float:
        return self._direction

    @direction.setter
    def direction(self, direction: float):
        self._direction = direction

    def toPoint(self):
        """
        Converts the vector into an X-Y coordinate representation.

        Returns:
        """
        x: float = self._magnitude * cos((pi / 180.0) * self._direction)
        y: float = self._magnitude * sin((pi / 180.0) * self._direction)

        return Point(x=int(x), y=int(y))

    def __add__(self, other: 'Vector') -> 'Vector':
        """
        Calculates the resultant sum of two vectors.
        Args:
            other:

        Returns:  The result of vector addition
        """
        #
        # break into x-y placeholder
        # a is self and other is b
        #
        aX: float = self.magnitude * cos(PI_180 * self.direction)
        aY: float = self.magnitude * sin(PI_180 * self.direction)

        bX: float = other.magnitude * cos(PI_180 * other.direction)
        bY: float = other.magnitude * sin(PI_180 * other.direction)

        # add x-y components
        aX += bX
        aY += bY
        # Pythagorean' theorem to get resultant magnitude
        # double magnitude = Math.Sqrt(Math.Pow(aX, 2) + Math.Pow(aY, 2));
        magnitude: float = sqrt(pow(aX, 2) + pow(aY, 2))

        # calculate direction using inverse tangent
        if isclose(magnitude, 0.0, rel_tol=Vector.RELATIVE_TOLERANCE):
            self.logger.info(f'magnitude was zero')
            direction: float = 0.0
        else:
            direction = (180.0 / pi) * atan2(aY, aX)

        return Vector(magnitude=magnitude, direction=direction)

    def __mul__(self, other) -> 'Vector':
        """
        Only magnitude is affected by scalar multiplication

        In the C# version other was a scalar value.  In this
        version it has to be a Vector with the 'magnitude' value set to the
        appropriate value

        Args:
            other:

        Returns:  A Vector whose magnitude has been multiplied by other.magnitude
        """
        return Vector(magnitude=self.magnitude * other.magnitude, direction=self._direction)

    def __eq__(self, other) -> bool:
        """
        Args:
            other:

        Returns:   True if both the magnitude and direction are equal,
        """
        ans: bool = False
        if isinstance(other, Vector):
            if isclose(self.magnitude, other.magnitude, rel_tol=Vector.RELATIVE_TOLERANCE) and isclose(self.direction, other.direction, rel_tol=Vector.RELATIVE_TOLERANCE):
                ans = True

        return ans

    def __str(self) -> str:
        """

        return mMagnitude.ToString("N5") + " " + mDirection.ToString("N2") + "°";

        Returns:   A string representation of the vector.
        """
        return f'magnitude: {self._magnitude:.5f} direction: {self._direction:.2f}°'

    def __repr__(self) -> str:
        return self.__str()
