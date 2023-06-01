from classes.menu import Menu
import classes.utils as const


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Controles'
        self.controlsx, self.controlsy = self.screen_width_mid, self.screen_height_mid + 55
        self.volx, self.voly = self.screen_width_mid, self.screen_height_mid + 100
        self.backx, self.backy = self.screen_width_mid, self.screen_height_mid + 150
        self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.draw_background()
            self.game.draw_text('Opcoes    ( Em Breve )', 81, const.screen_width / 2, const.screen_height / 2 - 250, const.dark_blue)
            self.game.draw_text('Opcoes    ( Em Breve )', 80, const.screen_width / 2, const.screen_height / 2 - 250, const.black)
            self.game.draw_text('Volume', 40, self.volx, self.voly, (0, 0, 0))
            self.game.draw_text('Controles', 40, self.controlsx, self.controlsy, (0, 0, 0))
            self.game.draw_text('Voltar', 40, self.backx, self.backy, (0, 0, 0))
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Controles':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volume'
            elif self.state == 'Volume':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy)
                self.state = 'Voltar'
            elif self.state == 'Voltar':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controles'
        elif self.game.UP_KEY:
            if self.state == 'Controles':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy)
                self.state = 'Voltar'
            elif self.state == 'Volume':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controles'
            elif self.state == 'Voltar':
                self.menu_button.play()
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volume'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Controles':
                self.menu_button.play()
                print("controles")
            elif self.state == 'Volume':
                self.menu_button.play()
                print("volume")
            elif self.state == 'Voltar':
                self.menu_button.play()
                self.game.curr_menu = self.game.main_menu
            self.run_display = False
