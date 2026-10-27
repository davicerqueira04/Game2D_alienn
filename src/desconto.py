import abc


class IDesconto(abc.ABC):
    @abc.abstractmethod
    def calcular(self, valor: float) -> float:
        raise NotImplementedError


class ICupom(abc.ABC):
    @abc.abstractmethod
    def aplicar_cupom(self, codigo: str) -> bool:
        raise NotImplementedError


class IVIP(abc.ABC):
    @abc.abstractmethod
    def validar_usuario_vip(self, usuario: str) -> bool:
        raise NotImplementedError


class DescontoNormal(IDesconto):
    def calcular(self, valor: float) -> float:
        return valor * 0.1


class DescontoVIP(IDesconto, ICupom, IVIP):
    def calcular(self, valor: float) -> float:
        return valor * 0.2

    def aplicar_cupom(self, codigo: str) -> bool:
        return True

    def validar_usuario_vip(self, usuario: str) -> bool:
        return usuario == "vip"


class DescontoPremium(IDesconto):
    def calcular(self, valor: float) -> float:
        return valor * 0.3


class Pedido:
    def __init__(self, desconto: IDesconto) -> None:
        self.desconto = desconto

    def total(self, valor: float) -> float:
        return valor - self.desconto.calcular(valor)


def aplicar_desconto(desconto: IDesconto, valor: float) -> float:
    return desconto.calcular(valor)


if __name__ == "__main__":
    valor = 100.0
    normal = DescontoNormal()
    vip = DescontoVIP()
    premium = DescontoPremium()

    print("Desconto normal:", aplicar_desconto(normal, valor))
    print("Desconto VIP:", aplicar_desconto(vip, valor))
    print("Cupom VIP:", vip.aplicar_cupom("DESC10"))

    pedido_normal = Pedido(normal)
    pedido_vip = Pedido(vip)
    print("Normal:", pedido_normal.total(valor))
    print("VIP:", pedido_vip.total(valor))
