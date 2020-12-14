"""CPU functionality."""

import sys

# op codes
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000 
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4 # stack pointer
        self.pc = 0
        self.fl = 0b00000000
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
            address = self.registers[7]
            self.registers[operand_a] = self.ram_read(address)
            self.registers[7] += 1
            self.pc += program_counter_increment
        elif command_to_execute == PUSH:
            self.registers[7] -= 1
            value = self.registers[operand_a]
            address = self.registers[7]
            self.ram_write(value, address)
            self.pc += program_counter_increment
        elif command_to_execute == CALL:
            self.registers[7] -= 1
            value = self.pc + 2
            address = self.registers[7]
            self.ram_write(value, address)
            self.pc = self.registers[operand_a]
        elif command_to_execute == RET:
            self.pc = self.ram[self.registers[7]]
            self.registers[7] += 1
        elif command_to_execute == ADD:
            self.registers[operand_a] += self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == CMP:
            if self.registers[operand_a] == self.registers[operand_b]:
                self.fl = self.fl | 0b00000001
            elif self.registers[operand_a] < self.registers[operand_b]:
                self.fl = self.fl | 0b00000100
            elif self.registers[operand_a] > self.registers[operand_b]:
                self.fl = self.fl | 0b00000010
            self.pc += program_counter_increment
        elif command_to_execute == JMP:
            address_to_jump_to = self.registers[operand_a]
            self.pc = address_to_jump_to
        elif command_to_execute == JEQ:
            if self.fl & 0b1 == 1:
                address_to_jump_to = self.registers[operand_a]
                self.pc = address_to_jump_to
            else:
                self.pc += program_counter_increment
        elif command_to_execute == JNE:
            if self.fl & 0b1 == 0:
                address_to_jump_to = self.registers[operand_a]
                self.pc = address_to_jump_to
            else:
                self.pc += program_counter_increment
        elif command_to_execute == AND:
            self.registers[operand_a] = self.registers[operand_a] & self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == OR:
            self.registers[operand_a] = self.registers[operand_a] | self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == XOR:
            self.registers[operand_a] = self.registers[operand_a] ^ self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == NOT:
            self.registers[operand_a] = self.registers[operand_a] ~ self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == SHL:
            self.registers[operand_a] = self.registers[operand_a] << self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == SHR:
            self.registers[operand_a] = self.registers[operand_a] >> self.registers[operand_b]
            self.pc += program_counter_increment
        elif command_to_execute == MOD:
            try:
                self.registers[operand_a] = self.registers[operand_a] % self.registers[operand_b]
            except:
                print('Error, cannot divide by 0')
                self.halt = True
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
    


            

