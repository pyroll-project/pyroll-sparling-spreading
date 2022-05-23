import numpy as np
from pyroll.core import RollPass


@RollPass.hookimpl
def sparling_temperature_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def sparling_strain_rate_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def sparling_material_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def sparling_roll_surface_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def sparling_bar_surface_coefficient(roll_pass: RollPass):
    return 1


@RollPass.hookimpl
def sparling_exponent(roll_pass: RollPass):
    in_equivalent_height = roll_pass.in_profile.equivalent_rectangle.height
    in_equivalent_width = roll_pass.in_profile.equivalent_rectangle.width
    equivalent_height_change = (roll_pass.out_profile.equivalent_rectangle.height - roll_pass.in_profile.equivalent_rectangle.height)

    return 0.981 * np.exp(
        -0.6735 * ((2.395 * in_equivalent_width ** 0.9) / (
                    roll_pass.roll.working_radius ** 0.55 * in_equivalent_height ** 0.1 * equivalent_height_change ** 0.25)))


@RollPass.hookimpl
def spread(roll_pass: RollPass):
    compression = (roll_pass.in_profile.equivalent_rectangle.height
                   / roll_pass.out_profile.equivalent_rectangle.height)
    spread = (
            compression ** (roll_pass.sparling_exponent *
                            roll_pass.sparling_roll_surface_coefficient *
                            roll_pass.sparling_bar_surface_coefficient *
                            roll_pass.sparling_material_coefficient *
                            roll_pass.sparling_temperature_coefficient *
                            roll_pass.sparling_strain_rate_coefficient)
    )

    return spread
