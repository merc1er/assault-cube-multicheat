from dataclasses import dataclass


@dataclass
class Vec2:
    x: float
    y: float


@dataclass
class Vec3:
    x: float
    y: float
    z: float


@dataclass
class Viewport:
    x: float
    y: float
    width: float
    height: float
