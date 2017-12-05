"""
Exceptions need separate module to avoid cyclic dependencies.
"""


class ReputeeNotFoundError(Exception):
    pass


class RidDuplicateError(Exception):
    pass