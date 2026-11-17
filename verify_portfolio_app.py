"""Check the recorded Lab 14 window sensitivity through the reviewer entry point."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


def verify():
    app = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run(timeout=60)

    for window, months, weights, metrics in (
        ("All returns", 59, ["20.00", "25.00", "0.00", "55.00", "0.00", "0.00"],
         ["8.31%", "11.43%", "55.00%"]),
        ("Last 36 months", 36, ["0.00", "10.00", "0.00", "80.00", "0.00", "10.00"],
         ["8.30%", "7.40%", "80.00%"]),
    ):
        app.sidebar.radio[1].set_value(window).run(timeout=60)
        assert not app.exception and not app.error, (window, app.exception, app.error)
        assert [control.value for control in app.sidebar.number_input] == [8.0, 20.0]
        assert any(f"{months} monthly returns" in caption.value for caption in app.caption)
        assert [metric.value for metric in app.metric[:3]] == metrics
        weight_tables = [
            frame.value for frame in app.dataframe if "Weight (%)" in frame.value.columns
        ]
        assert weight_tables[0]["Weight (%)"].tolist() == weights
        verdicts = next(frame.value for frame in app.dataframe if "Verdict" in frame.value)
        assert verdicts["Portfolio"].tolist() == [
            "Equal weight", "Inverse volatility", "Constrained portfolio"]
        assert verdicts["Verdict"].iloc[-1] == "Pass — both screens"

    app.sidebar.number_input[0].set_value(30.0).run(timeout=60)
    assert not app.exception and not app.error
    verdicts = next(frame.value for frame in app.dataframe if "Verdict" in frame.value)
    assert verdicts["Verdict"].iloc[-1] == "Fail — no feasible grid mix"
    assert any("Stop: no mix" in warning.value for warning in app.warning)
    print("PASS: both windows, three mandate verdicts and the infeasible-constraint stop.")


if __name__ == "__main__":
    verify()
