import pygame
from tests.doubles import StubSemDesconto, StubShip
from src.desconto import Pedido
from src.game_events import GameEventHandler


def test_pedido_com_stub() -> None:
    pedido = Pedido(StubSemDesconto())
    assert pedido.total(100) == 100


def test_pedido_com_mock_desconto(mocker) -> None:
    mock_desconto = mocker.Mock()
    mock_desconto.calcular.return_value = 10

    pedido = Pedido(mock_desconto)
    resultado = pedido.total(100)

    assert resultado == 90
    mock_desconto.calcular.assert_called()
    mock_desconto.calcular.assert_called_once_with(100)
    assert mock_desconto.calcular.call_count == 1


def test_game_event_handler_com_stub_e_mock(mocker) -> None:
    """Aplica ao menos um stub (StubShip) e um mock (mock_bullet_manager) no Game2D_Alien."""
    stub_ship = StubShip()
    mock_bullet_manager = mocker.Mock()
    event_handler = GameEventHandler(stub_ship, mock_bullet_manager)

    # Testando manipulação de evento com o Stub da nave
    event_right = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
    event_handler._handle_keydown(event_right)
    assert stub_ship.moving_right is True

    # Testando disparo com Mock do BulletManager
    event_space = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
    event_handler._handle_keydown(event_space)
    mock_bullet_manager._fire_bullet.assert_called_once()
