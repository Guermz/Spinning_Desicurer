import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import time

ser = None
current_thread = None
stop_event = threading.Event()

def auto_connect_serial():
    global ser
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "wchusb" in port.description.lower():  # Some clones
            try:
                ser = serial.Serial(port.device, 9600, timeout=1)
                time.sleep(2)  # Allow Arduino to initialize
                return
            except:
                continue
    ser = None

def send_command(command):
    if ser and ser.is_open:
        ser.write((command + '\n').encode('utf-8'))
        print(f"Sent: {command}")
    else:
        update_status("Serial connection not available.")

def update_status(message):
    status_var.set(f"Status: {message}")

def step1_sequence():
    def run():
        stop_event.clear()
        update_status("Spinning (Step 1 - Part 1)")
        send_command("LED OFF MOTOR 1200")
        for _ in range(180):
            if stop_event.is_set():
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped")
                return
            time.sleep(1)

        update_status("Spinning + LED (Step 1 - Part 2)")
        send_command("LED ON MOTOR 1200")
        for _ in range(300):
            if stop_event.is_set():
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped")
                return
            time.sleep(1)

        send_command("LED OFF MOTOR 1000")
        update_status("Step 1 Complete")
    global current_thread
    current_thread = threading.Thread(target=run, daemon=True)
    current_thread.start()

def step2_sequence():
    def run():
        stop_event.clear()
        update_status("Spinning + LED (Step 2)")
        send_command("LED ON MOTOR 1200")
        for _ in range(180):
            if stop_event.is_set():
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped")
                return
            time.sleep(1)
        send_command("LED OFF MOTOR 1000")
        update_status("Step 2 Complete")
    global current_thread
    current_thread = threading.Thread(target=run, daemon=True)
    current_thread.start()

def stop_sequence():
    stop_event.set()
    send_command("LED OFF MOTOR 1000")
    update_status("Stopped")

def send_custom():
    command = entry_custom.get().strip()
    if command:
        send_command(command)
        update_status(f"Sent custom command")

# GUI setup
root = tk.Tk()
root.title("Spinning Desicurer Control")
root.geometry("450x400")

tk.Label(root, text="Spinning Desicurer Controller", font=("Helvetica", 16)).pack(pady=10)

btn1 = tk.Button(root, text="Step 1 (Spin 3min → Spin+LED 5min)", command=step1_sequence, width=40)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Step 2 (Spin+LED 3min)", command=step2_sequence, width=40)
btn2.pack(pady=10)

btn_stop = tk.Button(root, text="STOP", command=stop_sequence, bg="red", fg="white", width=20)
btn_stop.pack(pady=10)

tk.Label(root, text="Send Custom Command (e.g., LED ON MOTOR 1200):").pack(pady=5)
entry_custom = tk.Entry(root, width=40)
entry_custom.pack()
btn_custom = tk.Button(root, text="Send", command=send_custom)
btn_custom.pack(pady=10)

# Status label
status_var = tk.StringVar()
status_var.set("Status: Ready")
status_label = tk.Label(root, textvariable=status_var, fg="blue")
status_label.pack(pady=10)

# Auto-connect on start
auto_connect_serial()

root.mainloop()
