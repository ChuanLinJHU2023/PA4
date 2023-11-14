from main import *
x="101"
y="010"
s="001100110101011001100110010101111"
onlineSignalProcessor=SignalProcess(s,x,y)
positions_of_x_in_solution=[12,  13,  14,  15,  16,  18,  23,  25,  26]
positions_of_y_in_solution=[9,  10,  11,  17,  19,  20,  21,  22,  24,  27,  28,  29]
positions_of_noises_in_solution=[1,  2,  3,  4,  5,  6,  7,  8,  30,  31,  32,  33]
solutionId=onlineSignalProcessor.getIdOfSolution(positions_of_x_in_solution,positions_of_y_in_solution,positions_of_noises_in_solution)
print(solutionId)
onlineSignalProcessor.translateSolutionWithId(5186)

