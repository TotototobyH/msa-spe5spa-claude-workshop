import pathlib
import pandas as pd

HERE        = pathlib.Path(__file__).parent
INPUT_PATH  = HERE / ".." / "data" / "gps_training_messy.csv"
OUTPUT_PATH = HERE / ".." / "data" / "gps_training_clean.csv"

# Physiological thresholds used for flagging — rows are kept, not dropped.
DISTANCE_FLAG_M  = 15_000   # metres: above any realistic training session total
SPEED_FLAG_MS    = 12.4     # m/s: above the human sprint world-record speed


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_raw(path: pathlib.Path) -> pd.DataFrame:
    """Load every column as a string so we control all type conversion."""
    return pd.read_csv(path, dtype=str)


def drop_blank_rows(df: pd.DataFrame, log: list) -> pd.DataFrame:
    """Remove rows that are entirely empty."""
    blank = df.isnull().all(axis=1)
    count = int(blank.sum())
    if count:
        log.append(f"Dropped {count} completely blank row(s).")
    return df[~blank].reset_index(drop=True)


def parse_dates(df: pd.DataFrame, log: list) -> pd.DataFrame:
    """Normalise the three date formats found in the file to ISO 8601."""
    dates = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y"):
        mask = dates.isna()
        if not mask.any():
            break
        parsed = pd.to_datetime(df.loc[mask, "date"], format=fmt, errors="coerce")
        dates.loc[mask] = parsed
    unparsed = int(dates.isna().sum())
    if unparsed:
        log.append(f"WARNING: {unparsed} date value(s) could not be parsed — left as NaT.")
    df["date"] = dates.dt.strftime("%Y-%m-%d")
    return df


def normalise_sessions(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and lowercase every session name."""
    df["session"] = df["session"].str.strip().str.lower()
    return df


def strip_player_ids(df: pd.DataFrame) -> pd.DataFrame:
    """Remove leading/trailing whitespace from player_id."""
    df["player_id"] = df["player_id"].str.strip()
    return df


def drop_duplicates(df: pd.DataFrame, log: list) -> pd.DataFrame:
    """Drop exact duplicates after normalisation; log the count."""
    before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    dropped = before - len(df)
    if dropped:
        log.append(f"Dropped {dropped} duplicate row(s) (detected after normalisation).")
    return df


def cast_numerics(df: pd.DataFrame) -> pd.DataFrame:
    """Convert metric columns from string to float/int."""
    float_cols = [
        "total_distance_m",
        "high_speed_running_m",
        "sprint_distance_m",
        "max_speed_ms",
    ]
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["rpe"] = pd.to_numeric(df["rpe"], errors="coerce").astype("Int64")
    return df


def flag_suspect_values(df: pd.DataFrame, log: list) -> pd.DataFrame:
    """Log rows with implausible values; rows are kept in the output."""
    dist_flags = df["total_distance_m"] > DISTANCE_FLAG_M
    for _, row in df[dist_flags].iterrows():
        log.append(
            f"FLAGGED total_distance_m={row['total_distance_m']:.1f} m"
            f" — player={row['player_id']} date={row['date']}"
            f" session={row['session']} (threshold {DISTANCE_FLAG_M} m, row kept)."
        )

    speed_flags = df["max_speed_ms"] > SPEED_FLAG_MS
    for _, row in df[speed_flags].iterrows():
        log.append(
            f"FLAGGED max_speed_ms={row['max_speed_ms']} m/s"
            f" — player={row['player_id']} date={row['date']}"
            f" session={row['session']} (threshold {SPEED_FLAG_MS} m/s, row kept)."
        )

    missing_speed = int(df["max_speed_ms"].isna().sum())
    log.append(f"Rows with missing max_speed_ms: {missing_speed} (left as NaN).")

    return df


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    log = []

    df = load_raw(INPUT_PATH)
    df = drop_blank_rows(df, log)
    df = parse_dates(df, log)
    df = normalise_sessions(df)
    df = strip_player_ids(df)
    df = drop_duplicates(df, log)
    df = cast_numerics(df)
    df = flag_suspect_values(df, log)

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Input : {INPUT_PATH}  ({len(df)} rows after cleaning)")
    print(f"Output: {OUTPUT_PATH}")
    print()
    for line in log:
        print(line)


if __name__ == "__main__":
    main()
