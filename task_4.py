from __future__ import annotations
from typing import Self, List, Union, Generator

class Village:
    """Class Village"""

    class Resident:
        """Basic class for an inhabitant"""

        def __init__(self: Self, name: str, beard_growth_time: float) -> None:
            """Creates a common inhabitant
            @param beard_growth_time Time until the next shave
            """
            self.__name: str = name
            self.__beard_growth_time: float = beard_growth_time
            self.__last_shave_time: float = 0  # Fixed: added double underscore

        def __str__(self: Self) -> str:
            """Returns the name of the inhabitant."""
            return self.__name

        def __repr__(self: Self) -> str:
            """Returns a string representation of the object.
            @return String representation of the object
            """
            return (
                f"{self.__class__.__module__}.{self.__class__.__qualname__}"
                f"({self.__name!r}, {self.__beard_growth_time!r})"
            )

        def _get_next_shave_time(self: Self) -> float:
            """Returns the time of the next shave.
            @return Time of the next shave
            """
            return self.__last_shave_time + self.__beard_growth_time

        def set_last_shave_time(self: Self, time: float) -> None:
            """Sets the time of the last shave.
            @param time Time of the last shave.
            """
            self.__last_shave_time = time

    class Barber(Resident):
        """Class Barber"""

        def __init__(self: Self, name: str, beard_growth_time: float, shave_time: float) -> None:
            """Creates a barber.
            @param beard_growth_time Time until the next shave
            @param shave_time Time for one shave
            """
            super().__init__(name, beard_growth_time)
            self.__shave_time: float = shave_time
            self.__busy_till: float = 0

        def busy_till(self: Self) -> float:
            return self.__busy_till

        def shave(self: Self, time: float, resident: Village.Resident) -> None:
            """Shaves an inhabitant.
            @param resident Inhabitant.
            """
            print(f"{time}: barber {self} shaves inhabitant {resident}.", end="")
            if resident is self:
                print(" Barber shaves himself!", end="")
            if time != resident._get_next_shave_time():
                print(" Barber is late for the shave!", end="")
            print()
            self.__busy_till = time + self.__shave_time
            resident.set_last_shave_time(self.__busy_till)

    def __init__(self: Self) -> None:
        """Creates a village."""
        self.residents: List[Village.Resident] = []

    def add_resident(self: Self, resident: Village.Resident) -> None:
        """Adds an inhabitant to the village.
        @param resident Inhabitant.
        """
        self.residents.append(resident)

    def get_next_shave(self: Self) -> Village.Resident:
        """Returns the inhabitant who should be shaved next.
        @returns Inhabitant who should be shaved next.
        """
        return min(self.residents, key=lambda x: x._get_next_shave_time())

    def get_next_free_barber(self: Self) -> Village.Barber:
        """Returns the barber who will be free next.
        @returns Barber who will be free next.
        """
        return min([r for r in self.residents if isinstance(r, Village.Barber)],
                   key=lambda x: x.busy_till())

    @staticmethod
    def __range(count: int) -> Generator[int, None, None]:
        i: int = 0
        while True:
            if count != -1 and i >= count: break
            yield i
            i += 1

    def run(self: Self, count: int = -1) -> None:
        """Starts the simulation for the given number of shaves.
        @param count Number of shaves.
        """
        try:
            for i in self.__range(count):
                resident = self.get_next_shave()
                barber = self.get_next_free_barber()
                time = max(resident._get_next_shave_time(), barber.busy_till())
                barber.shave(time, resident)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    village = Village()
    village.add_resident(Village.Resident(name="r1", beard_growth_time=2))
    village.add_resident(Village.Resident(name="r2", beard_growth_time=4))
    village.add_resident(Village.Barber(name="b1", beard_growth_time=6, shave_time=1))
    village.run(20)