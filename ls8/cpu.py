"""CPU functionality."""

import sys

# op codes
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4 # stack pointer
        self.pc = 0
        self.fl = 0
        self.halt = False

    def load(self, file_to_load):
        """Load a program into memory."""

        address = 0
        try:
            with open(file_to_load) as my_file:
                for line in my_file:
                    comment_split = line.split('#')
                    maybe_binary_number = comment_split[0]
                    try:
                        x = int(maybe_binary_number, 2)
                        self.ram_write(x, address)
                        address += 1
                    except:
                        continue
                    
        except FileNotFoundError:
            print('file not found...')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def execute_command(self, command_to_execute, operand_a, operand_b):
        program_counter_increment = ((command_to_execute >> 6) & 0b11) + 1
        if command_to_execute == HLT:
            self.halt = True
            self.pc += program_counter_increment
        elif command_to_execute == PRN:
            print(self.registers[operand_a])
            self.pc += program_counter_increment
        elif command_to_execute == LDI:
            self.registers[operand_a] = operand_b
            self.pc += program_counter_increment
        elif command_to_execute == MUL:
            self.registers[operand_a] *= self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == POP:
            self.registers[operand_a] = self.ram[self.registers[7] + 1]
            self.registers[7] += 1
            self.pc += program_counter_increment
        elif command_to_execute == PUSH:
            self.ram[self.registers[7]] = self.registers[operand_a]
            self.registers[7] -= 1
            self.pc += program_counter_increment
    def run(self):
        """Run the CPU."""
        while not self.halt:
            command_to_execute = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            self.execute_command(command_to_execute, operand_a, operand_b)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
    


            

