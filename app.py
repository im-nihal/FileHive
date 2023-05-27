from tkinter import PhotoImage, Tk


class App(Tk):
    """
    Tkinter application window.
    Args:
        title (str): The title of the application window.
    """

    def __init__(self, title):
        """
        Initializes application window.
        Args:
            title (str): The title of the application window.
        """
        super().__init__()

        self.title(title)
        self.config(bg="#1e1e1e")

        # first param is True for all TopLevels to have same icons
        self.iconphoto(True, PhotoImage(file="images/toplevel.png"))

        # width & height of computer screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate x and y coordinates to center the window
        x = (screen_width - 900) // 2
        y = (screen_height - 592) // 2

        # Set the position and size of the window
        self.geometry(f"900x592+{x}+{y}")
        self.resizable(False, False)
