import importlib.util

import numpy as np
from pyroll.core import BaseRollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "3.0.0"
PILLAR_MODEL_INSTALLED = bool(importlib.util.find_spec("pyroll.pillar_model"))

BaseRollPass.sparling_temperature_coefficient = Hook[float]()
"""Temperature correction factor g for Sparling's spread equation."""

BaseRollPass.sparling_strain_rate_coefficient = Hook[float]()
"""Velocity correction factor j for Sparling's spread equation."""

BaseRollPass.sparling_material_coefficient = Hook[float]()
"""Material correction factor f for Sparling's spread equation."""

BaseRollPass.sparling_roll_surface_coefficient = Hook[float]()
"""Friction correction factor a for Sparling's spread equation."""

BaseRollPass.sparling_bar_surface_coefficient = Hook[float]()
"""Friction correction factor b for Sparling's spread equation."""

BaseRollPass.sparling_exponent = Hook[float]()
"""Exponent w for Sparling's spread equation."""

root_hooks.add(Unit.OutProfile.width)


@BaseRollPass.sparling_temperature_coefficient
def sparling_temperature_coefficient(roll_pass: BaseRollPass):
    return 1


@BaseRollPass.sparling_strain_rate_coefficient
def sparling_strain_rate_coefficient(roll_pass: BaseRollPass):
    return 1


@BaseRollPass.sparling_material_coefficient
def sparling_material_coefficient(roll_pass: BaseRollPass):
    return 1


@BaseRollPass.sparling_roll_surface_coefficient
def sparling_roll_surface_coefficient(roll_pass: BaseRollPass):
    return 1


@BaseRollPass.sparling_bar_surface_coefficient
def sparling_bar_surface_coefficient(roll_pass: BaseRollPass):
    return 1


@BaseRollPass.sparling_exponent
def sparling_exponent(self: BaseRollPass):
    return 0.981 * np.exp(
        -0.6735 * ((2.395 * self.in_profile.equivalent_width ** 0.9) / (
                self.roll.working_radius ** 0.55
                * self.in_profile.equivalent_height ** 0.1
                * (-self.abs_draught) ** 0.25
        ))
    )


@BaseRollPass.OutProfile.width
def width(self: BaseRollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_INSTALLED and rp.disk_elements):
        if not self.has_set_or_cached("width"):
            return None

        return (
                rp.draught
                ** (
                        -rp.sparling_exponent
                        * rp.sparling_temperature_coefficient
                        * rp.sparling_strain_rate_coefficient
                        * rp.sparling_material_coefficient
                        * rp.sparling_roll_surface_coefficient
                        * rp.sparling_bar_surface_coefficient
                )
        ) * rp.in_profile.width


try:
    @BaseRollPass.DiskElement.pillar_spreads
    def pillar_spreads(self: BaseRollPass.DiskElement):
        rp = self.roll_pass
        return (
                self.pillar_draughts
                ** (
                        -rp.sparling_exponent
                        * rp.sparling_temperature_coefficient
                        * rp.sparling_strain_rate_coefficient
                        * rp.sparling_material_coefficient
                        * rp.sparling_roll_surface_coefficient
                        * rp.sparling_bar_surface_coefficient
                )
        )
except AttributeError:
    pass  # pillar_model not loaded
