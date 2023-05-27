from tkinter import Frame, Button
from functools import partial
import ui.images as img


class Sidebar(Frame):
    """
    A custom Tkinter frame representing a sidebar with buttons.
    Args:
        master (Tk): The parent Tkinter window or frame.
        bg (str): The background color of the sidebar.
        activebg (str): The background color when a button is active.
        draw_files (callable): A function to handle drawing files based on the selected button.
    Attributes:
        buttons (dict): A dictionary to store the buttons.
    Methods:
        button_clicked(button): Handles the button click event.
    """
    def __init__(self, master, bg, activebg, draw_files, **kwargs):
        """
        Initializes the Sidebar.

        Args:
            master (Tk): The parent Tkinter window or frame.
            bg (str): The background color of the sidebar.
            activebg (str): The background color when a button is active.
            draw_files (callable): A function to handle drawing files based on the selected button.
            **kwargs: Additional keyword arguments to be passed to the Frame constructor.
        """
        kwargs['bg'] = bg
        super().__init__(master, **kwargs)

        self.draw_files = draw_files

        # dictionary to store buttons
        self.buttons = {}

        buttons = [
            ('Home', img.home),
            ('Desktop', img.desktop),
            ('Downloads', img.downloads),
            ('Documents', img.documents),
            ('Pictures', img.pictures),
            ('Music', img.music),
            ('Videos', img.videos),
        ]

        for button_text, button_image in buttons:
            button = Button(
                self,
                text=button_text,
                image=button_image,
                activeforeground='white',
                compound='left',
                bg=bg,
                fg='white',
                activebackground=activebg,
                relief='sunken',
                bd=0,
                highlightthickness=0,
                cursor='hand2',
                anchor='w',
                width=170,
            )
            button.pack(side='top', padx=0, pady=0, fill='x')
            button.selected = False
            button.config(command=partial(self.button_clicked, button))
            self.buttons[button_text] = button

    def button_clicked(self, button):
        """
        Handles the button click event.
        Args:
            button (Button): The button that was clicked.
        """
        for b in self.buttons.values():
            if b == button:
                b.config(bg='#404040')
                b.selected = True
            else:
                b.config(bg=self['bg'], activebackground='#3a3a3a')
                b.selected = False

        # Perform actions based on active button
        print(f"{button['text']} button clicked!")

        # Calling the draw_files function with button text
        self.draw_files(button['text'])
