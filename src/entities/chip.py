from loguru import logger
class Chip[T]:
    """
    Chip object.
    Supports __add__ (__radd__), __eq__, getting amount with get_amount() method.
    """

    def __init__(self, amount: int):
        self.amount = int(amount)

    def __add__(self, other: T):
        """
        Add Chip as a left operand
        """
        if not isinstance(other, (Chip, int)):
            logger.error("Tried to add Chip to incompatible type")
            return NotImplemented

        amount = self.amount
        if isinstance(other, int):
            amount += int(other)
        else:
            amount += int(other.amount)

        return Chip(amount)

    def __radd__(self, other: T) -> T:
        """
        Add Chip as a right operand
        """
        return self.__add__(other)

    def __eq__(self, other: T | int):
        if not isinstance(other, (Chip, int)):
            logger.error("Tried to compare Chip to incompatible type")
            return NotImplemented

        if isinstance(other, int):
            return self.amount == other
        else:
            return self.amount == other.amount


    def get_amount(self):
        return self.amount
