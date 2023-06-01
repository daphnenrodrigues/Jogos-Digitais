from classes.menu import Menu
import classes.utils as const


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Iniciar'
        self.startx, self.starty = self.screen_width_mid, self.screen_height_mid + 55
        self.optionsx, self.optionsy = self.screen_width_mid, self.screen_height_mid + 100
        self.creditsx, self.creditsy = self.screen_width_mid, self.screen_height_mid + 150
        self.exitsx, self.exitsy = self.screen_width_mid, self.screen_height_mid + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.draw_background()
            self.game.draw_text('Survive Nature', 82, const.screen_width / 2, const.screen_height / 2 - 250, const.dark_blue)
            self.game.draw_text('Survive Nature', 80, const.screen_width / 2, const.screen_height / 2 - 250, const.black)
            self.game.draw_text('Iniciar', 40, self.startx, self.starty, (0, 0, 0))
            self.game.draw_text('Opcoes', 40, self.optionsx, self.optionsy, (0, 0, 0))
            self.game.draw_text('Creditos', 40, self.creditsx, self.creditsy, (0, 0, 0))
            self.game.draw_text('Sair', 40, self.exitsx, self.exitsy, (0, 0, 0))
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Iniciar':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Opcoes'
            elif self.state == 'Opcoes':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Creditos'
            elif self.state == 'Creditos':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.exitsx + self.offset, self.exitsy)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Iniciar'
        elif self.game.UP_KEY:
            if self.state == 'Iniciar':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.exitsx + self.offset, self.exitsy)
                self.state = 'Sair'
            elif self.state == 'Opcoes':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Iniciar'
            elif self.state == 'Creditos':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Opcoes'
            elif self.state == 'Sair':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Creditos'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Iniciar':
                self.menu_button.play()
                self.game.playing = True
            elif self.state == 'Opcoes':
                self.menu_button.play()
                self.game.curr_menu = self.game.options
            elif self.state == 'Creditos':
                self.menu_button.play()
                self.game.curr_menu = self.game.credits
            elif self.state == 'Sair':
                self.menu_button.play()
                self.game.running = False
            self.run_display = False
