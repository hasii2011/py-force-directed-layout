
from dataclasses import dataclass
from typing import List

NO_X_COORDINATE: int = 0
NO_Y_COORDINATE: int = 0


@dataclass
class Point:

    x: int = NO_X_COORDINATE
    y: int = NO_Y_COORDINATE

    def noCoordinates(self) -> bool:
        """

        Returns:  False if both coordinates are set to the invalid sentinel values
        """
        ans: bool = False
        if self.x == NO_X_COORDINATE and self.y == NO_Y_COORDINATE:
            ans = True

        return ans

    def __sub__(self, other) -> 'Point':

        newX: int = abs(self.x - other.x)
        newY: int = abs(self.y - other.y)

        return Point(x=newX, y=newY)

    @classmethod
    def deSerialize(cls, value: str) -> 'Point':

        point: Point = Point()

        xy: List[str] = value.split(sep=',')

        assert len(xy) == 2, 'Incorrectly formatted point'

        try:
            point.x = int(xy[0])
            point.y = int(xy[1])
        except ValueError as ve:
            print(f'Point - {ve}.')
            point.x = 0
            point.y = 0

        return point

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return self.__str__()
