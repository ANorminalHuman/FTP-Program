import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import FTPServer
import threading
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FTPClientApp:
    """Graphical Interface for FTP Client and Secure FTP Server"""
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced FTP Client")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        self.ftp = None
        self.ftp_server = None
        self.server_thread = None
        self.setup_ui()

    def setup_ui(self):
        # Connection Frame for FTP Client
        connection_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        connection_frame.pack(fill=tk.X)

        # Server connection
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

        # FTP Server Frame
        server_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        server_frame.pack(fill=tk.X)
        tk.Label(server_frame, text="Server IP:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.server_ip_entry = tk.Entry(server_frame, width=20)
        self.server_ip_entry.grid(row=0, column=1, padx=5)
        self.server_ip_entry.insert(0, "127.0.0.1")
        self.start_server_button = tk.Button(server_frame, text="Start Server", bg="#4caf50", fg="white", command=self.start_ftp_server)
        self.start_server_button.grid(row=0, column=2, padx=10)
        self.stop_server_button = tk.Button(server_frame, text="Stop Server", bg="#f44336", fg="white", command=self.stop_ftp_server)
        self.stop_server_button.grid(row=0, column=3, padx=10)
        self.stop_server_button.config(state=tk.DISABLED)

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
            logging.error(f"Failed to connect: {e}")
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def list_files(self):
        # more comprehensive error handling added
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
            logging.error(f"Failed to list files: {e}")
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
            logging.error(f"Failed to upload file: {e}")
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
            logging.error(f"Failed to download file: {e}")
            messagebox.showerror("Error", f"Failed to download file: {e}")

    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            self.ftp = None
        messagebox.showinfo("Disconnect", "Disconnected from FTP server.")

    def start_ftp_server(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user("user", "12345", os.getcwd(), perm="elradfmw")
        
        handler = TLS_FTPHandler
        handler.authorizer = authorizer
        handler.certfile = "path/to/your/certificate.pem"

        server_address = (self.server_ip_entry.get(), 21)
        self.ftp_server = FTPServer(server_address, handler)

        self.server_thread = threading.Thread(target=self.ftp_server.serve_forever)
        self.server_thread.start()
        self.start_server_button.config(state=tk.DISABLED)
        self.stop_server_button.config(state=tk.NORMAL)
        messagebox.showinfo("Server", "FTP Server started successfully.")

    def stop_ftp_server(self):
        if self.ftp_server:
            self.ftp_server.close_all()
            self.server_thread.join()
            self.ftp_server = None
            self.server_thread = None
            self.start_server_button.config(state=tk.NORMAL)
            self.stop_server_button.config(state=tk.DISABLED)
            messagebox.showinfo("Server", "FTP Server stopped successfully.")

def main():
    root = tk.Tk()
    app = FTPClientApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
