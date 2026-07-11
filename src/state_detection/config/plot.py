df = df[7000:8000]

fig, ax = plt.subplots(
    nrows=2,
    ncols=1,
    figsize=(16, 5),
    sharex=True,
    constrained_layout=True
)

# Top plot
ax[0].plot(df.index, df['respiration'], label='respiration', linewidth=2)
ax[0].legend(loc='upper right')
ax[0].set_ylabel('Respiration')
ax[0].grid(alpha=0.3)

# Bottom plot
ax[1].plot(df.index, df['respiration_amplitude'],
           label='respiration_amplitude',
           linewidth=2)
ax[1].legend(loc='center right')
ax[1].set_ylabel('Amplitude')
ax[1].set_xlabel('Time')
ax[1].grid(alpha=0.3)

# fig, ax = plt.subplots(
#     2, 1,
#     figsize=(16, 6),
#     sharex=True,
#     gridspec_kw={'hspace': 0.12}
# )

# ax[0].plot(x, respiration, lw=2)
# ax[0].legend(['respiration'], loc='upper right')

# ax[1].plot(x, respiration_amplitude, lw=2)
# ax[1].legend(['respiration_amplitude'], loc='center right')