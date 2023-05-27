from tkinter import Button, Entry, Frame, Menu, Toplevel, Label
import tkinter.messagebox as messagebox
import webbrowser
import ui.images as img
import os


class Toolbar(Frame):
    def __init__(self, parent, clikd_btn=None, draw_files=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(bg='#303030', height=35)

        self.parent = parent
        self.clikd_btn = clikd_btn
        self.draw_files = draw_files

        # Defining common button style properties
        button_style = {
            'bg': '#303030',
            'bd': 0,
            'relief': 'sunken',
            'highlightthickness': 0,
            'cursor': 'hand2',
            'activebackground': '#3a3a3a',
        }

        # Back button
        self.back = Button(self, image=img.back, **button_style)
        self.back.pack(side='left')

        # Forward button
        self.frwd = Button(self, image=img.frwd, **button_style)
        self.frwd.pack(side='left')

        # New folder button
        self.new_folder = Button(self, image=img.new_fold, **button_style)
        self.new_folder.pack(side='left', padx=13)

        # New document button
        self.new_doc = Button(self, image=img.new_doc, **button_style)
        self.new_doc.pack(side='left')

        # Search bar
        self.search_bar = Entry(self, bg='#242424', relief='flat', highlightthickness=0, fg='white',
                                font=('Georgia', 13), width=32)
        self.search_bar.pack(side='left', padx=(110, 10), pady=5, ipady=2, fill='x')

        # Search button
        self.search = Button(self, image=img.search, **button_style)
        self.search.pack(side='left')

        # about menu
        self.about_menu = Menu(self, tearoff=0)
        self.about_menu.configure(bg='#404040', fg='white', activebackground='#303030',
                                  activeforeground='white', bd=0, relief='sunken', activeborderwidth=0)
        self.about_menu.add_command(label='About App', command=self.about_app)
        self.about_menu.add_command(label='Developer', command=self.dev_info)

        # about button
        self.about = Button(self, image=img.about, **button_style)
        self.about.pack(side='right', padx=(12, 43))
        self.about.configure(command=self.show_menu)

        # bind mouse click event
        self.master.bind('<Button-1>', self.hide_menu)
        self.search.configure(command=self.perform_search)

    def show_menu(self):
        self.about_menu.post(self.about.winfo_rootx(), self.about.winfo_rooty() + self.about.winfo_height())

    def hide_menu(self, event):
        if self.about_menu.post:
            self.about_menu.unpost()
        self.master.bind("<Button-1>", self.about_menu.unpost())

    def perform_search(self):
        search_text = self.search_bar.get()
        if search_text:
            current_dir = self.draw_files(dir_name=self.clikd_btn, update_history=False)
            found_items = []
            for root, dirs, files in os.walk(current_dir):
                for item in dirs + files:
                    item_path = os.path.join(root, item)
                    if item.lower() == search_text.lower():
                        found_items.append(item_path)
            if found_items:
                if len(found_items) == 1:
                    item_path = found_items[0]
                    if os.path.isfile(item_path):
                        folder_path = os.path.dirname(item_path)
                        self.draw_files(dir_name=folder_path)  # Navigate to the folder containing the file
                    else:
                        self.draw_files(dir_name=item_path)  # Navigate to the specific directory/folder
                else:
                    messagebox.showinfo("Search Results", self.format(found_items))
            else:
                messagebox.showinfo("Search Results", "No matching items found.")
        else:
            messagebox.showwarning("Search", "Please enter search text.")

    def format(self, found_items):
        results = f"Found {len(found_items)} items:\n\n"
        for item in found_items:
            results += f"- {item}\n"
        return results

    def dev_info(self):
        dev_win = Toplevel(self)
        dev_win.title("Developer Profile")
        dev_win.resizable(False, False)

        # Developer image
        developer_image = Label(dev_win, image=img.me)
        developer_image.pack()

        # Developer name
        developer_name = Label(dev_win, text="Nihal Patel", font=('Helvetica', 16, 'bold'))
        developer_name.pack(pady=(10, 5))

        dev_title = Label(dev_win, text="Pythod Developer", font=('Helvetica', 14, 'italic'))
        dev_title.pack()

        # Developer social media handles
        social = Frame(dev_win)
        social.pack(pady=(0, 10))

        # LinkedIn handle
        linkdin = Label(social, image=img.linkdIn)
        linkdin.pack(side='left')
        linkdin.bind("<Button-1>", lambda e: webbrowser.open("https://www.linkedin.com/in/nihal-patel-a33b6520a/"))

        # Instagram handle
        insta = Label(social, image=img.ig)
        insta.pack(side='left', padx=5)
        insta.bind("<Button-1>", lambda e: webbrowser.open("https://www.instagram.com/_its.nihal/"))

        # GitHub handle
        github = Label(social, image=img.github)
        github.pack(side='left')
        github.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/its-nihal-patel"))

        # Thank you message
        msg = Label(dev_win, text="Thanks for using this application", font=('Helvetica', 12))
        msg.pack(pady=(12, 0))

        # Center the developer window on the screen
        dev_win.update_idletasks()
        screen_width = dev_win.winfo_screenwidth()
        screen_height = dev_win.winfo_screenheight()
        window_width = dev_win.winfo_width()
        window_height = dev_win.winfo_height()
        dev_win.geometry(f"+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}")

    def about_app(self):
        about_win = Toplevel(self)
        about_win.title("About App")
        about_win.resizable(False, False)

        # Heading
        heading_label = Label(about_win, text="About App", font=('Helvetica', 16, 'bold'))
        heading_label.pack(pady=(10, 0))

        # Paragraph 1
        txt = '''FileHive is file exploring application
        that allows users to navigate & manage
        files/folders. It's user-friendly graphical
        interface designed to simplify file
        management tasks.'''

        para1_label = Label(about_win, text=txt, font=('Helvetica', 11))
        para1_label.pack()

        # Paragraph 2
        txt2 = '''The UI is inspired from nautilus
        file manager dark mode theme.
        
        Developed By Nihal Patel'''
        para2_label = Label(about_win, text=txt2, font=('Helvetica', 11))
        para2_label.pack()

        # Center the window
        about_win.update_idletasks()
        screen_width = about_win.winfo_screenwidth()
        screen_height = about_win.winfo_screenheight()
        window_width = about_win.winfo_width()
        window_height = about_win.winfo_height()
        about_win.geometry(f"+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}")
