import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('TkAgg')  # Under the new MacOS, we need this line to make sure that matplotlib works properly

filename_of_graph = "ComparisonForTestRun_Output"


def reader_for_record(record_filename, startLineNumber):
    with open(record_filename, mode="r") as file_of_record:
        lines = file_of_record.readlines()
        for index_of_line in range(startLineNumber, len(lines)):
            line = lines[index_of_line]
            lines[index_of_line] = eval(line)
        return lines[startLineNumber:]


record_filename = "TestRun_Output"
records = reader_for_record(record_filename, 6)
print(records)
list_n = [single_record[0] for single_record in records]
list_TotalNumberOfFateLineDerivation = [single_record[1] for single_record in records]
list_TotalNumberOfFateLineEvolve = [single_record[2] for single_record in records]
list_Expression1 = [single_record[3] for single_record in records]
list_Expression2 = [single_record[4] for single_record in records]
plt.plot(list_n, list_TotalNumberOfFateLineDerivation, "g", label="TotalNumberOfFateLineDerivation")
plt.plot(list_n, list_TotalNumberOfFateLineEvolve, "g--", label="TotalNumberOfFateLineEvolve")
plt.plot(list_n, list_Expression1, "r", label='n**2')
plt.plot(list_n, list_Expression2, "r--", label="3*(1-(7/3)**n)/(1-7/3)")
plt.xlabel("n")
plt.ylabel("count")
plt.legend()
plt.title("Asymptotical Behavior (n versus counts)")
filename_of_graph = "ComparisonForTestRun_Output"
plt.savefig(filename_of_graph)
plt.show()
