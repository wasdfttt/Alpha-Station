# Alpha Station Analysis
To analyze the data, run scopedataV2.py with the file path of where the data is stored. Change the region that calculates the baseline voltage on line 71 and the integration bounds on line 98 if necessary. Line 118 may also need to be changed as it filters out waveforms below a certain amount of charge.

If the waveform plots look good, then run Alpha Station Gain Effect.py with the same parameters. It will print a list of the means that can be used in Gain Plot.ipynb to create a plot of the gain as a function of angle.