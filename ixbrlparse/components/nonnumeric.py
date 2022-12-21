from copy import deepcopy
from typing import Any, Dict, List, Optional, Union

from ixbrlparse.components import ixbrlContext

from .transform import get_format, ixbrlFormat


class ixbrlNonNumeric:
    def __init__(
        self,
        context: Union[ixbrlContext, str, None],
        name: str,
        format_: Optional[str],
        value: str,
        ixt: Optional[str],
    ) -> None:

        name_split: List[str] = name.split(":", maxsplit=1)
        if len(name_split) == 2:
            self.schema = name_split[0]
            self.name = name_split[1]
        else:
            self.schema = "unknown"
            self.name = name_split[0]

        self.text = value
        self.context = context
        self.format = format_
        self.value = value

        format_ = {
            "format_": self.format,
            "numeric": False,
            "decimals": None,
            "scale": None,
            "sign": None,
            "ixt": ixt,
        }
        self.format: Optional[ixbrlFormat] = get_format(format_["format_"])(**format_)

        try:
            if isinstance(self.format, ixbrlFormat):
                self.value = self.format.parse_value(self.text)
        except ValueError:
            print(value)
            raise

    def to_json(self) -> Dict[str, Any]:
        values = deepcopy(self.__dict__)
        if isinstance(values.get("format"), ixbrlFormat):
            values["format"] = values["format"].to_json()
        if isinstance(self.context, ixbrlContext):
            values["context"] = self.context.to_json()
        return values
