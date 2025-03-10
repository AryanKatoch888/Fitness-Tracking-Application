from auth import AuthApp
from fit import FitnessApp
from splash import SplashApp


class NavigationManager:
    def __init__(self, root):
        self.root = root
        
    def show_login(self):
        AuthApp(self.root, self)

    def show_splash(self):
        SplashApp(self.root, self)
    
    def show_fitness_app(self):
        FitnessApp(self.root)
        
