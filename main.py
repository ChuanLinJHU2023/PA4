class FateLine:
    def __init__(self, x, y, index_x=0, index_y=0, history=None):
        self.id = 0
        self.x = x
        self.y = y
        self.index_x = index_x
        self.index_y = index_y
        self.history = history
        if history is None:
            history = []
        self.history = history
        self.birth_date = len(self.history)
        self.n_of_noise = None
        self.n_of_noise_b = None
        self.n_of_noise_d = None
        self.is_solution = None

    def make_choice_when_receiving_symbol(self, symbol):
        if "d" in self.history:
            self.history.append("d")
            if OnlineSignalProcessor.isTestRun:
                OnlineSignalProcessor.number_of_fate_line_evolvement += 1
            return None
        returnedFateLines = []
        symbol_x = self.x[self.index_x]
        symbol_y = self.y[self.index_y]
        if symbol_x == symbol:
            # Create a new Fate Line that chooses y at this point
            history = self.history.copy()
            history.append("x")
            index_x = self.index_x_increment()
            index_y = self.index_y
            x = self.x
            y = self.y
            newFateLine = FateLine(x, y, index_x, index_y, history)
            returnedFateLines.append(newFateLine)
            if OnlineSignalProcessor.isTestRun:
                OnlineSignalProcessor.number_of_fate_line_derivation += 1
        if symbol_y == symbol:
            # Create a new Fate Line that chooses y at this point
            history = self.history.copy()
            history.append("y")
            index_x = self.index_x
            index_y = self.index_y_increment()
            x = self.x
            y = self.y
            newFateLine = FateLine(x, y, index_x, index_y, history)
            returnedFateLines.append(newFateLine)
            if OnlineSignalProcessor.isTestRun:
                OnlineSignalProcessor.number_of_fate_line_derivation += 1
        if "x" not in self.history and "y" not in self.history:
            self.history.append("b")
        else:
            self.history.append("d")
        if OnlineSignalProcessor.isTestRun:
            OnlineSignalProcessor.number_of_fate_line_evolvement += 1
        return returnedFateLines

    def index_x_increment(self):
        return (self.index_x + 1) % len(self.x)

    def index_y_increment(self):
        return (self.index_y + 1) % len(self.y)

    def check(self):
        # In Paragraph 5, to get a correct solution, we need at least a full match of x and a full match of y.
        count_of_symbols_from_x = self.history.count("x")
        count_of_symbols_from_y = self.history.count("y")
        count_of_symbols_from_b = self.history.count("b")
        count_of_symbols_from_d = self.history.count("d")
        len_x = len(self.x)
        len_y = len(self.y)
        len_history = len(self.history)
        self.n_of_noise = len_history - count_of_symbols_from_x - count_of_symbols_from_y
        self.n_of_noise_b = count_of_symbols_from_b
        self.n_of_noise_d = count_of_symbols_from_d
        if count_of_symbols_from_x >= len_x and count_of_symbols_from_y >= len_y:
            if count_of_symbols_from_x % len_x == 0 and count_of_symbols_from_y % len_y == 0:
                self.is_solution = True
                return
        self.is_solution = False
        return


class OnlineSignalProcessor:
    number_of_fate_line_evolvement = 0
    number_of_fate_line_derivation = 0
    isTestRun = False
    TestRunOutputFilename = None
    TestRunDatasetOutputFilename = None
    TestRunDatasetInputFilename = None

    def __init__(self, x, y, whetherWithMinimalNoise=False):
        newFateLine = FateLine(x, y)
        self.FateLines = []
        self.FateLines.append(newFateLine)
        self.failed_solutions = []
        self.whetherWithMinimalNoise = whetherWithMinimalNoise

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
            i += 1
            print("Fate Line{:3} (birth date:{:3}):".format(fateLine.id, fateLine.birth_date), fateLine.history)
        print()
        print()

    def getSolutions(self):
        whetherWithMinimalNoise = self.whetherWithMinimalNoise
        n_of_noise_minimal = 1000000
        for fateLine in self.FateLines:
            fateLine.check()
            if fateLine.is_solution and fateLine.n_of_noise < n_of_noise_minimal:
                n_of_noise_minimal = fateLine.n_of_noise
        print("Here is all the solutions:")
        for fateLine in self.FateLines:
            if fateLine.is_solution:
                if whetherWithMinimalNoise:
                    if fateLine.n_of_noise == n_of_noise_minimal:
                        print("Fate Line{:3} (birth date:{:3}):".format(fateLine.id, fateLine.birth_date),
                              fateLine.history)
                else:
                    if fateLine.n_of_noise_b == 8 and fateLine.n_of_noise_d==4:
                        print("Fate Line{:3} (birth date:{:3}):".format(fateLine.id, fateLine.birth_date), fateLine.history)


        print()
        print()
        if OnlineSignalProcessor.isTestRun:
            with open(OnlineSignalProcessor.TestRunDatasetOutputFilename, "a+") as file:
                fateLine = self.FateLines[0]
                n = len(fateLine.history)
                file.write("There is the output dataset of a test run with n={}\n".format(n))
                for fateLine in self.FateLines:
                    if fateLine.is_solution:
                        file.write("Fate Line{:3} (birth date:{:3}): {}\n".format(fateLine.id, fateLine.birth_date,
                                                                                  fateLine.history))
                file.write("\n" * 10)

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
                print(positions_of_y, "are repetitions of y")
                print(positions_of_noise, "are noise")

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

    def TestRunSummary(self):
        fateLine = self.FateLines[0]
        a0 = len(fateLine.history)
        a1 = OnlineSignalProcessor.number_of_fate_line_derivation
        a2 = OnlineSignalProcessor.number_of_fate_line_evolvement
        a3 = 2 ** a0
        a4 = 3 ** a0
        with open(OnlineSignalProcessor.TestRunOutputFilename, "a+") as file:
            file.write("{} {} {} {} {}\n".format(a0, a1, a2, a3, a4))


def SignalProcess(signal, x, y, whetherWithMinimalNoise=False):
    onlineSignalProcessor = OnlineSignalProcessor(x, y, whetherWithMinimalNoise=whetherWithMinimalNoise)
    for symbol in signal:
        onlineSignalProcessor.receive_symbol(symbol)
        onlineSignalProcessor.report()
    onlineSignalProcessor.getSolutions()
    if OnlineSignalProcessor.isTestRun:
        onlineSignalProcessor.TestRunSummary()
    return onlineSignalProcessor
