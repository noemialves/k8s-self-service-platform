from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Environment:
    name: str
    cluster: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class Namespace:
    name: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

