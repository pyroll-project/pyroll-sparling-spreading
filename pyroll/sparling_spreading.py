import importlib.util

import numpy as np
from pyroll.core import RollPass, ThreeRollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "2.0.0rc0"
PILLAR_MODEL_INSTALLED = bool(importlib.util.find_spec("pyroll.pillar_model"))

RollPass.sparling_temperature_coefficient = Hook[float]()
"""Temperature correction factor g for Sparling's spread equation."""

RollPass.sparling_strain_rate_coefficient = Hook[float]()
"""Velocity correction factor j for Sparling's spread equation."""

RollPass.sparling_material_coefficient = Hook[float]()
"""Material correction factor f for Sparling's spread equation."""

RollPass.sparling_roll_surface_coefficient = Hook[float]()
"""Friction correction factor a for Sparling's spread equation."""

RollPass.sparling_bar_surface_coefficient = Hook[float]()
"""Friction correction factor b for Sparling's spread equation."""

RollPass.sparling_exponent = Hook[float]()
"""Exponent w for Sparling's spread equation."""

root_hooks.add(Unit.OutProfile.width)


@RollPass.sparling_temperature_coefficient
def sparling_temperature_coefficient(roll_pass: RollPass):
    return 1


@RollPass.sparling_strain_rate_coefficient
def sparling_strain_rate_coefficient(roll_pass: RollPass):
    return 1


@RollPass.sparling_material_coefficient
def sparling_material_coefficient(roll_pass: RollPass):
    return 1


@RollPass.sparling_roll_surface_coefficient
def sparling_roll_surface_coefficient(roll_pass: RollPass):
    return 1


@RollPass.sparling_bar_surface_coefficient
def sparling_bar_surface_coefficient(roll_pass: RollPass):
    return 1


@RollPass.sparling_exponent
def sparling_exponent(self: RollPass):
    return 0.981 * np.exp(
        -0.6735 * ((2.395 * self.in_profile.equivalent_width ** 0.9) / (
                self.roll.working_radius ** 0.55
                * self.in_profile.equivalent_height ** 0.1
                * (-self.abs_draught) ** 0.25
        ))
    )


# noinspection PyUnresolvedReferences
@RollPass.spread
def spread(self: RollPass):
    if not (PILLAR_MODEL_INSTALLED and self.disk_elements):
        return (
                self.draught
                ** (
                        -self.sparling_exponent
                        * self.sparling_temperature_coefficient
                        * self.sparling_strain_rate_coefficient
                        * self.sparling_material_coefficient
                        * self.sparling_roll_surface_coefficient
                        * self.sparling_bar_surface_coefficient
                )
        )


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_INSTALLED and rp.disk_elements):
        if not self.has_set_or_cached("width"):
            return None

        return rp.spread * rp.in_profile.width


@ThreeRollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_INSTALLED and rp.disk_elements):
        if not self.has_set_or_cached("width"):
            return None

        return rp.spread * rp.in_profile.width


if PILLAR_MODEL_INSTALLED:
    import pyroll.pillar_model


    # noinspection PyUnresolvedReferences
    @RollPass.DiskElement.pillar_spreads
    def pillar_spreads(self: RollPass.DiskElement):
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
