from classes.menu import Menu
import classes.utils as const


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.menu_button.play()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.draw_background()
            self.game.draw_text('Creditos', 83, const.screen_width / 2, const.screen_height / 2 - 250, const.dark_blue)
            self.game.draw_text('Creditos', 80, const.screen_width / 2, const.screen_height / 2 - 250, const.black)
            self.game.draw_text('Breno Ferreira Pinho          ( 41932110 )', 40, const.screen_width / 2, const.screen_height / 2 + 55, const.black)
            self.game.draw_text('Bruno Nardelli Santiago   ( 41933613 )', 40, const.screen_width / 2, const.screen_height / 2 + 100, const.black)
            self.game.draw_text('Daphne Nanni Rodrigues    ( 32123655 )', 40, const.screen_width / 2, const.screen_height / 2 + 150, const.black)
            self.blit_screen()
