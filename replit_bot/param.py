"""file that stores the Param for type hints

```py
@bot.command(...)
def name(ctx, pass_obj: Param(
    desc="something to pass",
    required=False,
    default="lol"
)):
    ctx.reply(pass_obj)
```
"""

from typing import Any
from .exceptions import NonRequiredParamsMustHaveDefault


class DumbClass:
    def __call__(self, obj):
        return obj


dumb_class = DumbClass()
dumb_class.__name__ = "Any"


class Param:
    """similar to discord.py param type hinting for commands"""

    def __init__(
        self,
        desc: str = "",
        required: bool = None,
        default: Any = None,
        type_cast: Any = dumb_class,
        detect_type: bool = False,
    ) -> None:
        """init"""
        self.desc = desc
        self.required = required
        self.default = default
        self.type_cast = type_cast
        self.detect_type = detect_type
        if not self.required and self.default is None:
            raise NonRequiredParamsMustHaveDefault(
                "no required params must have default"
            )
