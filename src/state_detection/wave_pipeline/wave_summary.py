from state_detection.operators.events import enter_state, exit_state, event_number
from state_detection.operators.meaasures import smooth
from state_detection.operators.states import rising_state, falling_state

def add_summary_comparison_features(summarydf, signal, group):
    summarydf = summarydf.copy()

    group_cols = group if isinstance(group, list) else [group]

    amp = f"{signal}_amplitude"
    rise = f"{signal}_rise_time"
    fall = f"{signal}_fall_time"

    if f"{signal}_peak_index" in summarydf.columns:
        summarydf[f"{signal}_period"] = (
            summarydf.groupby(group_cols)[f"{signal}_peak_index"]
                 .diff()
        )

    summarydf[f"{signal}_amplitude_prev"] = (
        summarydf.groupby(group_cols)[amp].shift(1)
    )

    summarydf[f"{signal}_damping_ratio"] = (
        summarydf[amp] / summarydf[f"{signal}_amplitude_prev"]
    )

    summarydf[f"{signal}_decay_rate"] = (
        1 - summarydf[f"{signal}_damping_ratio"]
    )

    summarydf[f"{signal}_symmetry"] = (
        summarydf[rise] / (summarydf[rise] + summarydf[fall])
    )

    return summarydf

def summarize_runs(summarydf, signal, group):
    return (
        summarydf.groupby(group)
        .agg(
            **{
                f"{signal}_amplitude_mean": (f"{signal}_amplitude", "mean"),
                f"{signal}_amplitude_std": (f"{signal}_amplitude", "std"),

                f"{signal}_period_mean": (f"{signal}_period", "mean"),
                f"{signal}_period_std": (f"{signal}_period", "std"),

                f"{signal}_wave_duration_mean": (f"{signal}_wave_duration", "mean"),
                f"{signal}_wave_duration_std": (f"{signal}_wave_duration", "std"),

                f"{signal}_rise_time_mean": (f"{signal}_rise_time", "mean"),
                f"{signal}_fall_time_mean": (f"{signal}_fall_time", "mean"),

                f"{signal}_symmetry_mean": (f"{signal}_symmetry", "mean"),
                f"{signal}_symmetry_std": (f"{signal}_symmetry", "std"),

                f"{signal}_damping_ratio_mean": (f"{signal}_damping_ratio", "mean"),
                f"{signal}_damping_ratio_std": (f"{signal}_damping_ratio", "std"),

                f"{signal}_decay_rate_mean": (f"{signal}_decay_rate", "mean"),
                f"{signal}_decay_rate_std": (f"{signal}_decay_rate", "std"),

                # Number of detected oscillations
                f"{signal}_wave_count": (f"{signal}_wave_num", "count"),

                # Largest oscillation
                f"{signal}_max_amplitude": (f"{signal}_amplitude", "max"),

                # Longest oscillation
                f"{signal}_max_duration": (f"{signal}_wave_duration", "max"),

                # Fraction of waves that are growing
                f"{signal}_fraction_growing": (
                    f"{signal}_damping_ratio",
                    lambda x: (x > 1).mean()
                ),

                # Fraction of waves that are damping
                f"{signal}_fraction_damping": (
                    f"{signal}_damping_ratio",
                    lambda x: (x < 1).mean()
                ),
            }
        )
    )
