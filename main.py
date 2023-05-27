import os
import platform
import glob
from tkinter import Button
import ui.pop_up_menu as pm

from app import App
root = App("FileHive")


# variable to store nav history, index of current path & path of right-clicked button
history = []
current_index = -1
clikd_btn = None

from subprocess import call as file_call
import ui.images as img


def draw_files(dir_name=None, update_history=True):
    """ Retrieves files/folders from given directory on a GUI (scrollable frame). Represents files/folders using buttons
        Arranges these files/folders in grid format. Opens files with appropriate application according to OS.
        Tracks navigation history to allow navigation through folders """

    global history, current_index

    file_icons = {
        '.txt': img.txt,
        '.py': img.code,
        '.java': img.code,
        '.cpp': img.code,
        '.jpg': img.pic,
        '.png': img.pic,
        '.pdf': img.pdf,
        '.mp4': img.vid,
        '.rar': img.archive,
        '.zip': img.archive,
        '.mp3': img.mp3,
        '.mkv': img.vid,
        '.3gp': img.vid,
        '.jpeg': img.pic,
    }

    # Clear previously drawn widgets
    for widget in scrollable_frame.scrollable_frame.winfo_children():
        widget.destroy()

    # set default filepath as home dir
    if dir_name is None or dir_name == 'Home':
        filepath = os.path.expanduser('~')
    else:
        # Construct filepath using provided dir name
        filepath = os.path.join(os.path.expanduser('~'), dir_name)

        # if filepath exist get a list of items in the filepath and sort alphabetically
    if os.path.exists(filepath):
        items = [os.path.basename(item) for item in glob.glob(os.path.join(filepath, '*'))]

        # Create buttons for files and folders
        # corresponding image for filetype or folder
        #
        row = 0
        col = 0
        for item in items:
            item_path = os.path.join(filepath, item)
            is_directory = os.path.isdir(item_path)
            item_name = os.path.basename(item_path)
            _name = item_name if len(item_name) <= 14 or is_directory else \
                item_name[:14 // 2 - 2] + "..." + item_name[-12 // 2 + 1:]

            # file extension
            file_ext = os.path.splitext(item_name)[1]

            if is_directory:
                image_path = img.folder
            else:
                image_path = file_icons.get(file_ext, img.unknown)

            btn_img = image_path
            button = Button(scrollable_frame.scrollable_frame, text=_name, image=btn_img, compound='top',
                            fg='white', bg='#1e1e1e', borderwidth=0, highlightthickness=0,
                            width=55, height=55, wraplength=100, activebackground='#404040',
                            activeforeground='white')

            button.grid(row=row, column=col, padx=30, pady=4, sticky='nsew')

            button.bind("<Button-3>", lambda event, clicked_btn=item_path,
                                             file_ext=file_ext: on_right_click(event, clicked_btn, file_ext))

            # button click event to button_clicked method from Sidebar class
            button.config(command=lambda btn=button: sidebar.button_clicked(btn))

            # open files with appropriate application
            if not is_directory:
                if platform.system() == 'Windows':
                    button.config(command=lambda fp=item_path: os.startfile(fp))
                else:
                    button.config(command=lambda fp=item_path: file_call(('xdg-open', fp)))
            else:
                # Recursively display contents of subdirectories
                button.config(command=lambda dir_name=item_path: draw_files(dir_name))

            # Increment the column counter
            col += 1

            # Move to the next row if the current row is full
            if col == 5:
                col = 0
                row += 1

        # Configure the grid to be responsive
        scrollable_frame.scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.scrollable_frame.grid_columnconfigure(1, weight=1)
        scrollable_frame.scrollable_frame.grid_columnconfigure(2, weight=1)
        for i in range(row + 1):
            scrollable_frame.scrollable_frame.grid_rowconfigure(i, weight=1)

        # Update the scrollable frame's scroll region & visibility
        scrollable_frame.canvas.configure(scrollregion=scrollable_frame.canvas.bbox("all"))
        scrollable_frame.scrollbar_visibility()

        # Update nav history & current_index
        if update_history:
            current_index += 1
            # Remove any forward history
            history = history[:current_index]
            history.append(filepath)

    else:
        print(f"Directory {filepath} does not exist.")

    return filepath


def on_right_click(event, clicked_btn, file_ext=None):
    """
    Handle the right-click event on a button
    """
    global clikd_btn
    clikd_btn = clicked_btn

    menu = pm.ContextMenu(root, tearoff=0, file_ext=file_ext, clikd_btn=clicked_btn, draw_files=draw_files)
    menu.post(event.x_root, event.y_root)

    # Bind a left-click event to hide the right-click menu
    root.bind("<Button-1>", lambda event: menu.unpost())


def _back():
    """
    Go back to the previous directory in the browsing history.
    Updates current dir based on browsing history & re-draws files in prev directory.
    Note: The browsing history must have at least one previous directory for this function to work.
    """
    global history, current_index

    if current_index > 0:
        current_index -= 1
        prev_dir = history[current_index]
        draw_files(prev_dir, update_history=False)


def _forward():
    """
    Go forward to the next dir in browsing history.
    Updates current directory based on browsing history & re-draws files in next dir.
    Note: The browsing history must have at least one next directory for this function to work.
    """
    global history, current_index

    if current_index < len(history) - 1:
        current_index += 1
        next_dir = history[current_index]
        draw_files(next_dir, update_history=False)


from tkinter import simpledialog, messagebox


def new_folder():
    """
    Create a new folder in the current directory.
    Function uses global variable 'history' to determine current directory.
    Prompts user to enter new folder name & creates folder in current dir.
    If the folder name is valid & folder creation is successful, file browser is updated to display new folder.
    """

    current_dir = history[-1]

    while True:
        folder_name = simpledialog.askstring("New Folder", "Enter New Folder Name")
        if folder_name is None:
            return

        # Remove leading/trailing spaces
        folder_name = folder_name.strip()

        if folder_name:
            new_folder_path = os.path.join(current_dir, folder_name)

            try:
                os.mkdir(new_folder_path)
                draw_files(current_dir)
                break
            except OSError:
                messagebox.showerror("Error", f"Folder Name '{folder_name}' Already exists. Try Again!",
                                     parent=root, icon='error')
        else:
            messagebox.showwarning("Warning", "Please Enter A Folder Name", parent=root,
                                   icon='warning', default='ok')


def newdoc():
    """
    Create a new document in the current directory.
    Prompts user to enter a document name & creates a new document with specified name & extension.
    If the document name is valid & creation is successful, the file browser is updated to display new document.
    Function uses global variable 'history' to determine current directory.
    Note: If no extension is provided, the function uses '.txt' as the default extension for the new document.
    """

    current_dir = history[-1]

    while True:
        doc_info = simpledialog.askstring("New Document", "Enter Document Name")
        if doc_info is None:
            return

        # Remove leading/trailing spaces
        doc_info = doc_info.strip()

        if doc_info:
            # Split the document name and extension
            doc_name, ext = os.path.splitext(doc_info)

            # if extension is not provided; use default extension '.txt'
            if ext == "":
                ext = ".txt"

            doc_filename = doc_name + ext
            # Create the full path for the new document
            new_doc_path = os.path.join(current_dir, doc_filename)

            if os.path.exists(new_doc_path):
                messagebox.showerror("Error", f"A filename '{doc_filename}' already exists. Choose a different name.",
                                     parent=root, icon='error')
                continue

            try:
                open(new_doc_path, 'w').close()
                draw_files(current_dir)  # Re-draw files in current directory to display new doc
                break

            except OSError:
                messagebox.showerror("Error", f"Error occurred while creating the document '{doc_filename}'",
                                     parent=root, icon='error')
        else:
            messagebox.showwarning("Warning", "Please Enter A Document Name", parent=root,
                                   icon='warning', default='ok')


#  --------------- toolbar  ---------------
from toolbar import Toolbar

# Create, configure and bind functions to toolbar
toolbar = Toolbar(root, clikd_btn=clikd_btn, draw_files=draw_files)
toolbar.back.config(command=_back)
toolbar.frwd.config(command=_forward)
toolbar.new_folder.config(command=new_folder)
toolbar.new_doc.config(command=newdoc)
toolbar.pack(side='top', fill='x')

# --------------- sidebar ---------------
from sidebar import Sidebar

# Create and configure the sidebar
sidebar = Sidebar(root, '#242424', '#404040', draw_files)
sidebar.pack(side='left', fill='y')

# --------------- scrollable frame ---------------
from ui.scrollable_frame import ScrollableFrame

# Create & configure scrollable frame
scrollable_frame = ScrollableFrame(root, bg='#1e1e1e')
scrollable_frame.pack(side='left', fill='both', expand=True)


if __name__ == "__main__":
    draw_files()
    root.mainloop()
