import operator
from typing import Callable

from core.machine.arithmetic import ALU
from core.machine.clock import ClockGenerator
from core.exceptions import (
    ConstantIsNotWriteable, ProgramExit, IncorrectDataType
)
from core.isa import InstructionSet
from core.machine.memory import MemoryController
from core.model import (
    Address, Register, Label, Operand, Instruction,
    Destination, Source
)
from core.machine.registers import RegisterController


class InstructionController(InstructionSet):
    def __init__(
            self,
            clock: ClockGenerator,
            alu: ALU,
            memory: MemoryController,
            registers: RegisterController
    ) -> None:
        self.clock = clock
        self.alu = alu
        self.memory = memory
        self.registers = registers

    def get(self, operand: Operand) -> int | str:
        if isinstance(operand, Address):
            return self.memory.get(operand)
        elif isinstance(operand, Register):
            return self.registers.get(operand)
        return operand.value

    def set(self, operand: Operand, value: int | str) -> None:
        if isinstance(operand, Address):
            self.memory.set(operand, value)
        elif isinstance(operand, Register):
            if not isinstance(value, int):
                raise IncorrectDataType(type(value))
            self.registers.set(operand, value)
        else:
            raise ConstantIsNotWriteable(operand.value)

    def _reduce_op(self, reducer: Callable, *operands: Operand) -> None:
        result: int = self.get(operands[0])
        self.clock.tick()
        for operand in operands:
            operand_value: int = self.get(operand)
            result = self.alu.operation(reducer, result, operand_value)
            self.clock.tick()
        self.set(operands[0], result)

    # @_proxy
    def i_add(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.add, dest, *ops)

    def i_sub(self, dest: Destination, *ops: Source) -> None:
        self._reduce_op(operator.sub, dest, *ops)

    def i_mul(self, dest: Destination, *ops: Source):
        self._reduce_op(operator.mul, dest, *ops)

    def i_div(self, dest: Destination, *ops: Source):
        self._reduce_op(operator.floordiv, dest, *ops)

    def i_xor(self, dest: Destination, *ops: Source):
        self._reduce_op(operator.xor, dest, *ops)

    def i_and(self, dest: Destination, *ops: Source):
        self._reduce_op(operator.and_, dest, *ops)

    def i_or(self, dest: Destination, *ops: Source):
        self._reduce_op(operator.or_, dest, *ops)

    def i_dec(self, dest: Destination):
        self.set(dest, self.get(dest) - 1)

    def i_inc(self, dest: Destination, *ops: Source):
        self.set(dest, self.get(dest) + 1)

    def i_jmp(self, label: Label):
        self.registers.set_instruction_pointer(label.index - 1)

    def i_mov(self, dest: Destination, src: Source):
        self.set(dest, self.get(src))

    def i_ld(self, register: Register, address: Address):
        self.set(register, self.get(address))

    def i_cmp(self, var: Destination, op: Source):
        self.alu.operation(self.i_sub, self.get(var), self.get(op))

    def i_call(self, label: Label):
        pass

    def i_ret(self):
        raise ProgramExit

    def i_hlt(self):
        pass

    def execute(self, instruction: Instruction) -> None:
        name: str = instruction.name
        self.get_all()[name](self, *instruction.operands)
        self.registers.set_instruction_pointer(
            self.registers.get_instruction_pointer() + 1
        )
        self.clock.tick()

    @classmethod
    def get_all(cls) -> dict[str, Callable]:
        return super().get_all()
