from tkinter import Frame, Canvas
from tkinter.ttk import Scrollbar, Style


class ScrollableFrame(Frame):
    """
    A custom Tkinter frame with a scrollable canvas.
    Args: container: The parent widget or container where the ScrollableFrame will be placed.
          **kwargs: Additional keyword arguments to be passed to Frame constructor.

    Attributes:
        canvas (Canvas): The canvas widget used for scrolling.
        scrollbar (Scrollbar): The vertical scrollbar widget.
        scrollable_frame (Frame): The frame inside the canvas that holds the scrollable content.

    Methods:
        bind_scroll_events(), on_mousewheel(event), update_scrollbar_visibility()
    """
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        # Configure frame & create canvas
        self.configure(bg='#1e1e1e', highlightthickness=0)
        self.canvas = Canvas(self, bg='#1e1e1e', highlightthickness=0)

        # scrollbar style
        style = Style()
        style.configure("Custom.Vertical.TScrollbar",
                        background='#343434',
                        troughcolor='#343434',
                        bordercolor='#343434',
                        arrowsize=13,
                        gripcount=0,
                        relief='flat')

        style.map("Custom.Vertical.TScrollbar",
                  background=[('!active', '#5b5b5b'), ('active', '#a9a9a9')],
                  sliderrelief=[('pressed', 'flat')],
                  sliderborderwidth=[('pressed', 0)])

        # Create vertical scrollbar
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview,
                                   style="Custom.Vertical.TScrollbar")

        # Create the scrollable frame
        self.scrollable_frame = Frame(self.canvas, bg='#1e1e1e')

        # canvas window
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack & bind
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_events()

    def scroll_events(self):
        """Binds scroll events and updates the scrollbar visibility"""
        self.canvas.bind("<MouseWheel>", self.mousewheel)
        self.scrollbar_visibility()

    def mousewheel(self, event):
        """Scrolls the canvas in response to the mouse wheel event"""
        self.canvas.yview_scroll(-int(event.delta / 120), "units")

    def scrollbar_visibility(self):
        """Updates the visibility of the scrollbar based on content and canvas height"""
        self.update_idletasks()
        content_height = self.scrollable_frame.winfo_reqheight()
        canvas_height = self.canvas.winfo_height()

        if content_height > canvas_height:
            # Show the scrollbar if the content height is greater than the canvas height
            self.scrollbar.pack(side="right", fill="y")
        else:
            # Hide the scrollbar if the content height is smaller than or equal to the canvas height
            self.scrollbar.pack_forget()
