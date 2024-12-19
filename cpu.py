from memory import Memory
from cache import Cache

class CPU:

    def __init__(self):
        self.cache = Cache()
        self.memory = Memory()
        self.program_counter = 0
        self.register = {
            "instruction": 0,
            "R1": 0,
            "R2": 0,
            "R3": 0,
            "R7": 0
        }
        self.cache_flag = 0
    
    def load_into_memory(self, path):
        self.memory.load_data(path)
    
    def fetch_instruction(self, path):
        try:
            with open(path, "r") as file:
                instructions = file.readlines()
                while self.program_counter < len(instructions):
                    instruction = self.parse_instruction(instructions[self.program_counter])
                    self.decode_instruction(instruction[0])
                    if self.register["instruction"] == "HALT":
                        break
                    self.execute_instruction(instruction[1:])
                    self.program_counter += 1
        except FileNotFoundError:
            print(f"File not found at the {path}")
        except Exception as error:
            print(f"An error occured {error}")
        print("Instruction executed")
    
    def decode_instruction(self, instruction):
            self.register["instruction"] = instruction
    
    def execute_instruction(self, instruction):
        match self.register["instruction"]:
            case "ADD":
                self.add_instruction(target=instruction[0], operand_1=instruction[1], operand_2=instruction[2].strip())
            case "ADDI":
                self.addi_instrcution(target=instruction[0], operand_1=instruction[1], immd=int(instruction[2]))
            case "SUB":
                self.sub_instruction(target=instruction[0], operand_1=instruction[1], operand_2=instruction[2].strip())
            case "SLT":
                self.slt_instruction(target=instruction[0], operand_1=instruction[1], operand_2=instruction[2])
            case "BNE":
                self.bne_instruction(operand_1=instruction[0], operand_2=instruction[1], offset=int(instruction[2]))
            case "J":
                self.j_instruction(operand=instruction[0])
            case "JAL":
                self.jal_instruction(instruction[0])
            case "LW":
                register = instruction[1][-3:-1]
                offset = format(register + int(instruction[1][:-3]), "08b")
                self.lw_instruction(target=instruction[0], offset=offset)
            case "SW":
                register = instruction[1][-3:-1]
                offset = format(register + int(instruction[1][:-3]), "08b")
                self.sw_instruction(offset=offset, target=instruction[0])
            case "CACHE":
                self.cache_instruction(code=int(instruction[0]))
            case _:
                print("Unknown instruction")
    
    def add_instruction(self, target, operand_1, operand_2):
        self.register[target] = self.register[operand_1] + self.register[operand_2]
        print(f"Value {self.register[target]} saved at register {target}")
    
    def addi_instrcution(self, target, operand_1, immd):
        self.register[target] = self.register[operand_1] + immd
        print(f"Value {self.register[target]} saved at register {target}")

    def sub_instruction(self, target, operand_1, operand_2):
        self.register[target] = self.register[operand_1] - self.register[operand_2]
        print(f"Value {self.register[target]} saved at register {target}")

    def slt_instruction(self, target, operand_1, operand_2):
        if operand_1 < operand_2:
            self.register[target] = 1
            print(f"Value at {self.register[target]} set to 1")
        else:
            self.register[target] = 0
            print(f"Value at {self.register[target]} set to 0")

    def bne_instruction(self, operand_1, operand_2, offset):
        if operand_1 != operand_2:
            self.program_counter = (self.program_counter + 4) + offset * 4
            print(f"Program counter set to {self.program_counter}")

    def j_instruction(self, operand):
        self.program_counter = int(operand) * 4
        print(f"Program counter set to {self.program_counter}")

    def jal_instruction(self, operand):
        self.register["R7"] = self.program_counter + 4
        self.program_counter = operand * 4
        print(f"Value {self.program_counter + 4} saved at register R7, program counter set to {operand * 4}")

    def lw_instruction(self, target, offset):
        self.register[target] = self.memory.fetch_data(offset)
        print(f"Value {self.register[target]} saved at register {target} from memory location {offset}")

    def sw_instruction(self, target, offset):
        self.memory.update_address(offset, target)
        print(f"Value at {offset} updated to {target}")
    
    def cache_instruction(self, code):
        if code == 2:
            self.cache.flush_cache()
        else:
            self.cache_flag = code
            print(f"Cache set to {'On' if self.cache_flag == 1 else 'Off'}")
    
    def parse_instruction(self, instruction):
        return instruction.split(",")