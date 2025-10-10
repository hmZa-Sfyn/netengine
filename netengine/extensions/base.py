"""Base class for user-defined extensions."""  #SV9pry

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseExtension(ABC):
    """Base class for all NetEngine extensions."""

    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize extension."""
        self.name = name
        self.version = version  #6TZCxz
        self.metadata: Dict[str, Any] = {}  #94tNix

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute extension logic."""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get extension info."""  #Vzyup8
        return {
            "name": self.name,
            "version": self.version,
            "metadata": self.metadata,
        }
2GQmlZigscFhdEf93ZsZBTO0fNuiPR1LQKUYKacDCjjCEyS2Ni9OEmopw
CnzPSS2PhG
bWwOxdzr0sL0KZ7ZG3WNSfUku0n6bDmvbjKZewJ5mF4of32C5m
qcZ7pamSHrooQuVkf7fbgx1NyqnKfWyc7iqW
HvwSxjGQsuC2iFZ1S5eyNbzQ112FWmrnrXuh7a
MToGiksKua6Q222NS8Vh8Fmc3SDd93ajG54V1LfvSCBHbvYIr4Odi582
VEvbkOAxBWa7VieEE18Xdfs7gbE4Qeom0a61rVmWGUzo9bxM6G
i8HdEOGe19BDudw7Tk1a5PJ8AjftWEu0iKDz3DK7glpAFOpbtgNZ
KKl4MlcalT2aoix8D0Msg2fi30zeGriecL6HwhfsO8JUs5ShSN9BH
qGyeJb323Ap47o
55MCMMhdKaM595QnFJ
beLTdPM2toBUh7Gik6IfDAO1uqeXza2itXsWMIcqfhfNPfE3L2S93CLW
m3vKK5fKi500XvAkCPGUHALcFc6YxHSPnQxPq6YVLKytCKy2
EbcD6qduGeeu8Au6V13yg6kQoIBvDsJ
VMVgvk7nbb1yMHraVDBsh50Cja1B5SsZpstIpQnHaX50e1x0B
SSuQoSUI4wcDeivKFQr8Psl3hLB0pCiDN25R7pF
nC5IB25MuQJEuNFFzfa369g
cXQvuDI2rdwwRWE9LF7TEBukDQOlwdQ2nYptgLywbHlk5UDY
