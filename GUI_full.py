import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import time

ser = None
current_thread = None
stop_event = threading.Event()

# Customizable defaults
step1_spin_duration = 180
step1_led_duration = 300
step2_total_duration = 180
motor_speed = 1200

completion_color = "#28a745"  # Green for complete

def auto_connect_serial():
    global ser
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "wchusb" in port.description.lower():
            try:
                ser = serial.Serial(port.device, 9600, timeout=1)
                time.sleep(2)
                return
            except:
                continue
    ser = None

def send_command(command):
    if ser and ser.is_open:
        ser.write((command + '\n').encode('utf-8'))
        print(f"Sent: {command}")
    else:
        update_status("Serial connection not available.", "red")

def update_status(message, color="blue"):
    status_var.set(f"Status: {message}")
    status_label.config(fg=color)

def update_timer(label, seconds):
    def countdown():
        for remaining in range(seconds, 0, -1):
            if stop_event.is_set():
                label.config(text="")
                return
            mins, secs = divmod(remaining, 60)
            label.config(text=f"Time Left: {mins:02}:{secs:02}")
            time.sleep(1)
        label.config(text="")
    threading.Thread(target=countdown, daemon=True).start()

def step1_sequence():
    def run():
        stop_event.clear()
        update_status("Spinning (Step 1 - Part 1)", "orange")
        send_command(f"LED OFF MOTOR {motor_speed}")
        update_timer(timer_label, step1_spin_duration)
        for _ in range(step1_spin_duration):
            if stop_event.is_set():
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped", "red")
                return
            time.sleep(1)

        update_status("Spinning + LED (Step 1 - Part 2)", "orange")
        send_command(f"LED ON MOTOR {motor_speed}")
        update_timer(timer_label, step1_led_duration)
        for _ in range(step1_led_duration):
            if stop_event.is_set():
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped", "red")
                return
            time.sleep(1)

        send_command("LED OFF MOTOR 1000")
        update_status("Step 1 Complete", completion_color)
    global current_thread
    current_thread = threading.Thread(target=run, daemon=True)
    current_thread.start()

def step2_sequence():
    def run():
        stop_event.clear()
        update_status("Spinning + LED (Step 2)", "orange")
        send_command(f"LED ON MOTOR {motor_speed}")
        update_timer(timer_label, step2_total_duration)
        for _ in range(step2_total_duration):
            if stop_event.is_set():
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped", "red")
                return
            time.sleep(1)
        send_command("LED OFF MOTOR 1000")
        update_status("Step 2 Complete", completion_color)
    global current_thread
    current_thread = threading.Thread(target=run, daemon=True)
    current_thread.start()

def stop_sequence():
    stop_event.set()
    send_command("LED OFF MOTOR 1000")
    update_status("Stopped", "red")

def send_custom():
    command = entry_custom.get().strip()
    if command:
        send_command(command)
        update_status(f"Sent custom command", "blue")

def apply_custom_values():
    global step1_spin_duration, step1_led_duration, step2_total_duration, motor_speed
    step1_spin_duration = int(spin1_var.get())
    step1_led_duration = int(led1_var.get())
    step2_total_duration = int(step2_var.get())
    motor_speed = int(speed_var.get())
    update_status("Custom values applied", "blue")

# GUI setup
root = tk.Tk()
root.title("Spinning Desicurer Control")
root.geometry(f"{root.winfo_screenwidth()//2}x{root.winfo_screenheight()}+0+0")
root.configure(bg="#ffffff")
root.resizable(True, True)

style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#ccc")

# Header
header = tk.Label(root, text="Spinning Desicurer Controller", font=("Helvetica", 20, "bold"), bg="#ffffff")
header.pack(pady=20)

btn1 = tk.Button(root, text="Step 1 (Spin → Spin+LED)", command=step1_sequence, width=40, height=2, bg="#007acc", fg="white", font=("Helvetica", 14))
btn1.pack(pady=8)
btn2 = tk.Button(root, text="Step 2 (Spin+LED)", command=step2_sequence, width=40, height=2, bg="#007acc", fg="white", font=("Helvetica", 14))
btn2.pack(pady=8)
btn_stop = tk.Button(root, text="STOP", command=stop_sequence, bg="red", fg="white", width=20, height=2, font=("Helvetica", 14, "bold"))
btn_stop.pack(pady=12)

# Timer label
timer_label = tk.Label(root, text="", font=("Helvetica", 16), bg="#ffffff")
timer_label.pack(pady=10)

# Custom settings
tk.Label(root, text="Customize Step Durations (seconds)", font=("Helvetica", 14, "bold"), bg="#ffffff").pack(pady=5)
frame_custom = tk.Frame(root, bg="#ffffff")
frame_custom.pack(pady=10)

spin1_var = tk.StringVar(value=str(step1_spin_duration))
led1_var = tk.StringVar(value=str(step1_led_duration))
step2_var = tk.StringVar(value=str(step2_total_duration))
speed_var = tk.StringVar(value=str(motor_speed))

fields = [
    ("Step 1 - Spin:", spin1_var),
    ("Step 1 - LED:", led1_var),
    ("Step 2 Total:", step2_var),
    ("Motor Speed:", speed_var)
]

for i, (label_text, var) in enumerate(fields):
    tk.Label(frame_custom, text=label_text, bg="#ffffff", font=("Helvetica", 12)).grid(row=i//2, column=(i%2)*2, padx=5, pady=6, sticky="e")
    tk.Entry(frame_custom, textvariable=var, width=8, font=("Helvetica", 12)).grid(row=i//2, column=(i%2)*2+1, padx=5, pady=6)

btn_apply = tk.Button(root, text="Apply Custom Values", command=apply_custom_values, bg="#444", fg="white", width=30, font=("Helvetica", 12))
btn_apply.pack(pady=10)

# Custom command
tk.Label(root, text="Send Custom Command (e.g., LED ON MOTOR 1200):", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
entry_custom = tk.Entry(root, width=45, font=("Helvetica", 12))
entry_custom.pack(pady=3)
btn_custom = tk.Button(root, text="Send", command=send_custom, bg="#444", fg="white", width=20, font=("Helvetica", 12))
btn_custom.pack(pady=5)

# Status
status_var = tk.StringVar()
status_var.set("Status: Ready")
status_label = tk.Label(root, textvariable=status_var, fg="blue", font=("Helvetica", 14, "bold"), bg="#ffffff")
status_label.pack(pady=10)

auto_connect_serial()
root.mainloop()
