from typing import Dict, Any


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.values: Dict[str, Any] = {}
        self.mutable: set[str] = set()   # track which variables are mutable

    def define(self, name: str, value: Any, is_mut: bool = False):
        self.values[name] = value
        if is_mut:
            self.mutable.add(name)

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(name)

    def assign(self, name: str, value: Any):
        if name in self.values:
            if name not in self.mutable:
                raise RuntimeError(f"Cannot assign to immutable variable '{name}'")
            self.values[name] = value
            return
        if self.parent:
            return self.parent.assign(name, value)
        raise NameError(name)