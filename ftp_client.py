import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ftplib import FTP
import os

class FTPClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FTP Client")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        self.ftp = None

        # UI Elements
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
        self.tree.column("Name", anchor="w", width=200)
        self.tree.column("Size", anchor="e", width=100)
        self.tree.column("Type", anchor="center", width=100)
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
        for item in self.tree.get_children():
            self.tree.delete(item)


if __name__ == "__main__":
    root = tk.Tk()
    app = FTPClientApp(root)
    root.mainloop()
