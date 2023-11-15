# from main import *
# from main import *
# for n in
# x="101"
# y="0"
# s="100010101"
# onlineSignalProcessor=SignalProcess(s,x,y)
from main import *
OnlineSignalProcessor.isTestRun=True
OnlineSignalProcessor.TestRunOutputFilename="TestRun_Output"
for n in range(4,6):
    s="0"*(n-1)+"1"
    x="0"
    y="0"*(n-2)+"1"
    SignalProcess(s, x, y)
    # print(s)
    # print(x)
    # print(y)
    # print(x+y)