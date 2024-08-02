import math
import operator

from typing import Literal, Tuple, TypeVar

from CosyTrafo import (
    cartesian_to_spherical, spherical_to_cartesian,
    cartesian_to_cylindrical, cylindrical_to_cartesian,
    cylindrical_to_spherical, spherical_to_cylindrical,
)

# define custom type
AnyVector = TypeVar("AnyVector", bound="Vector")


class Vector:
    def __init__(
            self,
            a: float,
            b: float,
            c: float,
            csys: Literal["cartesian", "cylindrical", "spherical"]
    ) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.csys = csys

    def __repr__(self) -> str:
        return f"Vector({self.a}, {self.b}, {self.c}, csys={self.csys})"

    def to_cartesian(self) -> Tuple[float, float, float]:
        if self.csys == "cartesian":
            return self.a, self.b, self.c
        elif self.csys == "cylindrical":
            return cylindrical_to_cartesian(self.a, self.b, self.c)
        elif self.csys == "spherical":
            return spherical_to_cartesian(self.a, self.b, self.c)

    def to_spherical(self) -> Tuple[float, float, float]:
        if self.csys == "cartesian":
            return cartesian_to_spherical(self.a, self.b, self.c)
        elif self.csys == "cylindrical":
            return cylindrical_to_spherical(self.a, self.b, self.c)
        elif self.csys == "spherical":
            return self.a, self.b, self.c

    def to_cylindrical(self) -> Tuple[float, float, float]:
        if self.csys == "cartesian":
            return cartesian_to_cylindrical(self.a, self.b, self.c)
        elif self.csys == "cylindrical":
            return self.a, self.b, self.c
        elif self.csys == "spherical":
            return cylindrical_to_spherical(self.a, self.b, self.c)

    def __operate(self, other: AnyVector, op) -> AnyVector:
        a, b, c = [
            getattr(operator, op)(x, y)
            for x, y in zip(self.to_cartesian(), other.to_cartesian())
        ]
        return Vector(a, b, c, "cartesian")

    def __add__(self, other: AnyVector) -> AnyVector:
        return self.__operate(other, "add")

    def __sub__(self, other: AnyVector) -> AnyVector:
        return self.__operate(other, "sub")

    def __mul__(self, other: AnyVector) -> AnyVector:
        return self.__operate(other, "mul")

    def __truediv__(self, other: AnyVector) -> AnyVector:
        return self.__operate(other, "truediv")


if __name__ == "__main__":
    vec1 = Vector(1, 2, 3, "cartesian")
    vec2 = Vector(4, 5, 6, "cartesian")

    print(vec1 + vec2)
    print(vec1 - vec2)
    print(vec1 * vec2)
    print(vec1 / vec2)
