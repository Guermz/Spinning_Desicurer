import tkinter as tk
from tkinter import ttk, scrolledtext
import serial
import serial.tools.list_ports
import threading
import time

ser = None
stop_event = threading.Event()
sequence_running = False
reader_thread_started = False
timer_job = None

# Defaults
step1_spin_duration = 180
step1_led_duration = 300
step2_total_duration = 180
motor_speed = 1200

# Advanced window refs
advanced_window = None
serial_log = None


# -----------------------------
# Thread-safe UI helpers
# -----------------------------
def gui_call(func, *args, **kwargs):
    root.after(0, lambda: func(*args, **kwargs))


def update_status(message, color="blue"):
    def _update():
        status_var.set(f"Status: {message}")
        status_label.config(fg=color)
    gui_call(_update)


def update_phase(message):
    gui_call(lambda: phase_var.set(f"Phase: {message}"))


def update_connection_label(text, color="black"):
    def _update():
        connection_var.set(text)
        connection_label.config(fg=color)
    gui_call(_update)


def set_last_command(cmd):
    gui_call(lambda: last_command_var.set(f"Last Command: {cmd}"))


def log_message(msg):
    print(msg)
    if serial_log is not None:
        def _update():
            try:
                serial_log.insert(tk.END, msg + "\n")
                serial_log.see(tk.END)
            except Exception:
                pass
        gui_call(_update)


def set_buttons_running(running):
    def _update():
        state_main = tk.DISABLED if running else tk.NORMAL
        btn_step1.config(state=state_main)
        btn_step2.config(state=state_main)
        btn_connect.config(state=state_main)
        btn_reconnect.config(state=state_main)
        btn_disconnect.config(state=state_main)
        btn_advanced.config(state=state_main)
        btn_stop.config(state=tk.NORMAL)
    gui_call(_update)


# -----------------------------
# Serial handling
# -----------------------------
def list_ports():
    return [p.device for p in serial.tools.list_ports.comports()]


def refresh_ports():
    ports = list_ports()
    port_combo["values"] = ports
    if ports and not port_var.get():
        port_var.set(ports[0])


def auto_select_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc = (port.description or "").lower()
        if "arduino" in desc or "wchusb" in desc or "usb serial" in desc:
            return port.device
    return ports[0].device if ports else ""


def connect_serial(port=None):
    global ser, reader_thread_started

    disconnect_serial(silent=True)

    if not port:
        port = auto_select_port()

    if not port:
        update_connection_label("Connection: No serial port found", "red")
        update_status("No serial port found.", "red")
        return

    try:
        ser = serial.Serial(port, 9600, timeout=0.2)
        time.sleep(2)  # allow Arduino reset
        update_connection_label(f"Connection: {port} (Connected)", "green")
        update_status(f"Connected to {port}", "green")
        log_message(f"[INFO] Connected to {port}")

        if not reader_thread_started:
            threading.Thread(target=serial_reader, daemon=True).start()
            reader_thread_started = True

    except Exception as e:
        ser = None
        update_connection_label("Connection: Failed", "red")
        update_status("Failed to connect.", "red")
        log_message(f"[ERROR] Could not connect: {e}")


def disconnect_serial(silent=False):
    global ser
    try:
        if ser and ser.is_open:
            port_name = ser.port
            ser.close()
            if not silent:
                update_connection_label("Connection: Disconnected", "red")
                update_status("Disconnected", "red")
                log_message(f"[INFO] Disconnected from {port_name}")
    except Exception as e:
        if not silent:
            log_message(f"[ERROR] Disconnect failed: {e}")
    finally:
        ser = None
        if not silent:
            update_connection_label("Connection: Disconnected", "red")


def reconnect_serial():
    connect_serial(port_var.get().strip())


def send_command(command):
    global ser
    if ser and ser.is_open:
        try:
            ser.write((command + '\n').encode('utf-8'))
            set_last_command(command)
            log_message(f">>> {command}")
        except Exception as e:
            update_status("Serial write failed.", "red")
            log_message(f"[ERROR] Serial write failed: {e}")
    else:
        update_status("Serial connection not available.", "red")
        log_message("[ERROR] Serial connection not available.")


def serial_reader():
    global ser
    while True:
        try:
            if ser and ser.is_open and ser.in_waiting:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    log_message(f"ARDUINO: {line}")
        except Exception:
            pass
        time.sleep(0.05)


# -----------------------------
# Timer
# -----------------------------
def clear_timer():
    global timer_job
    if timer_job is not None:
        try:
            root.after_cancel(timer_job)
        except Exception:
            pass
        timer_job = None
    timer_var.set("")


def start_countdown(seconds):
    global timer_job
    clear_timer()
    end_time = time.time() + seconds

    def tick():
        global timer_job

        if stop_event.is_set():
            timer_var.set("")
            timer_job = None
            return

        remaining = max(0, int(round(end_time - time.time())))
        mins, secs = divmod(remaining, 60)
        timer_var.set(f"Time Left: {mins:02}:{secs:02}")

        if remaining > 0:
            timer_job = root.after(250, tick)
        else:
            timer_var.set("")
            timer_job = None

    tick()


def wait_with_stop(seconds):
    end_time = time.time() + seconds
    while time.time() < end_time:
        if stop_event.is_set():
            return False
        time.sleep(0.1)
    return True


# -----------------------------
# Sequence control
# -----------------------------
def begin_sequence():
    global sequence_running
    if sequence_running:
        update_status("A sequence is already running.", "red")
        return False
    sequence_running = True
    stop_event.clear()
    set_buttons_running(True)
    return True


def end_sequence():
    global sequence_running
    sequence_running = False
    set_buttons_running(False)
    update_phase("Idle")
    clear_timer()


def step1_sequence():
    global motor_speed
    if not begin_sequence():
        return

    def run():
        try:
            update_phase("Step 1 - Spin")
            update_status("Spinning (Step 1 - Part 1)", "orange")
            send_command(f"LED OFF MOTOR {motor_speed}")
            gui_call(start_countdown, step1_spin_duration)

            if not wait_with_stop(step1_spin_duration):
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped", "red")
                return

            update_phase("Step 1 - Spin + LED")
            update_status("Spinning + LED (Step 1 - Part 2)", "orange")
            send_command(f"LED ON MOTOR {motor_speed}")
            gui_call(start_countdown, step1_led_duration)

            if not wait_with_stop(step1_led_duration):
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped", "red")
                return

            send_command("LED OFF MOTOR 1000")
            update_status("Step 1 Complete", "green")

        finally:
            end_sequence()

    threading.Thread(target=run, daemon=True).start()


def step2_sequence():
    global motor_speed
    if not begin_sequence():
        return

    def run():
        try:
            update_phase("Step 2 - Spin + LED")
            update_status("Spinning + LED (Step 2)", "orange")
            send_command(f"LED ON MOTOR {motor_speed}")
            gui_call(start_countdown, step2_total_duration)

            if not wait_with_stop(step2_total_duration):
                send_command("LED OFF MOTOR 1000")
                update_status("Stopped", "red")
                return

            send_command("LED OFF MOTOR 1000")
            update_status("Step 2 Complete", "green")

        finally:
            end_sequence()

    threading.Thread(target=run, daemon=True).start()


def stop_sequence():
    stop_event.set()
    send_command("LED OFF MOTOR 1000")
    update_status("Stopped", "red")
    update_phase("Stopped")
    clear_timer()


# -----------------------------
# Manual controls
# -----------------------------
def led_on():
    send_command(f"LED ON MOTOR {motor_speed}")
    update_status("LED ON command sent", "blue")


def led_off():
    send_command(f"LED OFF MOTOR {motor_speed}")
    update_status("LED OFF command sent", "blue")


def led_only_on():
    send_command("LED ON")
    update_status("LED-only ON command sent", "blue")


def led_only_off():
    send_command("LED OFF")
    update_status("LED-only OFF command sent", "blue")


def motor_stop():
    send_command("LED OFF MOTOR 1000")
    update_status("Motor STOP command sent", "blue")


def send_motor_speed():
    try:
        val = int(manual_speed_var.get())
        if not (1000 <= val <= 2000):
            update_status("Manual speed must be 1000-2000", "red")
            return
        send_command(f"LED OFF MOTOR {val}")
        update_status(f"Motor speed {val} sent", "blue")
    except ValueError:
        update_status("Invalid manual speed", "red")


# -----------------------------
# Settings
# -----------------------------
def apply_custom_values():
    global step1_spin_duration, step1_led_duration, step2_total_duration, motor_speed
    try:
        s1 = int(spin1_var.get())
        l1 = int(led1_var.get())
        s2 = int(step2_var.get())
        ms = int(speed_var.get())

        if s1 < 0 or l1 < 0 or s2 < 0:
            update_status("Durations must be non-negative.", "red")
            return

        if not (1000 <= ms <= 2000):
            update_status("Motor speed must be between 1000 and 2000.", "red")
            return

        step1_spin_duration = s1
        step1_led_duration = l1
        step2_total_duration = s2
        motor_speed = ms
        manual_speed_var.set(str(ms))

        update_status("Settings applied", "green")
        log_message("[INFO] Settings updated")

    except ValueError:
        update_status("Please enter valid integers only.", "red")


# -----------------------------
# Advanced window with tabs
# -----------------------------
def open_advanced_window():
    global advanced_window, serial_log

    if advanced_window is not None and advanced_window.winfo_exists():
        advanced_window.lift()
        advanced_window.focus_force()
        return

    advanced_window = tk.Toplevel(root)
    advanced_window.title("Advanced Controls")
    advanced_window.geometry("780x500")
    advanced_window.configure(bg="white")

    notebook = ttk.Notebook(advanced_window)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # SETTINGS TAB
    tab_settings = tk.Frame(notebook, bg="white")
    notebook.add(tab_settings, text="Settings")

    frame_settings = tk.Frame(tab_settings, bg="white")
    frame_settings.pack(fill="both", expand=True, padx=20, pady=20)

    fields = [
        ("Step 1 Spin (s):", spin1_var),
        ("Step 1 LED (s):", led1_var),
        ("Step 2 Total (s):", step2_var),
        ("Motor Speed (1000-2000):", speed_var),
    ]

    for i, (label_text, var) in enumerate(fields):
        tk.Label(frame_settings, text=label_text, bg="white", font=("Helvetica", 11)).grid(
            row=i, column=0, sticky="e", padx=8, pady=8
        )
        tk.Entry(frame_settings, textvariable=var, width=14, font=("Helvetica", 11)).grid(
            row=i, column=1, sticky="w", padx=8, pady=8
        )

    tk.Button(
        frame_settings,
        text="Apply Settings",
        command=apply_custom_values,
        bg="#444",
        fg="white",
        width=18
    ).grid(row=5, column=0, columnspan=2, pady=16)

    # MANUAL TAB
    tab_manual = tk.Frame(notebook, bg="white")
    notebook.add(tab_manual, text="Manual Control")

    frame_manual = tk.Frame(tab_manual, bg="white")
    frame_manual.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame_manual, text="Manual Motor Speed:", bg="white", font=("Helvetica", 11)).grid(
        row=0, column=0, padx=8, pady=10, sticky="e"
    )
    tk.Entry(frame_manual, textvariable=manual_speed_var, width=12, font=("Helvetica", 11)).grid(
        row=0, column=1, padx=8, pady=10, sticky="w"
    )

    tk.Button(frame_manual, text="Send Speed", command=send_motor_speed, bg="#007acc", fg="white", width=14).grid(
        row=0, column=2, padx=8, pady=10
    )
    tk.Button(frame_manual, text="LED ON", command=led_on, bg="#28a745", fg="white", width=12).grid(
        row=1, column=0, padx=8, pady=10
    )
    tk.Button(frame_manual, text="LED OFF", command=led_off, bg="#666666", fg="white", width=12).grid(
        row=1, column=1, padx=8, pady=10
    )
    tk.Button(frame_manual, text="Motor STOP", command=motor_stop, bg="#aa3333", fg="white", width=14).grid(
        row=1, column=2, padx=8, pady=10
    )

    tk.Button(frame_manual, text="LED ONLY ON", command=led_only_on, bg="#1f9d55", fg="white", width=14).grid(
        row=2, column=0, padx=8, pady=10
    )
    tk.Button(frame_manual, text="LED ONLY OFF", command=led_only_off, bg="#555555", fg="white", width=14).grid(
        row=2, column=1, padx=8, pady=10
    )

    # SERIAL LOG TAB
    tab_log = tk.Frame(notebook, bg="white")
    notebook.add(tab_log, text="Serial Log")

    frame_log = tk.Frame(tab_log, bg="white")
    frame_log.pack(fill="both", expand=True, padx=10, pady=10)

    serial_log = scrolledtext.ScrolledText(frame_log, font=("Consolas", 10))
    serial_log.pack(fill="both", expand=True, pady=(0, 10))

    tk.Button(
        frame_log,
        text="Clear Log",
        command=lambda: serial_log.delete("1.0", tk.END),
        bg="#444",
        fg="white",
        width=14
    ).pack()


# -----------------------------
# Close
# -----------------------------
def on_close():
    try:
        stop_event.set()
        send_command("LED OFF MOTOR 1000")
        time.sleep(0.2)
        disconnect_serial(silent=True)
    except Exception:
        pass
    root.destroy()


# -----------------------------
# Main GUI
# -----------------------------
root = tk.Tk()
root.title("Spinning Desicurer Control")
root.geometry("1280x1900")
root.configure(bg="white")
root.protocol("WM_DELETE_WINDOW", on_close)

status_var = tk.StringVar(value="Status: Ready")
phase_var = tk.StringVar(value="Phase: Idle")
connection_var = tk.StringVar(value="Connection: Not connected")
last_command_var = tk.StringVar(value="Last Command: None")
timer_var = tk.StringVar(value="")
port_var = tk.StringVar()

spin1_var = tk.StringVar(value=str(step1_spin_duration))
led1_var = tk.StringVar(value=str(step1_led_duration))
step2_var = tk.StringVar(value=str(step2_total_duration))
speed_var = tk.StringVar(value=str(motor_speed))
manual_speed_var = tk.StringVar(value=str(motor_speed))

header = tk.Label(
    root,
    text="Spinning Desicurer Controller",
    font=("Helvetica", 18, "bold"),
    bg="white"
)
header.pack(pady=12)

frame_conn = tk.Frame(root, bg="white")
frame_conn.pack(pady=8)

tk.Label(frame_conn, text="Port:", bg="white", font=("Helvetica", 11)).grid(row=0, column=0, padx=4, pady=4)

port_combo = ttk.Combobox(frame_conn, textvariable=port_var, width=14, state="readonly")
port_combo.grid(row=0, column=1, padx=4, pady=4)

btn_connect = tk.Button(frame_conn, text="Connect", command=lambda: connect_serial(port_var.get().strip()), bg="#007acc", fg="white", width=10)
btn_connect.grid(row=0, column=2, padx=4, pady=4)

btn_reconnect = tk.Button(frame_conn, text="Reconnect", command=reconnect_serial, bg="#007acc", fg="white", width=10)
btn_reconnect.grid(row=0, column=3, padx=4, pady=4)

btn_disconnect = tk.Button(frame_conn, text="Disconnect", command=disconnect_serial, bg="#aa3333", fg="white", width=10)
btn_disconnect.grid(row=0, column=4, padx=4, pady=4)

connection_label = tk.Label(root, textvariable=connection_var, bg="white", fg="red", font=("Helvetica", 11, "bold"))
connection_label.pack(pady=4)

frame_main = tk.Frame(root, bg="white")
frame_main.pack(pady=12)

btn_step1 = tk.Button(frame_main, text="Step 1", command=step1_sequence, width=20, height=2, bg="#007acc", fg="white", font=("Helvetica", 40, "bold"))
btn_step1.grid(row=0, column=0, padx=8, pady=8)

btn_step2 = tk.Button(frame_main, text="Step 2", command=step2_sequence, width=20, height=2, bg="#007acc", fg="white", font=("Helvetica", 40, "bold"))
btn_step2.grid(row=0, column=1, padx=8, pady=8)

btn_stop = tk.Button(frame_main, text="STOP", command=stop_sequence, width=20, height=2, bg="red", fg="white", font=("Helvetica", 40, "bold"))
btn_stop.grid(row=1, column=0, columnspan=2, padx=8, pady=8)

timer_label = tk.Label(root, textvariable=timer_var, font=("Helvetica", 16, "bold"), bg="white")
timer_label.pack(pady=0)

phase_label = tk.Label(root, textvariable=phase_var, font=("Helvetica", 12, "bold"), bg="white", fg="#444")
phase_label.pack(pady=0)

status_label = tk.Label(root, textvariable=status_var, fg="blue", font=("Helvetica", 12, "bold"), bg="white")
status_label.pack(pady=0)

last_command_label = tk.Label(root, textvariable=last_command_var, fg="#333333", font=("Helvetica", 10), bg="white")
last_command_label.pack(pady=0)

frame_tools = tk.Frame(root, bg="white")
frame_tools.pack(pady=15)

btn_advanced = tk.Button(
    frame_tools,
    text="Open Advanced Controls",
    command=open_advanced_window,
    bg="#444",
    fg="white",
    width=24,
    height=2,
    font=("Helvetica", 11, "bold")
)
btn_advanced.pack()

refresh_ports()
if not port_var.get():
    auto_port = auto_select_port()
    if auto_port:
        port_var.set(auto_port)

if port_var.get():
    connect_serial(port_var.get())

root.mainloop()