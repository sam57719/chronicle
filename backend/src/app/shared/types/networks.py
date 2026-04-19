from typing import Annotated, Literal

from pydantic import IPvAnyAddress, IPvAnyNetwork, ValidateAs

type ValidatedNetworkHostStr = Annotated[
    str, ValidateAs(IPvAnyAddress | IPvAnyNetwork | Literal["localhost"], str)
]
