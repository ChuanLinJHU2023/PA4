from main import *
x="101"
y="0"
s="100010101"
onlineSignalProcessor=SignalProcess(s,x,y)
onlineSignalProcessor.translateSolutionWithId(69)
fateLine=onlineSignalProcessor.getFateLineById(69)

# For FateLine 69, we have
# [1, 2, 5, 7, 8, 9] are repetitions of x
# [3, 4, 6] are repetitions of y
# [] are noise