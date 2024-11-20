import tkinter as tk
from tkinter import messagebox
from ftplib import FTP
import os
import threading
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FTPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customizable FTP GUI")

        # FTP Client Frame
        client_frame = tk.Frame(self.root, padx=10, pady=10)
        client_frame.pack(fill="both", expand=True)

        tk.Label(client_frame, text="FTP Client").grid(row=0, columnspan=2, pady=10)
        tk.Label(client_frame, text="Server:").grid(row=1, column=0, sticky="w")
        tk.Label(client_frame, text="Port:").grid(row=2, column=0, sticky="w")
        tk.Label(client_frame, text="Username:").grid(row=3, column=0, sticky="w")
        tk.Label(client_frame, text="Password:").grid(row=4, column=0, sticky="w")

        self.server_entry = tk.Entry(client_frame)
        self.port_entry = tk.Entry(client_frame)
        self.username_entry = tk.Entry(client_frame)
        self.password_entry = tk.Entry(client_frame, show="*")

        self.server_entry.grid(row=1, column=1, pady=2)
        self.port_entry.grid(row=2, column=1, pady=2)
        self.username_entry.grid(row=3, column=1, pady=2)
        self.password_entry.grid(row=4, column=1, pady=2)

        connect_button = tk.Button(client_frame, text="Connect", command=self.connect_to_server)
        connect_button.grid(row=5, columnspan=2, pady=10)

        # FTP Server Frame
        server_frame = tk.Frame(self.root, padx=10, pady=10)
        server_frame.pack(fill="both", expand=True)

        tk.Label(server_frame, text="FTP Server").grid(row=0, columnspan=2, pady=10)
        tk.Label(server_frame, text="Server IP:").grid(row=1, column=0, sticky="w")
        tk.Label(server_frame, text="Port:").grid(row=2, column=0, sticky="w")
        tk.Label(server_frame, text="Username:").grid(row=3, column=0, sticky="w")
        tk.Label(server_frame, text="Password:").grid(row=4, column=0, sticky="w")

        self.server_ip_entry = tk.Entry(server_frame)
        self.server_port_entry = tk.Entry(server_frame)
        self.server_user_entry = tk.Entry(server_frame)
        self.server_pass_entry = tk.Entry(server_frame, show="*")

        self.server_ip_entry.grid(row=1, column=1, pady=2)
        self.server_port_entry.grid(row=2, column=1, pady=2)
        self.server_user_entry.grid(row=3, column=1, pady=2)
        self.server_pass_entry.grid(row=4, column=1, pady=2)

        start_server_button = tk.Button(server_frame, text="Start Server", command=self.start_server)
        start_server_button.grid(row=5, columnspan=2, pady=10)

    def connect_to_server(self):
        server = self.server_entry.get()
        port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            ftp = FTP()
            ftp.connect(server, int(port))
            ftp.login(username, password)
            messagebox.showinfo("Connection Successful", f"Connected to {server}")
            ftp.quit()
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def start_server(self):
        server_ip = self.server_ip_entry.get()
        server_port = self.server_port_entry.get()
        server_user = self.server_user_entry.get()
        server_pass = self.server_pass_entry.get()

        if not server_ip or not server_port or not server_user or not server_pass:
            messagebox.showwarning("Input Error", "Please fill all server details.")
            return

        try:
            server_thread = threading.Thread(
                target=self.run_server, args=(server_ip, int(server_port), server_user, server_pass)
            )
            server_thread.daemon = True
            server_thread.start()
            messagebox.showinfo("Server Started", f"FTP server is running on {server_ip}:{server_port}")
        except Exception as e:
            messagebox.showerror("Server Error", str(e))

    def run_server(self, server_ip, server_port, username, password):
        authorizer = DummyAuthorizer()
        authorizer.add_user(username, password, os.getcwd(), perm="elradfmw")
        handler = FTPHandler
        handler.authorizer = authorizer
        server = FTPServer((server_ip, server_port), handler)
        server.serve_forever()


if __name__ == "__main__":
    root = tk.Tk()
    app = FTPApp(root)
    root.mainloop()
