from core.model import (
    Instruction, InstructionInfo, Address,
    Register, Constant, Number, Label
)


class InstructionMemory:
    __available_instructions: dict[str, InstructionInfo] = {
        'XOR': InstructionInfo(operand_types={
            (Address | Register, Address | Register | Constant)
        }),
        'ADD': InstructionInfo(operand_types={
            (Address | Register, Address | Register | Number),
            (Address | Register, Address | Register | Number, Address | Register | Number)
        }),
        'AND': InstructionInfo(operand_types={
            (Address | Register, Address | Register | Number)
        }),
        'CALL': InstructionInfo(operand_types={
            (Label,)
        }),
        'CMP': InstructionInfo(operand_types={
            (Address | Register, Address | Register | Constant)
        }),
        'DEC': InstructionInfo(operand_types={
            (Address | Register,)
        }),
        'DIV': InstructionInfo(operand_types={
            (Address | Register, Address | Register | Number)
        }),
        'INC': InstructionInfo(operand_types={
            (Address | Register,)
        }),
        'MOV': InstructionInfo(operand_types={
            (Register | Address, Register | Address | Constant)
        }),
        'LD': InstructionInfo(operand_types={
            (Register, Address)
        }),
        'RET': InstructionInfo(operand_types={
            (Address | Register, Address | Register | Constant)
        }),
    }

    @classmethod
    def contains(cls, instruction_name: str) -> bool:
        return instruction_name in cls.__available_instructions

    @classmethod
    def get_info(cls, instruction_name: str) -> InstructionInfo:
        return cls.__available_instructions[instruction_name]

    @classmethod
    def get(cls, instruction_name: str) -> Instruction:
        return Instruction(
            name=instruction_name,
            info=cls.__available_instructions[instruction_name]
        )
