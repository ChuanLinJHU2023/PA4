from main import *
x="101"
y="0"
s="100010101"
onlineSignalProcessor=SignalProcess(s,x,y)
onlineSignalProcessor.translateSolutionWithId(1)

# Fate Line  1 (birth date:  0): ['x', 'x', 'y', 'y', 'x', 'y', 'x', 'x', 'x']
# positions_of_x_in_solution=[1,2,5,7,8,9]
# positions_of_y_in_solution=[3,4,6]
# positions_of_noises_in_solution=[]
# solutionId=onlineSignalProcessor.getIdOfSolution(positions_of_x_in_solution,positions_of_y_in_solution,positions_of_noises_in_solution)
# print(solutionId)

fateLine=onlineSignalProcessor.getFateLineById(22)
print(fateLine.check())