import tkinter as tk
from tkinter import messagebox
import re
import ipaddress


def calculate_address(ip, mask):
    if not validate_ip(ip):
        messagebox.showerror("Error", "Invalid IP. Format must be in decimal (0-255).")
        return
    if not validate_subnet_mask(mask):
        messagebox.showerror("Error",
                             "Invalid Subnet Mask. Must be in decimal format (e.g. 255.255.255.0) or in CIDR format (e.g. /24).")
        return

    try:
        if mask.startswith('/'):
            net = ipaddress.IPv4Network(f"{ip}{mask}", strict=False)
        else:
            net = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)

        network_address = str(net.network_address)
        broadcast_address = str(net.broadcast_address)
        available_hosts = net.num_addresses - 2 if net.num_addresses > 2 else 0

        label_ntwrk_value.config(text=network_address)
        label_brdcst_value.config(text=broadcast_address)
        label_hsts_value.config(text=str(available_hosts))

    except ValueError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def validate_input_ip(char):
    return char.isdigit() or char == '.'


def validate_input_mask(char):
    return char.isdigit() or char == '.' or char == '/'


def validate_ip(ip):
    pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                         r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    return pattern.match(ip) is not None


def validate_subnet_mask(mask):
    if mask.startswith('/'):
        return re.match(r"^/[0-9]{1,2}$", mask) is not None
    else:
        pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                             r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                             r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                             r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        return pattern.match(mask) is not None


def main_window():
    main_window = tk.Tk()
    main_window.title("IP address calculator")
    main_window.geometry("400x300")
    main_window.resizable(False, False)

    bg_color = "#266867"
    text_color = "#FFFFFF"
    main_window.configure(bg=bg_color)
    common_width = 30

    vcmd_ip = (main_window.register(validate_input_ip), '%S')
    vcmd_mask = (main_window.register(validate_input_mask), '%S')

    # ---------------------------------------------------------------------------------
    label_ip = tk.Label(main_window, text="IP Address: ", bg=bg_color, fg=text_color)
    label_ip.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="e")

    entry_ip = tk.Entry(main_window, width=common_width, validate="key", validatecommand=vcmd_ip)
    entry_ip.grid(row=0, column=1, padx=10, pady=10)

    # ---------------------------------------------------------------------------------
    label_msk = tk.Label(main_window, text="Subnet Mask: ", bg=bg_color, fg=text_color)
    label_msk.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="e")

    entry_msk = tk.Entry(main_window, width=common_width, validate="key", validatecommand=vcmd_mask)
    entry_msk.grid(row=1, column=1, padx=10, pady=10)

    # ---------------------------------------------------------------------------------
    button_add = tk.Button(main_window, bg="#1A4645", fg=text_color, text="Calculate IP",
                           command=lambda: calculate_address(entry_ip.get(), entry_msk.get()))
    button_add.grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
    # ---------------------------------------------------------------------------------

    label_ntwrk = tk.Label(main_window, text="Network Address: ", fg=text_color, bg=bg_color)
    label_ntwrk.grid(row=3, column=0, padx=(10, 0), pady=10, sticky="e")

    global label_ntwrk_value
    label_ntwrk_value = tk.Label(main_window, text="", bg=bg_color, fg=text_color)
    label_ntwrk_value.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # ---------------------------------------------------------------------------------
    label_brdcst = tk.Label(main_window, text="Broadcast Address: ", fg=text_color, bg=bg_color)
    label_brdcst.grid(row=4, column=0, padx=(10, 0), pady=10, sticky="e")

    global label_brdcst_value
    label_brdcst_value = tk.Label(main_window, text="", bg=bg_color, fg=text_color)
    label_brdcst_value.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # ---------------------------------------------------------------------------------
    label_hsts = tk.Label(main_window, text="Available Hosts: ", bg=bg_color, fg=text_color)
    label_hsts.grid(row=5, column=0, padx=(10, 0), pady=10, sticky="e")

    global label_hsts_value
    label_hsts_value = tk.Label(main_window, text="", bg=bg_color, fg=text_color)
    label_hsts_value.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    # ---------------------------------------------------------------------------------
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=1)

    main_window.mainloop()


if __name__ == '__main__':
    main_window()
