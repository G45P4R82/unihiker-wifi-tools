"""Touch-friendly WiFi Tools launcher for the Unihiker."""

import os
import tkinter as tk
from tkinter import messagebox, simpledialog

from . import network
from .portal import TrainingPortal


class WiFiToolsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Tools")
        self.root.geometry("320x240")
        self.root.configure(bg="#101820")
        self.portal = None
        self.previous_connection = None
        self.portal_ap_active = False
        self._build()

    def _build(self):
        tk.Label(self.root, text="WIFI TOOLS", fg="#7ee787", bg="#101820", font=("Sans", 18, "bold")).pack(pady=8)
        self.status = tk.Label(self.root, text="Pronto", fg="white", bg="#101820", wraplength=290)
        self.status.pack(pady=3)
        grid = tk.Frame(self.root, bg="#101820")
        grid.pack(fill="both", expand=True, padx=8, pady=5)
        buttons = [
            ("Status", self.show_status),
            ("Scan Wi-Fi", self.show_scan),
            ("Conectar", self.connect),
            ("Criar AP", self.start_ap),
            ("Portal treino", self.start_portal),
            ("Parar portal", self.stop_portal),
        ]
        for index, (label, command) in enumerate(buttons):
            button = tk.Button(grid, text=label, command=command, font=("Sans", 11), height=2)
            button.grid(row=index // 2, column=index % 2, sticky="nsew", padx=3, pady=3)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)
        grid.rowconfigure(2, weight=1)

    def run_action(self, action):
        try:
            return action()
        except Exception as error:
            messagebox.showerror("WiFi Tools", str(error))
            self.status.config(text="Erro: " + str(error)[:80])
            return None

    def show_status(self):
        values = self.run_action(network.status)
        if values is not None:
            text = "Estado: {0}\nSSID: {1}\nIP: {2}".format(
                values.get("GENERAL.STATE", "?"),
                values.get("GENERAL.CONNECTION", "-"),
                values.get("IP4.ADDRESS[1]", "-"),
            )
            self.status.config(text=text)

    def show_scan(self):
        networks = self.run_action(network.scan)
        if networks is None:
            return
        lines = ["{0}  {1}%  ch {2}".format(item["ssid"][:22], item["signal"], item["channel"]) for item in networks[:8]]
        messagebox.showinfo("Redes encontradas", "\n".join(lines) or "Nenhuma rede encontrada")
        self.status.config(text="{} redes encontradas".format(len(networks)))

    def connect(self):
        ssid = simpledialog.askstring("Conectar", "SSID:", parent=self.root)
        if not ssid:
            return
        password = simpledialog.askstring("Conectar", "Senha (vazio para rede aberta):", show="*", parent=self.root)
        self.run_action(lambda: network.connect(ssid, password or None))
        self.status.config(text="Conexão solicitada: " + ssid[:40])

    def start_ap(self):
        if not messagebox.askyesno("Criar AP", "Isso pode trocar a conexão Wi-Fi atual. Continuar?", parent=self.root):
            return
        ssid = simpledialog.askstring("Criar AP", "SSID do AP:", initialvalue="WiFiTools-Lab", parent=self.root)
        password = simpledialog.askstring("Criar AP", "Senha do AP (mínimo 8 caracteres):", show="*", parent=self.root)
        if ssid and password:
            self.run_action(lambda: network.hotspot_start(ssid, password))
            self.status.config(text="AP ativo: " + ssid[:40])

    def start_portal(self):
        if self.portal:
            self.status.config(text="Portal já está ativo em http://0.0.0.0:8081")
            return
        if not messagebox.askyesno("Portal autorizado", "Iniciar portal de treinamento em laboratório?", parent=self.root):
            return
        ssid = simpledialog.askstring("Portal autorizado", "SSID da campanha:", initialvalue="WiFiTools-Training", parent=self.root)
        password = simpledialog.askstring("Portal autorizado", "Senha do AP (mínimo 8 caracteres):", show="*", parent=self.root)
        if not ssid or not password:
            return
        try:
            self.previous_connection = network.status().get("GENERAL.CONNECTION")
            network.hotspot_start(ssid, password)
            self.portal = TrainingPortal(port=8081, data_dir=os.path.join(os.getcwd(), "portal-data"))
            self.portal.start()
            self.portal_ap_active = True
            self.status.config(text="AP + portal ativos\nhttp://10.42.0.1:8081")
        except Exception:
            if self.portal:
                self.portal.stop()
                self.portal = None
            if self.portal_ap_active:
                network.hotspot_stop()
                self.portal_ap_active = False
            raise

    def stop_portal(self):
        if self.portal:
            self.portal.stop()
            self.portal = None
            if self.portal_ap_active:
                try:
                    network.hotspot_stop()
                finally:
                    self.portal_ap_active = False
            if self.previous_connection and self.previous_connection != "WiFiTools-AP":
                try:
                    network.run(["nmcli", "connection", "up", "id", self.previous_connection], timeout=30)
                except Exception:
                    pass
            self.previous_connection = None
            self.status.config(text="Portal parado")
        else:
            self.status.config(text="Nenhum portal ativo")

    def close(self):
        self.stop_portal()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = WiFiToolsApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == "__main__":
    main()
