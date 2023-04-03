from typing import Any

from typing_extensions import Annotated

str255 = Annotated[str, 255]
json = dict[str, Any]
