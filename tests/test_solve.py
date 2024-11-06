import logging
import webbrowser
from pathlib import Path

import pyroll.core
from pyroll.core import Profile, PassSequence, RollPass, Roll, CircularOvalGroove, Transport, RoundGroove

import pyroll.sparling_spreading


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

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
            ),
        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report, encoding="utf-8")
        webbrowser.open(f.as_uri())

    except ImportError:
        pass
