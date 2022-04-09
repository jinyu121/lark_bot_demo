from pathlib import Path
from random import sample
from typing import List, Union


class LipsumDatabase:
    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)
        self.data = self.path.read_text().split('\n')

    def get(self, n: int = 1) -> List[str]:
        return sample(self.data, n)
