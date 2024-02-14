
from dataclasses import dataclass

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
