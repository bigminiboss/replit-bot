from typing import Dict, Any


class JSDict:
    def __init__(self, pyDict: Dict[str, Any]) -> None:
        for key in pyDict:
            setattr(self, key, pyDict[key])

    def __delitem__(self, key: str) -> None:
        delattr(self, key)

    def __setitem__(self, key, val) -> None:
        setattr(self, key, val)
