from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class _Node:
    edges: dict[str, int] = field(default_factory=dict)
    fail: int = 0
    outputs: list[str] = field(default_factory=list)


class AhoMatcher:
    """Small deterministic Aho-Corasick matcher for repository reference scans."""

    def __init__(self, patterns: Iterable[str]):
        self.nodes = [_Node()]
        for pattern in sorted(set(patterns)):
            self._add(pattern)
        self._build()

    def _add(self, pattern: str) -> None:
        state = 0
        for character in pattern:
            state = self.nodes[state].edges.setdefault(character, len(self.nodes))
            if state == len(self.nodes):
                self.nodes.append(_Node())
        self.nodes[state].outputs.append(pattern)

    def _build(self) -> None:
        queue: deque[int] = deque()
        for child in self.nodes[0].edges.values():
            queue.append(child)
        while queue:
            state = queue.popleft()
            for character, child in self.nodes[state].edges.items():
                queue.append(child)
                fallback = self.nodes[state].fail
                while fallback and character not in self.nodes[fallback].edges:
                    fallback = self.nodes[fallback].fail
                self.nodes[child].fail = self.nodes[fallback].edges.get(character, 0)
                self.nodes[child].outputs.extend(self.nodes[self.nodes[child].fail].outputs)

    def finditer(self, text: str):
        state = 0
        for index, character in enumerate(text):
            while state and character not in self.nodes[state].edges:
                state = self.nodes[state].fail
            state = self.nodes[state].edges.get(character, 0)
            for pattern in self.nodes[state].outputs:
                yield index - len(pattern) + 1, pattern
