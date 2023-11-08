class FateLine:
    def __init__(self, x, y, index_x=0, index_y=0, history=[]):
        self.x = x
        self.y = y
        self.index_x = index_x
        self.index_y = index_y
        self.history = history
        self.is_alive = True

    def make_choice_when_receiving_symbol(self, symbol):
        if not self.is_alive:
            self.history.append("d")
            return None
        symbol_x = self.x[self.index_x]
        symbol_y = self.y[self.index_y]
        if symbol_x == symbol and symbol_y != symbol:
            self.history.append("x")
            self.index_x = self.index_x_increment()
            return None
        if symbol_x != symbol and symbol_y == symbol:
            self.history.append("y")
            self.index_y = self.index_y_increment()
            return None
        if symbol_x != symbol and symbol_y != symbol:
            self.is_alive = False
            self.history.append("d")
            return None
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
            return newFateLine

    def index_x_increment(self):
        return (self.index_x + 1) % len(self.x)

    def index_y_increment(self):
        return (self.index_y + 1) % len(self.y)


class OnlineSignalProcessor:
    def __init__(self, x, y):
        newFateLine = FateLine(x, y)
        self.FateLines = []
        self.FateLines.append(newFateLine)

    def receive_symbol(self, symbol):
        newFateLines = []
        for fateLine in self.FateLines:
            newFateLine = fateLine.make_choice_when_receiving_symbol(symbol)
            if newFateLine:
                newFateLines.append(newFateLine)
        self.FateLines.extend(newFateLines)

    def report(self):
        worktime = len(self.FateLines[0].history)
        numerOfFateLines = len(self.FateLines)
        print("Here is a report at time t={}".format(worktime))
        i = 0
        while i < numerOfFateLines:
            fateLine = self.FateLines[i]
            print("Fate Line {:3}:".format(i + 1), fateLine.history)
            i += 1
        print()
        print()


def SignalProcess(signal, x, y):
    onlineSignalProcessor = OnlineSignalProcessor(x, y)
    for symbol in signal:
        onlineSignalProcessor.receive_symbol(symbol)
        onlineSignalProcessor.report()
    return onlineSignalProcessor
