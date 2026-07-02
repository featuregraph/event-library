def enter_state(state, group=None):
    x = state.astype(int)
    if group is None:
        return x.diff().eq(1)
    return x.groupby(group).diff().eq(1)


def exit_state(state, group=None):
    x = state.astype(int)
    if group is None:
        return x.diff().eq(-1)
    return x.groupby(group).diff().eq(-1)


def event_number(enter, group=None):
    if group is None:
        return enter.cumsum()
    return enter.groupby(group).cumsum()
