import os.path
import platform
import subprocess
import shutil
from tkinter.simpledialog import askstring
from tkinter import Menu, messagebox
import datetime
import send2trash


class ContextMenu(Menu):
    """
    Custom right-click menu for file manager application.
    """

    def __init__(self, master, file_ext=None, clikd_btn=None, draw_files=None, **kwargs):
        """
        Initialize the RightClickMenu.

        Args:
            master (Tk): The Tkinter root or Toplevel window.
            file_ext (str): File extension of the clicked item.
            clikd_btn (str): Path of the clicked item.
            draw_files (function): Function to refresh the content after operations.
            **kwargs: Additional keyword arguments for Menu widget.
        """
        super().__init__(master, **kwargs)

        # Configure menu appearance
        self.configure(bg="#272727", activebackground="#4b4b4b", borderwidth=0,
                       relief='sunken', bd=0, activeborderwidth=0, activeforeground='white', fg='white')

        # menu options
        self.add_command(label="Open", command=self.openfile)
        self.add_command(label="Copy", command=lambda: self.copy(self.clikd_btn))
        self.add_command(label="Rename", command=self.rename)
        self.add_command(label="Delete", command=self.delete_item)

        # Add additional options for archive files
        if file_ext == ".rar" or file_ext == ".zip":
            self.add_command(label="Extract", command=self.extract)

        self.add_command(label="Properties", command=self.properties)

        # Bind events to the menu
        master.bind("<Button-1>", self.on_root_click)
        master.bind("<Button-3>", self.blank_area)

        # Store the necessary attributes
        self.master = master
        self.clikd_btn = clikd_btn
        self.draw_files = draw_files

    copied_item = None

    def copy(self, source):
        """
        Copy the selected item.
        Args: source (str): Path of the item to be copied.
        """
        self.copied_item = source

    def paste(self):
        """Paste the copied item to the current directory"""
        if self.copied_item is not None:
            dst = os.getcwd()
            try:
                if os.path.isdir(self.copied_item):
                    shutil.copytree(self.copied_item, os.path.join(dst, os.path.basename(self.copied_item)))
                else:
                    shutil.copy2(self.copied_item, dst)
                messagebox.showinfo("Success", f"{self.copied_item} Copied Successfully to {dst}")
            except Exception as e:
                messagebox.showerror("Error", f"Error while pasting item: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Copied item does not exist")

    def on_root_click(self, event):
        """Event handler for left-click outside the menu.
        Closes the menu if it is open"""
        if self.winfo_ismapped():
            self.unpost()
        self.master.bind("<Button-1>", self.unpost())

    def blank_area(self, event):
        """
        Displays the menu when a right-click occurs on blank area"""
        self.delete(0, 'end')
        self.add_command(label="Paste", command=lambda: self.paste())
        self.add_command(label="Properties")
        self.post(event.x_root, event.y_root)
        self.master.bind("<Button-1>", lambda event: self.unpost())

    def openfile(self):
        """ Open the selected file or navigate into selected directory"""
        is_dir = os.path.isdir(self.clikd_btn)

        if is_dir:
            self.draw_files(dir_name=self.clikd_btn)
        else:
            if platform.system() == 'Windows':
                os.startfile(self.clikd_btn)
            else:
                subprocess.call(['xdg-open', self.clikd_btn])

    def rename(self):
        """Rename the selected file or directory"""
        if self.clikd_btn is not None:
            initial_name = os.path.basename(self.clikd_btn)
            current_dir = os.path.dirname(self.clikd_btn)

            while True:
                new_name = askstring("Rename", "Enter a new name:", initialvalue=initial_name)

                if new_name is None:
                    return  # User canceled the renaming process

                new_name = new_name.strip()

                if new_name != initial_name:
                    new_path = os.path.join(current_dir, new_name)

                    if not os.path.exists(new_path):
                        try:
                            os.rename(self.clikd_btn, new_path)
                            messagebox.showinfo("Success", f"{self.clikd_btn} renamed successfully to {new_path}")

                            # Refresh content after renaming
                            if self.draw_files:
                                self.draw_files(current_dir)

                            break

                        except Exception as e:
                            messagebox.showerror("Error", f"Error while renaming item: {str(e)}")
                    else:
                        messagebox.showerror("Error", f"File/Folder '{new_name}' already exists.")
                else:
                    messagebox.showwarning("Warning", "Same name entered. No changes made.")

    def extract(self):
        """ Extract an archive file (e.g., .rar or .zip)"""
        file_ext = os.path.splitext(self.clikd_btn)[1]
        extract_dir = os.path.dirname(self.clikd_btn)

        if file_ext == ".rar":
            if platform.system() == 'Windows':
                extract_cmd = f'unrar x "{self.clikd_btn}" "{extract_dir}"'
            else:
                extract_cmd = f'unrar x "{self.clikd_btn}" "{extract_dir}"'
        elif file_ext == ".zip":
            extract_cmd = f'unzip -o "{self.clikd_btn}" -d "{extract_dir}"'
        else:
            messagebox.showwarning("Warning", "Extraction not supported for this file format.")
            return

        try:
            subprocess.run(extract_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            messagebox.showinfo("Success", f"{self.clikd_btn} extracted successfully to {extract_dir}")

            # Refresh the content after extraction
            if self.draw_files:
                self.draw_files(extract_dir)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", "Error while extracting.")
        except Exception as e:
            messagebox.showerror("Error", f"Error while extracting: {str(e)}")

    def properties(self):
        """Display properties of the selected file or directory"""
        if self.clikd_btn is not None:
            try:
                properties_str = ""

                # if the path exists
                if not os.path.exists(self.clikd_btn):
                    messagebox.showerror("Error", f"File/Folder '{self.clikd_btn}' does not exist.")
                    return

                # Get the properties
                properties_str += f"Path: {self.clikd_btn}\n"
                properties_str += f"Type: {'Folder' if os.path.isdir(self.clikd_btn) else 'File'}\n"

                size = os.path.getsize(self.clikd_btn)  # in bytes

                if size < 1024:
                    properties_str += f"Size: {size} bytes\n"
                elif size < 1024 * 1024:
                    properties_str += f"Size: {size / 1024:.2f} KB\n"
                else:
                    properties_str += f"Size: {size / (1024 * 1024):.2f} MB\n"

                # Last modified timestamp
                last_modified_timestamp = os.path.getmtime(self.clikd_btn)
                last_modified_datetime = datetime.datetime.fromtimestamp(last_modified_timestamp)
                last_modified_str = last_modified_datetime.strftime("%Y-%m-%d %H:%M:%S")
                properties_str += f"Last Modified: {last_modified_str}\n"

                properties_str += f"Permissions: {oct(os.stat(self.clikd_btn).st_mode)[-3:]}\n"

                # Additional information
                if not os.path.isdir(self.clikd_btn):
                    properties_str += f"Extension: {os.path.splitext(self.clikd_btn)[1][1:]}\n"

                messagebox.showinfo("Properties", properties_str)

            except Exception as e:
                messagebox.showerror("Error", f"Error while retrieving properties: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No file/folder selected.")

    def delete_item(self):
        """ Delete the selected file or directory"""

        if self.clikd_btn is not None:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this item?")
            if confirmation:
                try:
                    if os.path.isdir(self.clikd_btn):
                        send2trash.send2trash(self.clikd_btn)
                    else:
                        send2trash.send2trash(self.clikd_btn)

                    messagebox.showinfo("Success", "Item moved to the recycle bin.")

                    # Refresh the content after deletion
                    if self.draw_files:
                        self.draw_files(os.path.dirname(self.clikd_btn))

                except OSError:
                    os.remove(self.clikd_btn)
                    messagebox.showwarning("Warning", "This item will be permanently deleted and cannot be restored.")

                    # Refresh the content after deletion
                    if self.draw_files:
                        self.draw_files(os.path.dirname(self.clikd_btn))

                except Exception as e:
                    messagebox.showerror("Error", f"Error while deleting item: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No file/folder selected.")
