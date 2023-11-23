from main import *
x="101"
y="010"
s="101010101010101"
onlineSignalProcessor=SignalProcess(s,x,y, whetherWithMinimalNoise=True)
onlineSignalProcessor.translateSolutionWithId(458)

# For FateLine458, we have
# [1, 2, 3, 7, 8, 9, 13, 14, 15] are repetitions of x
# [4, 5, 6, 10, 11, 12] are repetitions of y
# [] are noise