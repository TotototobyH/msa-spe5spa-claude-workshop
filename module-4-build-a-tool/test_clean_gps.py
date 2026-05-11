"""
Tests for clean_gps.py helpers.

Each test seeds exactly the issue it names, applies the relevant helper,
and asserts the expected outcome. The integration test at the bottom
seeds all issues into one synthetic DataFrame and runs the full pipeline.
"""

import pathlib
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from clean_gps import (
    DISTANCE_FLAG_M,
    SPEED_FLAG_MS,
    cast_numerics,
    drop_blank_rows,
    drop_duplicates,
    flag_suspect_values,
    normalise_sessions,
    parse_dates,
    strip_player_ids,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_df(**kwargs) -> pd.DataFrame:
    """Build a one-row DataFrame with sensible defaults, overridden by kwargs."""
    defaults = {
        "date": "2026-04-22",
        "session": "md-3 high intensity",
        "player_id": "NF001",
        "squad": "U23",
        "position": "CM",
        "total_distance_m": "9500.0",
        "high_speed_running_m": "1100.0",
        "sprint_distance_m": "400.0",
        "max_speed_ms": "8.5",
        "rpe": "6",
    }
    defaults.update(kwargs)
    return pd.DataFrame([defaults])


# ---------------------------------------------------------------------------
# Individual helper tests
# ---------------------------------------------------------------------------

def test_drop_blank_rows_removes_all_null_row():
    good = make_df()
    blank = pd.DataFrame([{c: None for c in good.columns}])
    df = pd.concat([good, blank], ignore_index=True)
    log = []
    result = drop_blank_rows(df, log)
    assert len(result) == 1
    assert "Dropped 1" in log[0]


def test_drop_blank_rows_keeps_partial_rows():
    """A row that is only partially empty must not be dropped."""
    partial = make_df(max_speed_ms=None)
    log = []
    result = drop_blank_rows(partial, log)
    assert len(result) == 1
    assert log == []


def test_parse_dates_iso():
    df = make_df(date="2026-04-22")
    result, log = parse_dates(df, []), []
    assert result["date"].iloc[0] == "2026-04-22"


def test_parse_dates_slash():
    df = make_df(date="22/04/2026")
    result = parse_dates(df, [])
    assert result["date"].iloc[0] == "2026-04-22"


def test_parse_dates_long_form():
    df = make_df(date="22 Apr 2026")
    result = parse_dates(df, [])
    assert result["date"].iloc[0] == "2026-04-22"


def test_parse_dates_all_three_formats():
    rows = [
        make_df(date="2026-04-22"),
        make_df(date="22/04/2026"),
        make_df(date="22 Apr 2026"),
    ]
    df = pd.concat(rows, ignore_index=True)
    result = parse_dates(df, [])
    assert list(result["date"]) == ["2026-04-22", "2026-04-22", "2026-04-22"]


def test_normalise_sessions_lowercases_and_strips():
    cases = ["MD-3 HIGH INTENSITY", "Md-3 High Intensity", "md-3 high intensity  "]
    for raw in cases:
        df = make_df(session=raw)
        result = normalise_sessions(df)
        assert result["session"].iloc[0] == "md-3 high intensity"


def test_strip_player_ids_removes_whitespace():
    for raw in ["NF022 ", " NF022", " NF022 "]:
        df = make_df(player_id=raw)
        result = strip_player_ids(df)
        assert result["player_id"].iloc[0] == "NF022"


def test_drop_duplicates_catches_post_normalisation_duplicate():
    """
    NF006 duplicate: identical values, session differs only in casing.
    After normalise_sessions the two rows are identical, so drop_duplicates
    should remove one.
    """
    row_a = make_df(player_id="NF006", session="Match + 1 Recovery")
    row_b = make_df(player_id="NF006", session="match + 1 recovery")
    df = pd.concat([row_a, row_b], ignore_index=True)
    df = normalise_sessions(df)
    log = []
    result = drop_duplicates(df, log)
    assert len(result) == 1
    assert "Dropped 1" in log[0]


def test_cast_numerics_converts_strings():
    df = make_df(
        total_distance_m="9500.0",
        high_speed_running_m="1100.0",
        sprint_distance_m="400.0",
        max_speed_ms="8.5",
        rpe="6",
    )
    result = cast_numerics(df)
    assert result["total_distance_m"].dtype == float
    assert result["max_speed_ms"].dtype == float
    assert result["rpe"].dtype == pd.Int64Dtype()


def test_missing_max_speed_preserved():
    """Rows with blank max_speed_ms must not be dropped — they stay as NaN."""
    df = make_df(max_speed_ms=None)
    df = cast_numerics(df)
    log = []
    result = flag_suspect_values(df, log)
    assert len(result) == 1
    assert pd.isna(result["max_speed_ms"].iloc[0])
    assert any("missing max_speed_ms: 1" in line for line in log)


def test_flag_suspect_distance_keeps_row():
    df = make_df(total_distance_m=str(DISTANCE_FLAG_M + 1))
    df = cast_numerics(df)
    log = []
    result = flag_suspect_values(df, log)
    assert len(result) == 1                          # row kept
    assert any("FLAGGED total_distance_m" in line for line in log)


def test_flag_suspect_speed_keeps_row():
    df = make_df(max_speed_ms=str(SPEED_FLAG_MS + 1))
    df = cast_numerics(df)
    log = []
    result = flag_suspect_values(df, log)
    assert len(result) == 1                          # row kept
    assert any("FLAGGED max_speed_ms" in line for line in log)


# ---------------------------------------------------------------------------
# Integration test — all issues seeded in one synthetic dataset
# ---------------------------------------------------------------------------

SYNTHETIC_CSV = """\
date,session,player_id,squad,position,total_distance_m,high_speed_running_m,sprint_distance_m,max_speed_ms,rpe
2026-04-22,MD-3 HIGH INTENSITY,NF001,U23,CM,9500.0,1100.0,400.0,,5
22/04/2026,md-3 high intensity,NF002 ,U23,WM,9200.0,1050.0,380.0,,7
22 Apr 2026,Md-3 High Intensity,NF003,U23,CB,7800.0,600.0,200.0,8.5,6
2026-04-22,MD-3 HIGH INTENSITY,NF004,U23,FW,35000.0,1200.0,450.0,,8
2026-04-22,md-3 high intensity,NF005,U16,CM,9000.0,900.0,300.0,14.9,4
20 Apr 2026,Match + 1 recovery,NF006 ,U23,CM,5200.0,550.0,210.0,8.3,4
20 Apr 2026,Match + 1 Recovery,NF006 ,U23,CM,5200.0,550.0,210.0,8.3,4
,,,,,,,,,
"""


def _run_pipeline(csv_text: str):
    """Apply every cleaning step in order and return (df, log)."""
    import io
    log = []
    df = pd.read_csv(io.StringIO(csv_text), dtype=str)
    df = drop_blank_rows(df, log)
    df = parse_dates(df, log)
    df = normalise_sessions(df)
    df = strip_player_ids(df)
    df = drop_duplicates(df, log)
    df = cast_numerics(df)
    df = flag_suspect_values(df, log)
    return df, log


def test_integration_row_count():
    """8 input rows − 1 blank − 1 duplicate = 6 output rows."""
    df, _ = _run_pipeline(SYNTHETIC_CSV)
    assert len(df) == 6


def test_integration_dates_normalised():
    df, _ = _run_pipeline(SYNTHETIC_CSV)
    assert df["date"].str.match(r"\d{4}-\d{2}-\d{2}").all()


def test_integration_sessions_lowercase():
    df, _ = _run_pipeline(SYNTHETIC_CSV)
    assert (df["session"] == df["session"].str.lower()).all()


def test_integration_player_ids_stripped():
    df, _ = _run_pipeline(SYNTHETIC_CSV)
    assert not df["player_id"].str.contains(r"\s").any()


def test_integration_outliers_kept_and_flagged():
    df, log = _run_pipeline(SYNTHETIC_CSV)
    assert (df["player_id"] == "NF004").any(), "Distance outlier row must be kept"
    assert (df["player_id"] == "NF005").any(), "Speed outlier row must be kept"
    assert any("FLAGGED total_distance_m" in line for line in log)
    assert any("FLAGGED max_speed_ms" in line for line in log)


def test_integration_missing_speed_preserved():
    df, log = _run_pipeline(SYNTHETIC_CSV)
    # NF001, NF002, NF004 all have blank max_speed_ms in the synthetic input
    missing = df["max_speed_ms"].isna().sum()
    assert missing == 3
    assert any("missing max_speed_ms" in line for line in log)


def test_integration_duplicate_removed():
    _, log = _run_pipeline(SYNTHETIC_CSV)
    assert any("duplicate" in line.lower() for line in log)
