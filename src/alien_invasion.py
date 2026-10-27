import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Gerencia o jogo e seus comportamentos."""

    def __init__(self) -> None:
        """Construtor da classe que inicializa o jogo e cria os recursos básicos"""
        pygame.init()
        self.settings: Settings = Settings()

        self.screen: pygame.Surface = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Criando uma instância da classe Ship para representar a nave espacial
        self.ship: Ship = Ship(self.screen, self.settings)

        # Mudando a cor do plano de fundo em RGB
        self.bg_color: tuple[int, int, int] = self.settings.bg_color

        self.bullets: pygame.sprite.Group = pygame.sprite.Group()  # Cria um grupo para armazenar os projéteis disparados pela nave

        self.aliens: pygame.sprite.Group = pygame.sprite.Group()  # Cria um grupo para armazenar os alienígenas presentes no jogo

    def create_fleet(self) -> None:
        """Cria uma frota de alienígenas."""
        # Cria um alienígena e calcula o número de alienígenas em uma linha
        # O espaçamento entre os alienígenas é igual a um alienígena
        alien = Alien(self.screen, self.settings)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            # Cria a primeira linha de alienígenas
            for alien_number in range(number_aliens_x):
                # Cria um alienígena e o posiciona na linha
                alien = Alien(self.screen, self.settings)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = int(alien.x)
                alien.y = alien_height + 2 * alien_height * row_number
                alien.rect.y = int(alien.y)
                self.aliens.add(alien)

    def run_game(self) -> None:
        """Cria um laço de repetição para a tela sempre ficar visível até
        que o usuário decida fechar a janela."""

        self.create_fleet()  # Cria a frota de alienígenas para ser desenhada na tela

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # Detecta quando uma tecla é pressionada
                    if event.key == pygame.K_RIGHT:  # Verifica se a tecla pressionada é a seta para a direita
                        self.ship.moving_right = True
                    elif event.key == pygame.K_LEFT:  # Verifica se a tecla pressionada é a seta para a esquerda
                        self.ship.moving_left = True
                    elif event.key == pygame.K_SPACE:  # Verifica se a tecla pressionada é a barra de espaço
                        if len(self.bullets) < self.settings.bullet_allowed:  # Verifica se o número de projéteis na tela excede o limite permitido
                            new_bullet = Bullet(self.screen, self.settings, self.ship)  # Cria um novo projétil
                            self.bullets.add(new_bullet)  # Adiciona o novo projétil ao grupo de projéteis

                elif event.type == pygame.KEYUP:  # Detecta quando uma tecla é liberada
                    if event.key == pygame.K_RIGHT:  # Verifica se a tecla liberada é a seta para a direita
                        self.ship.moving_right = False
                    elif event.key == pygame.K_LEFT:  # Verifica se a tecla liberada é a seta para a esquerda
                        self.ship.moving_left = False

            # Redesenha a tela a cada passagem pelo laço
            self.screen.fill(self.bg_color)

            # Redesenha a nave em sua posição atual
            self.ship.blitme()

            # Desenha os alienígenas presentes no grupo de alienígenas na tela
            self.aliens.draw(self.screen)

            # Atualiza a posição da nave com base na variável de controle
            self.ship.update()

            for bullet in self.bullets.sprites():  # Atualiza a posição de cada projétil no grupo de projéteis
                bullet.draw_bullet()  # Desenha cada projétil na tela

            self.bullets.update()  # Atualiza a posição de cada projétil no grupo de projéteis
            for bullet in self.bullets.copy():  # Verifica se algum projétil saiu da tela
                if bullet.rect.bottom <= 0:  # Se o projétil saiu da tela
                    self.bullets.remove(bullet)  # Remove o projétil do grupo de projéteis

            # Verifica as colisões entre os projéteis e os alienígenas
            pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

            for alien in self.aliens.sprites():
                if alien.check_edges():  # Verifica se algum alienígena atingiu a borda da tela
                    for alien in self.aliens.sprites():  # Atualiza a posição de cada alienígena no grupo de alienígenas
                        alien.rect.y += self.settings.fleet_drop_speed  # Move cada alienígena para baixo
                    self.settings.fleet_direction *= -1  # Inverte a direção da frota
                    break

            # Torna visível a tela mais recente
            pygame.display.flip()

            self.bullets.update()
            self.aliens.update()

            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                print("A nave foi atingida!")
                sys.exit()

if __name__ == '__main__':
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
