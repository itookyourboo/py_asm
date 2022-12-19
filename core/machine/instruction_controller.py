"""
Instruction Executor Unit
"""
import operator
from typing import Callable, Optional

from core.machine.alu import ALU, Flag
from core.machine.clock import ClockGenerator
from core.exceptions import (
    OperandIsNotWriteable, ProgramExit, NotEnoughOperands
)
from core.machine.io_controller import IOController
from core.machine.memory_controller import MemoryController
from core.model import (
    Address, Register, Label, Operand, Instruction,
    Destination, Source, IndirectAddress
)
from core.machine.register_controller import RegisterController


class InstructionController:
    """
    Instruction Controller class
        - current   -- the current executing instruction
    """

    def __init__(
            self,
            clock: ClockGenerator,
            alu: ALU,
            io_controller: IOController,
            memory: MemoryController,
            registers: RegisterController
    ) -> None:
        self.current: Optional[Instruction] = None
        self.clock = clock
        self.alu = alu
        self.io_controller = io_controller
        self.memory = memory
        self.registers = registers

    def get_operand_value(self, operand: Operand) -> int:
        """
        Get operand value.
            - Indirect Address: shift address and work like with direct
            - Direct Address: get value with MemoryController
            - Register: get value with RegisterController
            - Label: get index
            - Constant: just get value
        """
        if isinstance(operand, IndirectAddress):
            return self.memory.get(
                Address(
                    label=operand.label,
                    value=(
                            operand.value +
                            self.get_operand_value(operand.offset)
                    )
                )
            )
        if isinstance(operand, Address):
            return self.memory.get(operand)
        if isinstance(operand, Register):
            return self.registers.get(operand)
        return operand.value

    def set_operand_value(self, operand: Operand, value: int) -> None:
        """
        Set operand value.
            - Indirect Address: shift address and work like with direct
            - Direct Address: set value with MemoryController
            - Register: set value with RegisterController
            - Other: throw OperandIsNotWriteable
        """
        if isinstance(operand, IndirectAddress):
            self.memory.set(
                Address(
                    label=operand.label,
                    value=(
                            operand.value +
                            self.get_operand_value(operand.offset)
                    )),
                value
            )
        elif isinstance(operand, Address):
            self.memory.set(operand, value)
        elif isinstance(operand, Register):
            self.registers.set(operand, value)
        else:
            raise OperandIsNotWriteable(operand.value)

    def jump_to(self, label: Label) -> None:
        """
        Set instruction pointer to label value
        """
        self.registers.set_instruction_pointer(label.value - 1)

    def _reduce_op(
            self,
            reducer: Callable,
            dest: Destination,
            *operands: Source
    ) -> None:
        """
        Defines operation behavior applying reducer function to operands
            - Two operands.
                Apply reducer to them and save result into "dest"
            - Three and more operands.
                Apply reducer to "*operands" and save result into "dest"
        """
        op_count: int = len(operands)
        if op_count < 1:
            raise NotEnoughOperands

        result: int
        if op_count == 1:
            # First case:
            #   ADD OP1, OP2
            #   OP1 + OP2 --> OP1
            result = self.get_operand_value(dest)
        else:
            # Second case:
            #   ADD DEST, OP1, OP2, ...
            #   OP1 + OP2 + ... -> DEST
            result = self.get_operand_value(operands[0])
            operands = operands[1:]

        # get_operand_value -> tick
        self.clock.tick()

        for operand in operands:
            operand_value: int = self.get_operand_value(operand)
            # send data to ALU and get result
            result = self.alu.operation(reducer, result, operand_value)
            # apply operation -> tick
            self.clock.tick()

        self.set_operand_value(dest, result)

    def _jmp_if(self, label: Label, condition: bool) -> None:
        """
        Jump to label if condition is True
        """
        self.clock.tick()
        if condition:
            self.jump_to(label)

    def i_add(self, dest: Destination, *ops: Source) -> None:
        """
        ADD dest, *ops

        Sum operands amd save into dest
            - ADD A, B
                A = A + B
            - ADD A, B, C, D
                A = ((B + C) + D)
        """
        self._reduce_op(operator.add, dest, *ops)

    def i_sub(self, dest: Destination, *ops: Source) -> None:
        """
        SUB dest, *ops

        Subtract operands amd save into dest.
            - SUB A, B
                A = A - B
            - SUB A, B, C, D
                A = ((B - C) - D)
        """
        self._reduce_op(operator.sub, dest, *ops)

    def i_mul(self, dest: Destination, *ops: Source) -> None:
        """
        MUL dest, *ops

        Multiply operands amd save into dest
            - MUL A, B
                A = A * B
            - MUL A, B, C, D
                A = ((B * C) * D)
        """
        self._reduce_op(operator.mul, dest, *ops)

    def i_div(self, dest: Destination, *ops: Source) -> None:
        """
        DIV dest, *ops

        Divide (floor) operands amd save into dest.
            - DIV A, B
                A = A / B
            - DIV A, B, C, D
                A = ((B / C) / D)

        Can raise ALUDZeroDivisionError
        """
        self._reduce_op(operator.floordiv, dest, *ops)

    def i_mod(self, dest: Destination, *ops: Source) -> None:
        """
        MOD dest, *ops

        Modulo divide operands amd save into dest.
            - MOD A, B
                A = A % B
            - MOD A, B, C, D
                A = ((B % C) % D)

        Can raise ALUDZeroDivisionError
        """
        self._reduce_op(operator.mod, dest, *ops)

    def i_xor(self, dest: Destination, *ops: Source) -> None:
        """
        XOR dest, *ops

        Apply logical XOR to operands amd save into dest
            - XOR A, B
                A = A ^ B
            - XOR A, B, C, D
                A = ((B ^ C) ^ D)
        """
        self._reduce_op(operator.xor, dest, *ops)

    def i_and(self, dest: Destination, *ops: Source) -> None:
        """
        AND dest, *ops

        Apply logical AND to operands amd save into dest
            - AND A, B
                A = A & B
            - AND A, B, C, D
                A = ((B & C) & D)
        """
        self._reduce_op(operator.and_, dest, *ops)

    def i_or(self, dest: Destination, *ops: Source) -> None:
        """
        OR dest, *ops

        Apply logical OR to operands amd save into dest
            - OR A, B
                A = A | B
            - OR A, B, C, D
                A = ((B | C) | D)
        """
        self._reduce_op(operator.or_, dest, *ops)

    def i_dec(self, dest: Destination) -> None:
        """
        DEC dest

        Decrement (-1) operand
        """
        self.set_operand_value(dest, self.get_operand_value(dest) - 1)

    def i_inc(self, dest: Destination) -> None:
        """
        INC dest

        Increment (+1) operand
        """
        self.set_operand_value(dest, self.get_operand_value(dest) + 1)

    def i_jmp(self, label: Label) -> None:
        """
        JMP label

        Jump to label without condition
        """
        self.jump_to(label)

    def i_je(self, label: Label) -> None:
        """
        JE label

        Jump to label if Z Flag is set (operands are equal)
        """
        self._jmp_if(
            label,
            self.alu.get_flag(Flag.Z)
        )

    def i_jne(self, label: Label) -> None:
        """
        JE label

        Jump to label if Z Flag is not set (operands are not equal)
        """
        self._jmp_if(
            label,
            not self.alu.get_flag(Flag.Z)
        )

    def i_jl(self, label: Label) -> None:
        """
        JL label

        Jump to label if N Flag is set (first < second)
        """
        self._jmp_if(
            label,
            self.alu.get_flag(Flag.N)
        )

    def i_jg(self, label: Label) -> None:
        """
        JL label

        Jump to label if N Flag is not set (first > second)
        """
        self._jmp_if(
            label,
            not self.alu.get_flag(Flag.N)
        )

    def i_jle(self, label: Label) -> None:
        """
        JLE label

        Jump to label if Z or N flag is set (first <= second)
        """
        self._jmp_if(
            label,
            (
                    self.alu.get_flag(Flag.Z)
                    or
                    self.alu.get_flag(Flag.N)
            )
        )

    def i_jge(self, label: Label) -> None:
        """
        JGE label

        Jump to label if Z or not N flag is set (first >= second)
        """
        self._jmp_if(
            label,
            (
                    self.alu.get_flag(Flag.Z)
                    or
                    not self.alu.get_flag(Flag.N)
            )
        )

    def i_mov(self, dest: Destination, src: Source) -> None:
        """
        MOV dest, src

        Move value from src to dest
        """
        self.set_operand_value(dest, self.get_operand_value(src))

    def i_ld(
            self,
            register: Register,
            address: Address | IndirectAddress
    ) -> None:
        """
        LD register, address

        Load data by address to register
        """
        self.set_operand_value(register, self.get_operand_value(address))

    def i_cmp(self, var: Source, src: Source) -> None:
        """
        CMP op1, op2

        Compare two operands by subtracting and set flags
        """
        self.alu.operation(
            operator.sub,
            self.get_operand_value(var),
            self.get_operand_value(src)
        )

    def i_putc(self, src: Source) -> None:
        """
        PUTC src

        Write single into stdout
        """
        self.io_controller.putc(self.get_operand_value(src))

    def i_getc(self, dest: Destination) -> None:
        """
        GETC dest

        Read single char from stdout
        """
        self.set_operand_value(dest, self.io_controller.getc())

    def i_putn(self, src: Source) -> None:
        """
        PUTN src

        Write number into stdout
        """
        self.io_controller.putn(self.get_operand_value(src))

    def i_getn(self, dest: Destination) -> None:
        """
        GETN dest

        Read number from stdout
        """
        self.set_operand_value(dest, self.io_controller.getn())

    def i_hlt(self) -> None:
        """
        HLT

        Stop execution
        """
        raise ProgramExit

    def execute(self, instruction: Instruction) -> None:
        """
        Execute instruction by its name
        """
        self.current = instruction
        name: str = self.current.name
        # map needed function by name and call it
        self.get_all()[name](self, *instruction.operands)
        # increment instruction pointer (next instruction)
        self.registers.set_instruction_pointer(
            self.registers.get_instruction_pointer() + 1
        )
        # increment ticks and instructions after execution
        self.clock.tick()
        self.clock.inst()

    @classmethod
    def get_all(cls) -> dict[str, Callable]:
        """
        Get dict with available instruction
        :return {instruction_name: instruction_executor_function}
        """
        return {
            key.replace('i_', ''): func
            for key, func in cls.__dict__.items()
            if key.startswith('i_')
        }
