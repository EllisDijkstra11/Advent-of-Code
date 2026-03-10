import unittest
from main import CPU  # Replace with your actual file name

class TestCPU(unittest.TestCase):
    def test_case_1_bst_opcode(self):
        """
        If register C contains 9, the program 2,6 would set register B to 1.
        """
        input_data = [0, 0, 9, 2, 6]  # A=0, B=0, C=9, Program=[2,6]
        cpu = CPU(input_data)
        cpu.find_result()
        self.assertEqual(cpu.reg_B, 1, "Register B should be set to 1.")

    def test_case_2_out_opcode(self):
        """
        If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
        """
        input_data = [10, 0, 0, 5, 0, 5, 1, 5, 4]  # A=10, B=0, C=0, Program=[5,0,5,1,5,4]
        cpu = CPU(input_data)
        cpu.find_result()
        self.assertEqual(cpu.string_result(), "0,1,2", "Output should be 0,1,2.")

    def test_case_3_adv_jnz_opcodes(self):
        """
        If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0
        and leave 0 in register A.
        """
        input_data = [2024, 0, 0, 0, 1, 5, 4, 3, 0]  # A=2024, B=0, C=0, Program=[0,1,5,4,3,0]
        cpu = CPU(input_data)
        cpu.find_result()
        self.assertEqual(cpu.string_result(), "4,2,5,6,7,7,7,7,3,1,0", "Output should match expected sequence.")
        self.assertEqual(cpu.reg_A, 0, "Register A should be set to 0 after execution.")

    def test_case_4_bxl_opcode(self):
        """
        If register B contains 29, the program 1,7 would set register B to 26.
        """
        input_data = [0, 29, 0, 1, 7]  # A=0, B=29, C=0, Program=[1,7]
        cpu = CPU(input_data)
        cpu.find_result()
        self.assertEqual(cpu.reg_B, 26, "Register B should be set to 26 after XOR operation.")

    def test_case_5_bxc_opcode(self):
        """
        If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
        """
        input_data = [0, 2024, 43690, 4, 0]  # A=0, B=2024, C=43690, Program=[4,0]
        cpu = CPU(input_data)
        cpu.find_result()
        self.assertEqual(cpu.reg_B, 44354, "Register B should be set to 44354 after XOR operation with C.")

    def test_case_6_historian_output(self):
        """
        The Historians' device outputs 4,6,3,5,6,3,5,2,1,0 with the provided input.
        Input:
            Register A: 729
            Register B: 0
            Register C: 0
            Program: 0,1,5,4,3,0
        """
        input_data = [729, 0, 0, 0, 1, 5, 4, 3, 0]  # A=729, B=0, C=0, Program=[0,1,5,4,3,0]
        cpu = CPU(input_data)
        cpu.find_result()
        self.assertEqual(cpu.string_result(), "4,6,3,5,6,3,5,2,1,0", "Output should match 4,6,3,5,6,3,5,2,1,0.")

if __name__ == '__main__':
    unittest.main()