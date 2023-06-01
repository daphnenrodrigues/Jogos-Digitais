class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # Pegando a posição do mouse
        pos = pygame.mouse.get_pos()

        # Verificar as condições de clicar e se ele está em cima do botão
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Adicionar botão na tela
        Game.screen.blit(self.image, self.rect)

        return action