"""file that stores exceptions"""


class NonRequiredParamsMustHaveDefault(Exception):
    """for when the user does nto specify default for a non required parameter"""


class InvalidSid(Exception):
    """sid invalid"""


class NamesMustBeAlphanumeric(Exception):
    """for when command name is not alphanumeric"""


class MustBeRunOnReplitForButtons(Exception):
    """you must be on replit to run bot for now"""
