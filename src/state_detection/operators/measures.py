def smooth(df, signal, group, window):
    return (
        df.groupby(group)[signal]
          .transform(lambda s: s.rolling(window, min_periods=window).mean())
    )
def group_transform(df, signal, op, group):
    return df.groupby(group)[signal].transform(op)

def group_map(df, signal, op, group, offset=0):
    return df[group].map(df.groupby(group)[signal].agg(op).shift(offset))