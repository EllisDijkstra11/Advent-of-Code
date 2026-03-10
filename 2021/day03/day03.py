from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    return [n for n in input_lines.split('\n')]

class Bits:
    def __init__(self, bits):
        self.bits = bits
        self.gamma_rate = ""
        self.epsilon_rate = ""
        self.oxygen_generator_rating = bits
        self.CO2_scrubber_rating = bits
    
    def getGammaRate(self):
        return self.gamma_rate
    
    def getEpsilonRate(self):
        return self.epsilon_rate
    
    def getDecimal(self, binary):
        decimal = 0

        for index in range(len(binary)):
            if binary[index] == "1":
                decimal += 2 ** (len(binary) - index - 1)
        
        return decimal
    
    def findMostCommon(self, bits, index):
        zeroes = 0
        ones = 0

        for bit in bits:
            if bit[index] == "0":
                zeroes += 1
            else:
                ones += 1
        
        if zeroes > ones:
            return "0"
        
        return "1"
    
    def findLeastCommon(self, bits, index):
        zeroes = 0
        ones = 0

        for bit in bits:
            if bit[index] == "0":
                zeroes += 1
            else:
                ones += 1
        
        if zeroes <= ones:
            return "0"
        
        return "1"

    def findGammaRate(self):
        for index in range(len(self.bits[0])):
            self.gamma_rate += self.findMostCommon(self.bits, index)
        
    def findEpsilonRate(self):
        for index in range(len(self.bits[0])):
            self.epsilon_rate += self.findLeastCommon(self.bits, index)
            
    def getPowerConsumption(self):
        self.findGammaRate()
        self.findEpsilonRate()
        decimal_gamma_rate = self.getDecimal(self.gamma_rate)
        decimal_epsilon_rate = self.getDecimal(self.epsilon_rate)
        return decimal_gamma_rate * decimal_epsilon_rate

    def findOxygenGeneratorRating(self):
        while len(self.oxygen_generator_rating) > 1:
            for index in range(len(self.bits[0])):
                if len(self.oxygen_generator_rating) > 1:
                    most_common = self.findMostCommon(self.oxygen_generator_rating, index)
                    self.oxygen_generator_rating = list(filter(lambda x: x[index] == most_common, self.oxygen_generator_rating))

    def findCO2ScrubberRating(self):
        while len(self.CO2_scrubber_rating) > 1:
            for index in range(len(self.bits[0])):
                if len(self.CO2_scrubber_rating) > 1:
                    least_common = self.findLeastCommon(self.CO2_scrubber_rating, index)
                    self.CO2_scrubber_rating = list(filter(lambda x: x[index] == least_common, self.CO2_scrubber_rating))

    def getLifeSupportRating(self):
        self.findOxygenGeneratorRating()
        self.findCO2ScrubberRating()
        decimal_oxygen_generator_rating = self.getDecimal(self.oxygen_generator_rating[0])
        C02_scrubber_rating = self.getDecimal(self.CO2_scrubber_rating[0])
        return decimal_oxygen_generator_rating * C02_scrubber_rating

def first(input_bits):
    bits = Bits(input_bits)
    return bits.getPowerConsumption()


def second(input_bits):
    bits = Bits(input_bits)
    return bits.getLifeSupportRating()

if __name__ == "__main__":
    path = "2021/day03"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input       (198):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input       (230):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")