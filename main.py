from tkinter import Tk
from nav import NavigationManager
from db_setup import create_database

if __name__ == "__main__":
    create_database()
    root = Tk()
    root.title("Fitness Tracker")
    # app = fitness_app.FitnessApp(root)  # Wrap the fitness tracker in a class
    navigation_manager = NavigationManager(root)
    navigation_manager.show_login()
    # navigation_manager.show_splash()

    root.mainloop()
