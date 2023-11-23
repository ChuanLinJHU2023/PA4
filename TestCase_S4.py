from main import *
x="101"
y="010"
s="100110011001"
onlineSignalProcessor=SignalProcess(s,x,y, whetherWithMinimalNoise=True)
onlineSignalProcessor.translateSolutionWithId(216)


# For FateLine216, we have
# [1, 2, 4, 9, 11, 12] are repetitions of x
# [3, 5, 6, 7, 8, 10] are repetitions of y
# [] are noise