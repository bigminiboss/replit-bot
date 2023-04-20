"""File that stores exceptions"""


class NonRequiredParamsMustHaveDefault(Exception):
    """For when the user does not specify default for a non required parameter"""


class InvalidSid(Exception):
    """SID invalid"""


class NamesMustBeAlphanumeric(Exception):
    """For when command name is not alphanumeric"""


class MustBeRunOnReplitForButtons(Exception):
    """You must be on replit to run bot for now, if you want buttons"""
