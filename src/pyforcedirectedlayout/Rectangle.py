
from logging import Logger
from logging import getLogger


class Rectangle:
    """
    This class minimally emulates .Net `System.Drawing.Rectangle`

    https://learn.microsoft.com/en-us/dotnet/api/system.drawing.rectangle.-ctor?view=net-8.0

    Stores a set of four integers that represent the location and size of a rectangle.

    """
    def __init__(self, x: int, y: int, width: int, height: int):
        """
        Initializes a new instance of the Rectangle class with the specified location and size.

        Args:
            x:      The x-coordinate of the upper-left corner of the rectangle.
            y:      The y-coordinate of the upper-left corner of the rectangle.
            width:  The width of the rectangle.
            height: The height of the rectangle.
        """

        self.logger: Logger = getLogger(__name__)

        self._x: int = x
        self._y: int = y

        self._width:  int = width
        self._height: int = height

    @property
    def x(self) -> int:
        """
        Returns:  The x-coordinate of the upper-left corner of this Rectangle structure.
        """
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self) -> int:
        """
        Returns: The y-coordinate of the upper-left corner of this Rectangle structure.
        """
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def width(self) -> int:
        """
        Returns: The width of this Rectangle structure.
        """
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self) -> int:
        """
        Returns: The height of this Rectangle structure.
        """
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @classmethod
    def FromLTRB(cls, left: int, top: int, right: int, bottom: int) -> 'Rectangle':
        """

        Args:
            left:   The x-coordinate of the upper-left corner of this Rectangle structure.
            top:    The y-coordinate of the upper-left corner of this Rectangle structure.
            right:  The x-coordinate of the lower-right corner of this Rectangle structure.
            bottom: The y-coordinate of the lower-right corner of this Rectangle structure.

        Returns:
        """

        width:  int = right - left
        height: int = bottom - top

        return Rectangle(x=left, y=top, width=width, height=height)

    def __eq__(self, other) -> bool:
        """

        Args:
            other:

        Returns:  True if the defined rectangles are 'functionally' equal
        """
        ans: bool = False

        if isinstance(other, Rectangle) is False:
            pass
        else:
            if self.x == other.x and self.y == other.y and self.width == other.width and self.height == other.height:
                ans = True

        return ans

    def __str__(self) -> str:

        rendering: str = (
            f'x: {self._x} '
            f'y: {self._y} '
            f'width: {self._width} '
            f'height: {self._height}'
        )

        return rendering

    def __repr__(self) -> str:
        return self.__str__()
