class FateLine:
    def __init__(self, x, y, index_x=0, index_y=0, history=[]):
        self.id = 0
        self.x = x
        self.y = y
        self.index_x = index_x
        self.index_y = index_y
        self.history = history
        self.birth_date = len(history)

    def make_choice_when_receiving_symbol(self, symbol):
        if "d" in self.history:
            self.history.append("d")
            return None

        returnedFateLines = []
        if "x" not in self.history and "y" not in self.history and "d" not in self.history:
            history = self.history.copy()
            history.append("b")
            index_x = self.index_x
            index_y = self.index_y
            x = self.x
            y = self.y
            newFateLine = FateLine(x, y, index_x, index_y, history)
            returnedFateLines.append(newFateLine)

        symbol_x = self.x[self.index_x]
        symbol_y = self.y[self.index_y]
        if symbol_x == symbol and symbol_y != symbol:
            self.history.append("x")
            self.index_x = self.index_x_increment()
        if symbol_x != symbol and symbol_y == symbol:
            self.history.append("y")
            self.index_y = self.index_y_increment()
        if symbol_x != symbol and symbol_y != symbol:
            self.history.append("d")
        if symbol_y == symbol and symbol_x == symbol:
            # Create a new Fate Line that chooses y at this point
            history = self.history.copy()
            history.append("y")
            index_x = self.index_x
            index_y = self.index_y_increment()
            x = self.x
            y = self.y
            newFateLine = FateLine(x, y, index_x, index_y, history)
            # Revise the original Fate Line that chooses x at this point
            self.history.append("x")
            self.index_x = self.index_x_increment()
            returnedFateLines.append(newFateLine)
        return returnedFateLines

    def index_x_increment(self):
        return (self.index_x + 1) % len(self.x)

    def index_y_increment(self):
        return (self.index_y + 1) % len(self.y)

    def check(self):
        # In Paragraph 5, to get a correct solution, we need at least a full match of x and a full match of y.
        count_of_symbols_from_x = self.history.count("x")
        count_of_symbols_from_y = self.history.count("y")
        if count_of_symbols_from_x >= 3 and count_of_symbols_from_y >= 3:
            if count_of_symbols_from_x % 3 == 0 and count_of_symbols_from_y % 3 == 0:
                return True
        return False


class OnlineSignalProcessor:
    def __init__(self, x, y):
        newFateLine = FateLine(x, y)
        self.FateLines = []
        self.FateLines.append(newFateLine)
        self.failed_solutions=[]

    def receive_symbol(self, symbol):
        newFateLines = []
        for fateLine in self.FateLines:
            returnedFateLines = fateLine.make_choice_when_receiving_symbol(symbol)
            if returnedFateLines:
                for newFateLine in returnedFateLines:
                    newFateLines.append(newFateLine)
        self.FateLines.extend(newFateLines)

    def report(self):
        worktime = len(self.FateLines[0].history)
        print("Here is a report at time t={}".format(worktime))
        numberOfFateLines = len(self.FateLines)
        i = 0
        while i < numberOfFateLines:
            fateLine = self.FateLines[i]
            fateLine.id = i + 1
            print("Fate Line{:3} (birth date:{:3}):".format(fateLine.id, fateLine.birth_date), fateLine.history)
            i += 1
        print()
        print()

    def getSolutions(self):
        for fateLine in self.FateLines:
            if not fateLine.check():
                self.failed_solutions.append(fateLine.id)
        print("Here is all the solutions:")
        for fateLine in self.FateLines:
            if fateLine.id not in self.failed_solutions:
                print("Fate Line{:3} (birth date:{:3}):".format(fateLine.id, fateLine.birth_date), fateLine.history)
        print()
        print()

    def getFateLineById(self, id):
        for fateLine in self.FateLines:
            if fateLine.id == id:
                return fateLine

    def translateSolutionWithId(self, id):
        for fateLine in self.FateLines:
            if fateLine.id == id:
                history = fateLine.history
                positions_of_x = []
                positions_of_y = []
                positions_of_noise = []
                for i in range(len(history)):
                    if history[i] == "x":
                        positions_of_x.append(i + 1)
                    elif history[i] == "y":
                        positions_of_y.append(i + 1)
                    else:
                        positions_of_noise.append(i + 1)
                print("For FateLine{:3}, we have".format(id))
                print(positions_of_x, "are repetitions of x")
                print(positions_of_y, "are repetitions of x")
                print(positions_of_noise, "are repetitions of x")

    def getIdOfSolution(self, positions_of_x_in_solution, positions_of_y_in_solution, positions_of_noises_in_solution):
        for fateLine in self.FateLines:
            history = fateLine.history
            positions_of_x = []
            positions_of_y = []
            positions_of_noise = []
            for i in range(len(history)):
                if history[i] == "x":
                    positions_of_x.append(i + 1)
                elif history[i] == "y":
                    positions_of_y.append(i + 1)
                else:
                    positions_of_noise.append(i + 1)
            if positions_of_x == positions_of_x_in_solution:
                if positions_of_y == positions_of_y_in_solution:
                    if positions_of_noise == positions_of_noises_in_solution:
                        return fateLine.id
        return None


def SignalProcess(signal, x, y):
    onlineSignalProcessor = OnlineSignalProcessor(x, y)
    for symbol in signal:
        onlineSignalProcessor.receive_symbol(symbol)
        onlineSignalProcessor.report()
    onlineSignalProcessor.getSolutions()
    return onlineSignalProcessor
