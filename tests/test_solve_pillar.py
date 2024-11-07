import importlib
import logging
import webbrowser
from pathlib import Path

import numpy as np
import pyroll.core
import pytest
from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, Transport, RoundGroove

import pyroll.sparling_spreading
import pyroll.pillar_model

importlib.reload(pyroll.sparling_spreading)

DE_COUNT = 50


try:
    import pyroll.pillar_model

    importlib.reload(pyroll.sparling_spreading)

    PILLAR_MODEL_LOADED = True

except ImportError:
    PILLAR_MODEL_LOADED = False


@pytest.mark.skipif(not pyroll.sparling_spreading.PILLAR_MODEL_LOADED, reason="Pillar model is not installed.")
def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")
    pyroll.pillar_model.PILLAR_COUNT = 30

    in_profile = Profile.square(
        side=24e-3,
        corner_radius=3e-3,
        temperature=1200 + 273.15,
        strain=0,
        material=["C45", "steel"],
        flow_stress=100e6,
        density=7.5e3,
        thermal_capacity=690,
    )

    sequence = PassSequence(
        [
            RollPass(
                label="Oval I",
                roll=Roll(
                    groove=CircularOvalGroove(
                        depth=5e-3,
                        r1=6e-3,
                        r2=40e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    contact_length=58e-3,
                ),
                gap=2e-3,
                disk_element_count=DE_COUNT,
            ),
            Transport(
                label="I => II",
                duration=1
            ),
            RollPass(
                label="Round II",
                roll=Roll(
                    groove=RoundGroove(
                        r1=1e-3,
                        r2=10e-3,
                        depth=9e-3
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1
                ),
                gap=2e-3,
                disk_element_count=DE_COUNT,
            ),
        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    try:
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report, encoding="utf-8")
        webbrowser.open(f.as_uri())

    except ImportError:
        pass

    assert not np.isclose(sequence[0].out_profile.width, sequence[0].in_profile.width)
