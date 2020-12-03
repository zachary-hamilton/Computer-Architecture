"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 8
        self.register = [0] * 8
        self.op_codes = {'LDI': 0b10000010,
                            'PRN': 0b01000111,
                            'HLT': 0b00000001}

    def ram_read(self, address):
        '''Prints the given ram address'''
        print(self.ram[address])

    def ram_write(self, address, value):
        '''Writes a value to a specified ram address'''
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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

    def run(self):
        """Run the CPU."""
        running = True
        program_counter = 0
        #register = [0] * 8
        while running:
            command_to_execute = self.ram[program_counter]

            if command_to_execute == self.op_codes['HLT']:
                running = False
                program_counter += 1
            elif command_to_execute == self.op_codes['LDI']:
                value_to_save = self.ram[program_counter + 2]
                register_to_save_it_in = self.ram[program_counter + 1]
                self.register[register_to_save_it_in] = value_to_save
                program_counter += 3
            elif command_to_execute == self.op_codes['PRN']:
                register_to_print = self.register[program_counter + 1]
                print(f'{self.register[register_to_print]}')
                program_counter += 2
            
