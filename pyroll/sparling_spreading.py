import numpy as np

from pyroll.core import RollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "2.0.0b"

RollPass.sparling_temperature_coefficient = Hook[float]()
RollPass.sparling_velocity_coefficient = Hook[float]()
RollPass.sparling_material_coefficient = Hook[float]()
RollPass.sparling_friction_coefficient = Hook[float]()
RollPass.sparling_exponent = Hook[float]()


@RollPass.sparling_temperature_coefficient
def sparling_temperature_coefficient(self: RollPass):
    return 1


@RollPass.sparling_velocity_coefficient
def sparling_velocity_coefficient(self: RollPass):
    return 1


@RollPass.sparling_material_coefficient
def sparling_material_coefficient(self: RollPass):
    return 1


@RollPass.sparling_friction_coefficient
def sparling_friction_coefficient(self: RollPass):
    return 1


@RollPass.sparling_exponent
def sparling_exponent(self: RollPass):
    equivalent_height_change = self.in_profile.equivalent_height - self.out_profile.equivalent_height

    return 0.981 * np.exp(
        -0.6735 * ((2.395 * self.in_profile.equivalent_width ** 0.9) / (
                self.roll.working_radius ** 0.55 * self.in_profile.equivalent_height ** 0.1 * equivalent_height_change ** 0.25)))


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    roll_pass = self.roll_pass()

    if not self.has_set_or_cached("width"):
        self.width = roll_pass.roll.groove.usable_width

    spread = (roll_pass.draught ** (-roll_pass.sparling_exponent
                                    * roll_pass.sparling_temperature_coefficient
                                    * roll_pass.sparling_velocity_coefficient
                                    * roll_pass.sparling_material_coefficient
                                    * roll_pass.sparling_friction_coefficient)
              )

    return spread * roll_pass.in_profile.width


root_hooks.add(Unit.OutProfile.width)
