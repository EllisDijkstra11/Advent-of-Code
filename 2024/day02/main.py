from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    return [[int(n) for n in line.split(' ')] for line in input_lines.split('\n')]

class Reports:
    def __init__(self, reports):
        self.reports = reports
        self.safe_positive = {1, 2, 3}
        self.safe_negative = {-1, -2, -3}
    
    def find_save_reports(self):
        save_reports = 0

        for report in self.reports:
            current_report = set()
            for index in range(len(report) - 1):
                current_report.add(report[index + 1] - report[index])
            
            if self.report_is_safe(current_report):
                save_reports += 1
                
        return save_reports

    def find_almost_save_reports(self):
        save_reports = 0

        for report in self.reports:
            current_report = set()
            for index in range(len(report) - 1):
                current_report.add(report[index + 1] - report[index])
            
            if self.report_is_safe(current_report):
                save_reports += 1
            else:
                found = False
                for level in range(len(report)):
                    if not found:
                        new_report = report.copy()
                        new_report.pop(level)
                        current_report = set()

                        for index in range(len(new_report) - 1):
                            current_report.add(new_report[index + 1] - new_report[index])

                        if self.report_is_safe(current_report):
                            save_reports += 1
                            found = True
                
        return save_reports
    
    def report_is_safe(self, current_report):
        if self.safe_negative == current_report | self.safe_negative:
            return True
        elif self.safe_positive == current_report | self.safe_positive:
            return True
    
        return False


def first(reports):
    reports = Reports(reports)
    return reports.find_save_reports()

def second(reports):
    reports = Reports(reports)
    return reports.find_almost_save_reports()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day02"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input         (2):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input         (4):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")