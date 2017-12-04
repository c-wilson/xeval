"""
Exceptions need separate module to avoid cyclic dependancies.
"""


class PostError(Exception):
    pass


class GetError(Exception):
    pass


class ReputeeNotFoundError(Exception):
    pass


class RidDuplicateError(Exception):
    pass