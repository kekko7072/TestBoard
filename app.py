import customtkinter as ctk
import serial
import serial.tools.list_ports
import time # Imported time to handle the Arduino reset delay

class GridSerialApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("2x2 Control Grid")
        self.geometry("500x450") # Made slightly taller to fit the connect button

        self.serial_conn = None # Variable to store the persistent connection

        # Configure the grid system (2 columns, equal weight)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((1, 2), weight=1)

        # --- Header ---
        self.label = ctk.CTkLabel(self, text="Hardware Control Pad", font=("Arial", 22, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        # --- Row 1: The Main Controls ---
        self.on_btn = ctk.CTkButton(self, text="Led ON", fg_color="#2ecc71", # Green
                                    command=lambda: self.send_command("LED_ON"))
        self.on_btn.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.off_btn = ctk.CTkButton(self, text="Led OFF", fg_color="#e74c3c", # Red
                                     command=lambda: self.send_command("LED_OFF"))
        self.off_btn.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        # --- Row 2: Generic / Extra Buttons ---
        self.gen1_btn = ctk.CTkButton(self, text="Lock ON", fg_color="#2ecc71", # Green
                                      command=lambda: self.send_command("Lock_ON"))
        self.gen1_btn.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # FIXED: Removed the extra \n from the command string here
        self.gen2_btn = ctk.CTkButton(self, text="Lock OFF", fg_color="#e74c3c", # Red
                                      command=lambda: self.send_command("Lock_OFF"))
        self.gen2_btn.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        # --- Row 3: Port Selection & Connect Button ---
        self.port_var = ctk.StringVar(value="Select Port")
        self.port_menu = ctk.CTkOptionMenu(self, variable=self.port_var, values=self.get_ports())
        self.port_menu.grid(row=3, column=0, padx=20, pady=10)

        self.connect_btn = ctk.CTkButton(self, text="Connect", command=self.connect_serial)
        self.connect_btn.grid(row=3, column=1, padx=20, pady=10)

        # --- Row 4: Status Label ---
        self.status_label = ctk.CTkLabel(self, text="Status: Disconnected", text_color="gray")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

    def get_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports if ports else ["No Ports Found"]

    def connect_serial(self):
        port = self.port_var.get()
        if port in ["Select Port", "No Ports Found"]:
            self.status_label.configure(text="Error: Select Port First", text_color="red")
            return

        # Close any existing connection before opening a new one
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()

        try:
            self.status_label.configure(text="Connecting (Waiting for reset)...", text_color="orange")
            self.update() # Force UI to update text immediately

            # Open the persistent connection
            self.serial_conn = serial.Serial(port, 9600, timeout=1)
            
            # IMPORTANT: Wait 2 seconds for Arduino to finish booting up
            time.sleep(2) 

            self.status_label.configure(text=f"Connected: {port}", text_color="green")
        except Exception as e:
            self.status_label.configure(text="Port Error: Could not connect", text_color="red")
            self.serial_conn = None

    def send_command(self, cmd):
        # Check if we have an active, open connection first
        if not self.serial_conn or not self.serial_conn.is_open:
            self.status_label.configure(text="Error: Click Connect First!", text_color="red")
            return

        try:
            # We add the \n right here, so your Arduino can read it
            self.serial_conn.write(f"{cmd}\n".encode('utf-8'))
            self.status_label.configure(text=f"Sent: {cmd}", text_color="green")
        except Exception as e:
            self.status_label.configure(text="Send Error (Disconnected?)", text_color="red")
            self.serial_conn = None

if __name__ == "__main__":
    app = GridSerialApp()
    app.mainloop()