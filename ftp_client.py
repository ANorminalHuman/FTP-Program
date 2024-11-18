from ftplib import FTP
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class FTPClientApp:
    """Graphical Interface for FTP Client"""
    def __init__(self, root):
        self.root = root
        self.root.title("FTP Client")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.ftp = None

        self.setup_ui()

    def setup_ui(self):
        # Connection Frame
        connection_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        connection_frame.pack(fill=tk.X)

        tk.Label(connection_frame, text="Server:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.server_entry = tk.Entry(connection_frame, width=20)
        self.server_entry.grid(row=0, column=1, padx=5)

        tk.Label(connection_frame, text="Username:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
        self.username_entry = tk.Entry(connection_frame, width=15)
        self.username_entry.grid(row=0, column=3, padx=5)

        tk.Label(connection_frame, text="Password:", bg="#f0f0f0").grid(row=0, column=4, padx=5)
        self.password_entry = tk.Entry(connection_frame, width=15, show="*")
        self.password_entry.grid(row=0, column=5, padx=5)

        self.connect_button = tk.Button(connection_frame, text="Connect", bg="#4caf50", fg="white", command=self.connect)
        self.connect_button.grid(row=0, column=6, padx=10)

        # Files Frame
        self.files_frame = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.files_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.files_frame, columns=("Name", "Size", "Type"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Type", text="Type")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(fill=tk.X)

        tk.Button(buttons_frame, text="Upload File", bg="#2196f3", fg="white", command=self.upload_file).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(buttons_frame, text="Download File", bg="#2196f3", fg="white", command=self.download_file).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(buttons_frame, text="Refresh", bg="#2196f3", fg="white", command=self.list_files).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(buttons_frame, text="Disconnect", bg="#f44336", fg="white", command=self.disconnect).pack(side=tk.RIGHT, padx=10, pady=10)

    def connect(self):
        server = self.server_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.ftp = FTP(server)
            self.ftp.login(user=username, passwd=password)
            messagebox.showinfo("Connection", "Connected to FTP server successfully.")
            self.list_files()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def list_files(self):
        if not self.ftp:
            messagebox.showerror("Error", "Not connected to any server.")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            files = self.ftp.nlst()
            for file in files:
                try:
                    size = self.ftp.size(file)
                    self.tree.insert("", tk.END, values=(file, f"{size} bytes", "File"))
                except:
                    self.tree.insert("", tk.END, values=(file, "-", "Directory"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list files: {e}")

    def upload_file(self):
        if not self.ftp:
            messagebox.showerror("Error", "Not connected to any server.")
            return

        filepath = filedialog.askopenfilename()
        if not filepath:
            return

        try:
            with open(filepath, "rb") as file:
                self.ftp.storbinary(f"STOR {os.path.basename(filepath)}", file)
                messagebox.showinfo("Upload", f"File '{os.path.basename(filepath)}' uploaded successfully.")
                self.list_files()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

    def download_file(self):
        if not self.ftp:
            messagebox.showerror("Error", "Not connected to any server.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No file selected.")
            return

        filename = self.tree.item(selected_item[0], "values")[0]
        save_path = filedialog.askdirectory()
        if not save_path:
            return

        try:
            with open(os.path.join(save_path, filename), "wb") as file:
                self.ftp.retrbinary(f"RETR {filename}", file.write)
                messagebox.showinfo("Download", f"File '{filename}' downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download file: {e}")

    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            self.ftp = None
        messagebox.showinfo("Disconnect", "Disconnected from FTP server.")


def cli_mode():
    """Command-Line Interface for FTP Client"""
    print("Welcome to FTP Client CLI!")
    server = input("Enter server address: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        ftp = FTP(server)
        ftp.login(user=username, passwd=password)
        print(f"Connected to FTP server: {server}")

        while True:
            print("\nCommands:")
            print("1. List Files")
            print("2. Upload File")
            print("3. Download File")
            print("4. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                files = ftp.nlst()
                print("\nFiles on Server:")
                for file in files:
                    print(file)

            elif choice == "2":
                filepath = input("Enter the full path of the file to upload: ")
                try:
                    with open(filepath, "rb") as file:
                        ftp.storbinary(f"STOR {os.path.basename(filepath)}", file)
                        print(f"Uploaded {os.path.basename(filepath)} successfully.")
                except FileNotFoundError:
                    print("File not found.")

            elif choice == "3":
                filename = input("Enter the filename to download: ")
                save_path = input("Enter the directory to save the file: ")
                try:
                    with open(os.path.join(save_path, filename), "wb") as file:
                        ftp.retrbinary(f"RETR {filename}", file.write)
                        print(f"Downloaded {filename} successfully.")
                except Exception as e:
                    print(f"Error: {e}")

            elif choice == "4":
                ftp.quit()
                print("Disconnected from FTP server.")
                break

            else:
                print("Invalid choice. Try again.")

    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to select CLI or GUI mode."""
    print("FTP Client")
    print("1. CLI Mode")
    print("2. GUI Mode")

    choice = input("Enter your choice (1/2): ")
    if choice == "1":
        cli_mode()
    elif choice == "2":
        root = tk.Tk()
        app = FTPClientApp(root)
        root.mainloop()
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()