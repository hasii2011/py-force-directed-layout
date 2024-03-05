
from wx import DC

from pyforcedirectedlayout.Node import Node
from pyforcedirectedlayout.Point import Point
from pyforcedirectedlayout.Size import Size


class FakeNode(Node):

    def __init__(self, location: Point, fakeId: int = 0):
        super().__init__()
        self.location = location
        self._id: int = fakeId

    @property
    def fakeId(self) -> int:
        return self._id

    @property
    def size(self) -> Size:
        return Size(12, 12)

    def drawNode(self, dc: DC):
        pass

    def __str__(self) -> str:
        return f'FakeNode: id: {self._id} - {self.location}'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:

        ans: bool = False
        if self.fakeId == other.fakeId:
            ans = True

        return ans
