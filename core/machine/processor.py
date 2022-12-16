"""
Executing object file
"""
from typing import Iterator, Optional

from core.machine.arithmetic import ALU
from core.machine.clock import ClockGenerator
from core.exceptions import ProgramExit
from core.machine.instructions import InstructionController
from core.machine.io import IOController
from core.machine.memory import MemoryController
from core.model import Program, TextSection, Instruction
from core.machine.registers import RegisterController


class ProgramExecutor:
    def __init__(self, program: Program) -> None:
        self.current_instruction: Optional[Instruction] = None
        self.program = program
        self.clock = ClockGenerator()
        self.alu = ALU()
        self.io = IOController()
        self.r_controller = RegisterController()
        self.m_controller = MemoryController(program.data.memory)
        self.instruction_executor = InstructionController(
            self.clock,
            self.alu,
            self.io,
            self.m_controller,
            self.r_controller
        )

    def execute(self) -> Iterator['ProgramExecutor']:
        code: TextSection = self.program.text

        while (
                (pointer := self.r_controller.get_instruction_pointer())
                < len(code.lines)
        ):
            try:
                self.current_instruction = code.lines[pointer]
                self.instruction_executor.execute(self.current_instruction)
                yield self
            except ProgramExit:
                yield self
                return
