from state_detection.operators.states import rising_state, falling_state
from state_detection.operators.events import enter_state, exit_state, event_id
from state_detection.operators.measures import smooth, group_transform

def add_wave_smoothing(df, signals, group, window=20):
    df = df.copy()
    for signal in signals:
        df[f"{signal}_smooth"] = smooth(df, signal, group, window)
    return df

def add_wave_primitives(df, signals, diff_lag=10, eps=0):
    df = df.copy()

    for signal in signals:
        rising_col = f"{signal}_rising"
        falling_col = f"{signal}_falling"
        enter_rising_col = f"enter_{rising_col}"
        exit_rising_col = f"exit_{rising_col}"

        df[rising_col] = rising_state(df[signal], diff_lag, eps)
        df[falling_col] = falling_state(df[signal], diff_lag, eps)
        df[enter_rising_col] = enter_state(df[rising_col])
        df[exit_rising_col] = exit_state(df[rising_col])

    return df

def add_wave_id(df, signals, group, id_col):
    df = df.copy()
    for signal in signals:
        df[f"{signal}_wave_id"] = event_id(df, id_col, group)
    return df

def add_wave_features(df, signals, group):
    df = df.copy()
    for signal in signals:
        rising_col = f"{signal}_rising"
        falling_col = f"{signal}_falling"
        rising_time_col = f"{rising_col}_time"
        falling_time_col = f"{falling_col}_time"

        df[rising_time_col] = group_transform(df, rising_col, 'sum', group)
        df[falling_time_col] = group_transform(df, falling_col, 'sum', group)
        df[f'{signal}_amplitude'] = (group_transform(df, signal, 'max', group) -
                                     group_transform(df, signal, 'min', group)) / 2
        df[f'{signal}_duration'] = group_transform(df, rising_time_col, 'max', group) + \
                                    group_transform(df, falling_time_col, 'max', group)
    return df


