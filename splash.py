import tkinter as tk


class SplashApp:
    def __init__(self, root, navigation_manager):
        # Initialize splash screen
        self.splash = tk.Tk()
        self.setup_splash()
        self.navigation_manager = navigation_manager
        
        self.run()

    def setup_splash(self):
        """Setup the splash screen window."""
        self.splash.title("Splash Screen")
        self.splash.geometry("400x300")
        self.splash.overrideredirect(True)  # Remove window decorations

        # Add a label or logo
        tk.Label(
            self.splash, 
            text="Loading App...", 
            font=("Arial", 20), 
            fg="blue"
        ).pack(expand=True)

        # Show splash screen for a few seconds, then launch the main app
        self.splash.after(3000, self.navigation_manager.show_login())  # Show splash for 3 seconds

    def launch_main_app(self):
        """Close splash screen and launch the main application."""
        self.splash.destroy() 
        self.main_app()

    def main_app(self):
        """Setup and launch the main application window."""
        main_window = tk.Tk()
        main_window.title("Main App")
        main_window.geometry("600x400")
        tk.Label(
            main_window, 
            text="Welcome to the Main Application!", 
            font=("Arial", 18)
        ).pack(pady=50)
        main_window.mainloop()

    def run(self):
        """Run the splash screen."""
        self.splash.mainloop()


# # Run the application
# if __name__ == "__main__":
#     app = SplashApp()
#     app.run()
