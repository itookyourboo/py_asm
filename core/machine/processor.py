"""
Executing object file
"""
from core.machine.arithmetic import ALU
from core.machine.clock import ClockGenerator
from core.exceptions import ProgramExit
from core.machine.instructions import InstructionController
from core.machine.memory import MemoryController
from core.model import Program, TextSection
from core.machine.registers import RegisterController


class ProgramExecutor:
    def __init__(self, program: Program) -> None:
        self.program = program
        self.clock = ClockGenerator()
        self.alu = ALU()
        self.r_controller = RegisterController()
        self.m_controller = MemoryController(program.data.data)
        self.instruction_executor = InstructionController(
            self.clock,
            self.alu,
            self.m_controller,
            self.r_controller
        )

    def execute(self) -> None:
        code: TextSection = self.program.text

        while (
                (pointer := self.r_controller.get_instruction_pointer())
                < len(code.lines)
        ):
            try:
                instruction = code.lines[pointer]
                print(str(instruction))
                self.instruction_executor.execute(instruction)

                print('Registers:', self.r_controller)
                print('ALU', self.alu)
                print('Memory:', self.m_controller)
            except ProgramExit:
                break
        print('Program finished')
