import customtkinter as ctk
import subprocess
import sys
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PipManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Pip Manager")
        self.geometry("600x450")

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter package name (e.g., numpy)", width=300)
        self.entry.pack(pady=20)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.install_btn = ctk.CTkButton(self.btn_frame, text="Install", command=lambda: self.run_command("install"))
        self.install_btn.pack(side="left", padx=10)

        self.uninstall_btn = ctk.CTkButton(self.btn_frame, text="Uninstall", command=lambda: self.run_command("uninstall"))
        self.uninstall_btn.pack(side="left", padx=10)

        self.list_btn = ctk.CTkButton(self.btn_frame, text="List Installed", command=lambda: self.run_command("list"))
        self.list_btn.pack(side="left", padx=10)

        self.output_box = ctk.CTkTextbox(self, width=550, height=250)
        self.output_box.pack(pady=20)
        self.output_box.insert("0.0", "System ready. Waiting for input...\n")

    def run_command(self, action):
        package = self.entry.get()
        if action in ["install", "uninstall"] and not package:
            self.update_output("Error: Please enter a package name.\n")
            return

        self.update_output(f"Starting: {action} {package}...\n")
        threading.Thread(target=self.execute_pip, args=(action, package)).start()

    def execute_pip(self, action, package):
        try:
            cmd = [sys.executable, "-m", "pip", action]
            if action == "uninstall":
                cmd.append("-y")
            if package and action != "list":
                cmd.append(package)

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if stdout:
                self.update_output(stdout)
            if stderr:
                self.update_output(f"ERROR:\n{stderr}")
                
        except Exception as e:
            self.update_output(f"Exception occurred: {str(e)}\n")

    def update_output(self, text):
        self.output_box.insert(ctk.END, text + "\n")
        self.output_box.see(ctk.END)

if __name__ == "__main__":
    app = PipManager()
    app.mainloop()