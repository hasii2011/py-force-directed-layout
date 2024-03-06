
from enum import Enum

from wx import Colour
from wx import ColourDatabase


class DemoColorEnum(Enum):
    """
    Custom colors came from:
        https://www.rapidtables.com/web/color/RGB_Color.html
    """

    BLACK             = 'Black'
    CORNFLOWER_BLUE   = 'Cornflower Blue'
    WHITE             = 'White'
    LIGHT_GREY        = 'Light Grey'
    DARK_GREY         = 'Dark Grey'
    SKY_BLUE          = 'Sky Blue'
    DIM_GREY          = 'Dim Grey'
    GREEN             = 'Green'
    MEDIUM_BLUE       = 'Medium Blue'
    MIDNIGHT_BLUE     = 'Midnight Blue'
    LIGHT_BLUE        = 'Light Blue'
    LIGHT_STEEL_BLUE  = 'Light Steel Blue'
    ALICE_BLUE        = 'Alice Blue'
    DARK_SLATE_BLUE   = 'Dark Slate Blue'
    MEDIUM_SLATE_BLUE = 'Medium Slate Blue'
    YELLOW            = 'Yellow'
    SALMON            = 'Salmon'
    GAINSBORO         = 'Gainsboro'
    LIGHT_YELLOW      = 'Light Yellow'
    MINT_CREAM        = 'Mint Cream'

    @classmethod
    def toWxColor(cls, colorEnum: 'DemoColorEnum') -> Colour:
        cdb: ColourDatabase = ColourDatabase()

        cdb.AddColour(DemoColorEnum.ALICE_BLUE.value, Colour(240, 248, 255))
        cdb.AddColour(DemoColorEnum.GAINSBORO.value, Colour(218, 218, 218))
        cdb.AddColour(DemoColorEnum.LIGHT_YELLOW.value, Colour(255, 255, 224))
        cdb.AddColour(DemoColorEnum.MINT_CREAM.value, Colour(245, 255, 250))

        c: Colour = cdb.Find(colorEnum.value)
        if c.IsOk() is False:
            c = cdb.Find(DemoColorEnum.BLACK.value)
            print('Cannot find color use default')

        return c
