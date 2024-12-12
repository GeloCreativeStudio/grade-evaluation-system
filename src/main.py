"""
Main application for EECP GESYS.
"""

import tkinter as tk
from tkinter import ttk
from .ui.auth_screens import LoginScreen, RegistrarSignupScreen, StudentSignupScreen
from .ui.dashboard_screens import StudentDashboard, RegistrarDashboardNew
from .ui.ui_components import setup_styles, COLORS

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EECP GESYS")
        
        # Set window size and center it
        window_width = 1200
        window_height = 800
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Configure the root window
        self.root.configure(bg=COLORS['background'])
        
        # Setup custom styles
        setup_styles()
        
        # Create the container for all frames
        self.container = ttk.Frame(self.root, style='App.TFrame')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.current_user = None
        self.user_type = None
        
        # Initialize authentication frames
        for F in (LoginScreen, StudentSignupScreen, RegistrarSignupScreen):
            frame = F(self.container, self.show_frame, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show login screen initially
        self.show_frame("LoginScreen")
    
    def create_dashboard(self, user_type, user_id):
        """Create and show the appropriate dashboard."""
        if user_type == "student":
            frame = StudentDashboard(self.container, self.show_frame, self, user_id)
            self.frames["StudentDashboard"] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame("StudentDashboard")
        else:
            frame = RegistrarDashboardNew(self.container, self.show_frame, self)
            self.frames["RegistrarDashboard"] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame("RegistrarDashboard")
    
    def logout(self):
        """Handle user logout."""
        # Clear user data
        self.current_user = None
        self.user_type = None
        
        # Remove dashboard frames
        if "StudentDashboard" in self.frames:
            self.frames["StudentDashboard"].grid_forget()
            del self.frames["StudentDashboard"]
        if "RegistrarDashboard" in self.frames:
            self.frames["RegistrarDashboard"].grid_forget()
            del self.frames["RegistrarDashboard"]
        
        # Show login screen
        self.show_frame("LoginScreen")
    
    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()
    
    def run(self):
        """Start the application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
