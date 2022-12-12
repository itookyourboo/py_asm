class _Exception(Exception):
    pass


class UndefinedInstruction(_Exception):
    pass


class UndefinedLOC(_Exception):
    pass


class UnexpectedOperand(_Exception):
    pass


class UnexpectedArguments(_Exception):
    pass
