from pyroll.core import RollPass


@RollPass.hookspec
def sparling_temperature_coefficient(roll_pass: RollPass):
    """Gets the Sparling spreading model temperature coefficient g."""


@RollPass.hookspec
def sparling_strain_rate_coefficient(roll_pass: RollPass):
    """Gets the Sparling spreading model velocity coefficient j"""


@RollPass.hookspec
def sparling_material_coefficient(roll_pass: RollPass):
    """Gets the Sparling spreading model material coefficient f."""


@RollPass.hookspec
def sparling_roll_surface_coefficient(roll_pass: RollPass):
    """Gets the Sparling spreading model roll surface coefficient a."""


@RollPass.hookspec
def sparling_bar_surface_coefficient(roll_pass: RollPass):
    """Gets the Sparling spreading model bar surface coefficient b."""


@RollPass.hookspec
def sparling_exponent(roll_pass: RollPass):
    """Gets the Sparling spreading model exponent w."""
