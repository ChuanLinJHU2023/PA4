from main import *
OnlineSignalProcessor.isTestRun=True
OnlineSignalProcessor.TestRunOutputFilename="TestRun_Output"
OnlineSignalProcessor.TestRunDatasetOutputFilename="TestRun_DatasetOutput"
OnlineSignalProcessor.TestRunDatasetInputFilename="TestRun_DatasetInput"
s="""a0=n
a1=number_of_fate_line_derivation
a2=number_of_fate_line_evolvement
a3=2**n
a4=3*(1-(7/3)**n)/(1-7/3)
[a0,a1,a2,a3,a4]
"""
with open(OnlineSignalProcessor.TestRunOutputFilename, "a+") as file:
    file.write(s)

for n in range(4,16):
    s="0"*(n-1)+"1"
    x="0"
    y="0"*(n-2)+"1"
    with open(OnlineSignalProcessor.TestRunDatasetInputFilename, "a+") as file:
        file.write("There is the input dataset of a test run with n={}\n".format(n))
        file.write("n:{}\n".format(n))
        file.write("s:{}\n".format(s))
        file.write("x:{}\n".format(x))
        file.write("y:{}\n".format(y))
        file.write("\n"*5)
    SignalProcess(s, x, y)

    # a0 = n
    # a1 = number_of_fate_line_derivation
    # a2 = number_of_fate_line_evolvement
    # a3 = 2 ** n
    # a4 = 3 ** n