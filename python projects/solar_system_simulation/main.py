from pydantic import Field
from pydantic.dataclasses import dataclass


class System[T]:
    def __init__(self, celestial_bodies: list[T]):
        """
        Create a celestial system composed of celestial bodies
        :param celestial_bodies: T
        """
        self._celestial_bodies: list[T] = celestial_bodies

    @property
    def celestial_bodies(self) -> list[T]:
        """
        Return celestial bodies composing the system
        :return: T
        """
        return self._celestial_bodies

    def add(self, body: T):
        """
        Add a new celestial body to the system
        :param body: T
        :return: None
        """
        self._celestial_bodies.append(body)


    def remove(self, body: T) -> T | None:
        """
        Remove a body from a system and update the system
        :param body: T
        :return: T | None
        """
        try:
            self._celestial_bodies.remove(body)
            return body
        except ValueError:
            # TODO: check this best practice
            return None


@dataclass(kw_only=True)
class CelestialBody:
    name: str = Field()
    mass: int = Field(ge=0)  # ignore negative mass for now
    volume: int = Field(ge=0)
    density: int = Field(ge=0)
    spin: int = Field(ge=0)
    position: tuple[int, int, int]
    speed: int = Field(ge=0)


class Planet(CelestialBody): ...


class Star(CelestialBody): ...


class Moon(CelestialBody): ...


class Astroid(CelestialBody): ...


if __name__ == "__main__":
    # Units:
    #   mass     -> kg
    #   volume   -> km^3
    #   density  -> kg/m^3
    #   spin     -> rotation period, in hours (sidereal, rounded to nearest hour)
    #   position -> km, simplified to average distance from the body it
    #               orbits, placed on a single axis (not true 3D ephemeris)
    #   speed    -> average orbital speed, in m/s

    sun = Star(
        name="Sun",
        mass=1_989_000_000_000_000_000_000_000_000_000,  # 1.989e30 kg
        volume=1_410_000_000_000_000_000,  # 1.41e18 km^3
        density=1408,
        spin=609,  # ~25.4-day equatorial rotation
        position=(0, 0, 0),  # center of the solar system
        speed=0,  # reference frame origin
    )
    earth = Planet(
        name="Earth",
        mass=5_972_000_000_000_000_000_000_000,  # 5.972e24 kg
        volume=1_083_210_000_000,  # 1.08321e12 km^3
        density=5514,
        spin=24,
        position=(149_600_000, 0, 0),  # avg. distance from the Sun
        speed=29_780,  # avg. orbital speed around the Sun
    )

    solar_system = System[Star | Planet](
        [sun, earth],
    )


    print(solar_system.celestial_bodies)