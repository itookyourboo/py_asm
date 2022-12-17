import operator
from typing import Callable

from core.machine.arithmetic import ALU, Flag
from core.machine.clock import ClockGenerator
from core.exceptions import (
    ConstantIsNotWriteable, ProgramExit, NotEnoughOperands
)
from core.isa import InstructionSet
from core.machine.io import IOController
from core.machine.memory import MemoryController
from core.model import (
    Address, Register, Label, Operand, Instruction,
    Destination, Source, IndirectAddress
)
from core.machine.registers import RegisterController


class InstructionController(InstructionSet):
    def __init__(
            self,
            clock: ClockGenerator,
            alu: ALU,
            io: IOController,
            memory: MemoryController,
            registers: RegisterController
    ) -> None:
        self.clock = clock
        self.alu = alu
        self.io = io
        self.memory = memory
        self.registers = registers

    def get(self, operand: Operand) -> int:
        if isinstance(operand, IndirectAddress):
            return self.memory.get(
                Address(
                    value=operand.value,
                    index=(
                            operand.index + self.get(operand.offset)
                    )
                )
            )
        elif isinstance(operand, Address):
            return self.memory.get(operand)
        elif isinstance(operand, Register):
            return self.registers.get(operand)
        return operand.value

    def set(self, operand: Operand, value: int | str) -> None:
        if isinstance(operand, IndirectAddress):
            self.memory.set(
                Address(
                    value=operand.value,
                    index=(
                            operand.index + self.get(operand.offset)
                    )),
                value
            )
        elif isinstance(operand, Address):
            self.memory.set(operand, value)
        elif isinstance(operand, Register):
            self.registers.set(operand, value)
        else:
            raise ConstantIsNotWriteable(operand.value)

    def jump_to(self, label: Label) -> None:
        self.registers.set_instruction_pointer(label.index - 1)

    def _reduce_op(self, reducer: Callable, *operands: Operand) -> None:
        op_count: int = len(operands)
        if op_count < 2:
            raise NotEnoughOperands

        dest: Destination
        dest, *ops = operands

        result: int
        if op_count == 2:
            """
            First case: 
                ADD OP1, OP2
                OP1 + OP2 --> OP1
            """
            result = self.get(dest)
        else:
            """
            Second case:
                ADD DEST, OP1, OP2, ...
                OP1 + OP2 + ... -> DEST
            """
            result = self.get(ops[0])
            ops = ops[1:]
        self.clock.tick()

        for op in ops:
            operand_value: int = self.get(op)
            result = self.alu.operation(reducer, result, operand_value)
            self.clock.tick()

        self.set(dest, result)

    def _jmp_if(self, label: Label, condition: bool) -> None:
        self.clock.tick()
        if condition:
            self.jump_to(label)

    # @_proxy
    def i_add(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.add, dest, *ops)

    def i_sub(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.sub, dest, *ops)

    def i_mul(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.mul, dest, *ops)

    def i_div(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.floordiv, dest, *ops)

    def i_mod(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.mod, dest, *ops)

    def i_xor(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.xor, dest, *ops)

    def i_and(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.and_, dest, *ops)

    def i_or(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.or_, dest, *ops)

    def i_dec(self, dest: Destination) -> None:
        self.set(dest, self.get(dest) - 1)

    def i_inc(self, dest: Destination) -> None:
        self.set(dest, self.get(dest) + 1)

    def i_jmp(self, label: Label) -> None:
        self.jump_to(label)

    def i_je(self, label: Label) -> None:
        self._jmp_if(
            label,
            self.alu.get_flag(Flag.Z)
        )

    def i_jne(self, label: Label) -> None:
        self._jmp_if(
            label,
            not self.alu.get_flag(Flag.Z)
        )

    def i_jl(self, label: Label) -> None:
        self._jmp_if(
            label,
            self.alu.get_flag(Flag.N)
        )

    def i_jg(self, label: Label) -> None:
        self._jmp_if(
            label,
            not self.alu.get_flag(Flag.N)
        )

    def i_jle(self, label: Label) -> None:
        self._jmp_if(
            label,
            (
                    self.alu.get_flag(Flag.Z)
                    or
                    self.alu.get_flag(Flag.N)
            )
        )

    def i_jge(self, label: Label) -> None:
        self._jmp_if(
            label,
            (
                    self.alu.get_flag(Flag.Z)
                    or
                    not self.alu.get_flag(Flag.N)
            )
        )

    def i_mov(self, dest: Destination, src: Source) -> None:
        self.set(dest, self.get(src))

    def i_ld(self, register: Register, address: Address | IndirectAddress) -> None:
        self.set(register, self.get(address))

    def i_cmp(self, var: Destination, op: Source) -> None:
        self.alu.operation(operator.sub, self.get(var), self.get(op))

    def i_putc(self, op: Source) -> None:
        self.io.putc(self.get(op))

    def i_getc(self, dest: Destination) -> None:
        self.set(dest, self.io.getc())

    def i_putn(self, op: Source) -> None:
        self.io.putn(self.get(op))

    def i_getn(self, dest: Destination) -> None:
        self.set(dest, self.io.getn())

    def i_hlt(self) -> None:
        raise ProgramExit

    def execute(self, instruction: Instruction) -> None:
        name: str = instruction.name
        self.get_all()[name](self, *instruction.operands)
        self.registers.set_instruction_pointer(
            self.registers.get_instruction_pointer() + 1
        )
        self.clock.tick()
        self.clock.inst()

    @classmethod
    def get_all(cls) -> dict[str, Callable]:
        return super().get_all()
