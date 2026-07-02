from state_detection.state_operators import smooth, rising_state, falling_state, enter_state, exit_state, event_number

def add_wave_features(df, signal, group, smooth_window=20, diff_lag=10, eps=0):
    df = df.copy()

    smooth_col = f"{signal}_smooth"
    rising_col = f"{signal}_rising"
    falling_col = f"{signal}_falling"
    enter_col = f"enter_{rising_col}"
    exit_col = f"exit_{rising_col}"
    wave_col = f"{signal}_wave_num"

    df[smooth_col] = (
        df.groupby(group)[signal]
          .transform(lambda s: s.rolling(smooth_window, min_periods=smooth_window).mean())
    )

    delta = (
        df.groupby(group)[smooth_col]
          .transform(lambda s: s.diff(diff_lag))
    )

    df[rising_col] = delta > eps
    df[falling_col] = delta < -eps

    df[enter_col] = (
        df.groupby(group)[rising_col]
          .transform(lambda s: s.astype(int).diff().eq(1))
    )

    df[exit_col] = (
        df.groupby(group)[rising_col]
          .transform(lambda s: s.astype(int).diff().eq(-1))
    )

    df[wave_col] = (
        df.groupby(group)[enter_col]
          .transform(lambda s: s.cumsum())
    )

    return df

def measure_wave(df, wave_col, signals, group):
    group_cols = group + [wave_col] if isinstance(group, list) else [group, wave_col]

    agg_spec = {}

    for signal in signals:
        agg_spec[f"{signal}_peak"] = (signal, "max")
        agg_spec[f"{signal}_trough"] = (signal, "min")
        agg_spec[f"{signal}_mean"] = (signal, "mean")

    waves = (
        df.groupby(group_cols)
          .agg(**agg_spec)
          .reset_index()
    )

    for signal in signals:
        waves[f"{signal}_peak_to_trough"] = (
            waves[f"{signal}_peak"] - waves[f"{signal}_trough"]
        )
        waves[f"{signal}_amplitude"] = waves[f"{signal}_peak_to_trough"] / 2

    return waves