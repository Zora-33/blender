import math
import operator

from typing import Literal, Tuple, TypeVar, Iterator

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

    def __iter__(self) -> Iterator[float]:
        return iter((self.a, self.b, self.c))

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

    def dot(self, other: AnyVector) -> float:
        """calculates the scalar product or dot product between two vectors"""
        return sum(self * other)

    def cross(self, other: AnyVector) -> AnyVector:
        """calculates the cross product between two vectors"""
        a1, b1, c1 = self.to_cartesian()
        a2, b2, c2 = other.to_cartesian()

        return Vector(
            b1 * c2 - c1 * b2,
            c1 * a2 - a1 * c2,
            a1 * b2 - b1 * a2,
            csys="cartesian"
        )


if __name__ == "__main__":
    vec1 = Vector(1, 2, 3, "cartesian")
    vec2 = Vector(4, 5, 6, "cartesian")

    print(f"Add: {vec1 + vec2}")
    print(f"Subtract: {vec1 - vec2}")
    print(f"Multiply: {vec1 * vec2}")
    print(f"Divide: {vec1 / vec2}")
    print(f"Dot Product: {vec1.dot(vec2)}")
    print(f"Cross Product: {vec1.cross(vec2)}")
