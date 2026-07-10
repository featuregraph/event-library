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
