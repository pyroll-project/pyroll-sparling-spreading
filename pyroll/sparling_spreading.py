import logging
import numpy as np

from pyroll.core import SymmetricRollPass, RollPass, root_hooks, Unit
from pyroll.core.hooks import Hook

VERSION = "3.0.0"
PILLAR_MODEL_LOADED = False

SymmetricRollPass.sparling_temperature_coefficient = Hook[float]()
"""Temperature correction factor g for Sparling's spread equation."""

SymmetricRollPass.sparling_strain_rate_coefficient = Hook[float]()
"""Velocity correction factor j for Sparling's spread equation."""

SymmetricRollPass.sparling_material_coefficient = Hook[float]()
"""Material correction factor f for Sparling's spread equation."""

SymmetricRollPass.sparling_roll_surface_coefficient = Hook[float]()
"""Friction correction factor a for Sparling's spread equation."""

SymmetricRollPass.sparling_bar_surface_coefficient = Hook[float]()
"""Friction correction factor b for Sparling's spread equation."""

SymmetricRollPass.sparling_exponent = Hook[float]()
"""Exponent w for Sparling's spread equation."""

root_hooks.add(Unit.OutProfile.width)


@SymmetricRollPass.sparling_temperature_coefficient
def sparling_temperature_coefficient(roll_pass: SymmetricRollPass):
    return 1


@SymmetricRollPass.sparling_strain_rate_coefficient
def sparling_strain_rate_coefficient(roll_pass: SymmetricRollPass):
    return 1


@SymmetricRollPass.sparling_material_coefficient
def sparling_material_coefficient(roll_pass: SymmetricRollPass):
    return 1


@SymmetricRollPass.sparling_roll_surface_coefficient
def sparling_roll_surface_coefficient(roll_pass: SymmetricRollPass):
    return 1


@SymmetricRollPass.sparling_bar_surface_coefficient
def sparling_bar_surface_coefficient(roll_pass: SymmetricRollPass):
    return 1


@SymmetricRollPass.sparling_exponent
def sparling_exponent(self: SymmetricRollPass):
    return 0.981 * np.exp(
        -0.6735 * ((2.395 * self.in_profile.equivalent_width ** 0.9) / (
                self.roll.working_radius ** 0.55
                * self.in_profile.equivalent_height ** 0.1
                * (-self.abs_draught) ** 0.25
        ))
    )


@SymmetricRollPass.OutProfile.width
def width(self: SymmetricRollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_LOADED and rp.disk_elements):
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
    @RollPass.DiskElement.pillar_spreads
    def pillar_spreads(self: SymmetricRollPass.DiskElement):
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

    PILLAR_MODEL_LOADED = True


except AttributeError:
    logging.getLogger(__name__).debug("Pillar model not loaded. Can not register respective hook function.")
