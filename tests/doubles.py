from src.desconto import IDesconto


class StubSemDesconto(IDesconto):
    def calcular(self, valor: float) -> float:
        return 0.0


class StubShip:
    """Stub para a nave espacial em testes unitários."""

    def __init__(self) -> None:
        self.moving_right: bool = False
        self.moving_left: bool = False
        self.x: float = 100.0

    def update(self) -> None:
        if self.moving_right:
            self.x += 1.5
        if self.moving_left:
            self.x -= 1.5
