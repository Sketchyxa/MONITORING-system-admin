import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
import platform
import subprocess

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def scan_ports(ip, start_port, end_port, timeout, output_area):
    output_area.delete("1.0", tk.END)
    open_ports = []

    output_area.insert(tk.END, f"Pinging {ip}...\n")

    if not ping_host(ip):
        output_area.insert(tk.END, f"❌ Host {ip} is unreachable.\n", "error")
        return
    else:
        output_area.insert(tk.END, f"✅ Host {ip} is reachable. Starting scan...\n")

    def scan_port(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                s.connect((ip, port))
                open_ports.append(port)
                output_area.insert(tk.END, f"[OPEN] Port {port}\n", "open")
            except:
                output_area.insert(tk.END, f"[CLOSED] Port {port}\n", "closed")

    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    output_area.insert(tk.END, "\nScan complete.\n")

def start_scan():
    ip = ip_entry.get()
    try:
        port_range = port_entry.get().split("-")
        start_port = int(port_range[0])
        end_port = int(port_range[1])
        timeout = float(timeout_entry.get())
    except:
        messagebox.showerror("Invalid Input", "Please enter valid IP, port range, and timeout.")
        return

    scan_thread = threading.Thread(
        target=scan_ports, args=(ip, start_port, end_port, timeout, result_area)
    )
    scan_thread.start()

# GUI setup
root = tk.Tk()
root.title("Advanced Port Scanner")
root.geometry("550x550")

tk.Label(root, text="Target IP:").pack()
ip_entry = tk.Entry(root)
ip_entry.pack()

tk.Label(root, text="Port range (e.g. 20-1024):").pack()
port_entry = tk.Entry(root)
port_entry.pack()

tk.Label(root, text="Timeout (seconds):").pack()
timeout_entry = tk.Entry(root)
timeout_entry.insert(0, "1")
timeout_entry.pack()

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.pack(pady=10)

result_area = scrolledtext.ScrolledText(root, height=25)
result_area.pack(fill=tk.BOTH, expand=True)

# Цвета
result_area.tag_config("open", foreground="green")
result_area.tag_config("closed", foreground="red")
result_area.tag_config("error", foreground="orange")

root.mainloop()
