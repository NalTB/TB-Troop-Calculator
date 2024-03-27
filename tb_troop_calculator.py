import tkinter as tk
from tkinter import ttk

class TroopCalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("TB Troop Calculator - WPT Nalmerin")
        master.geometry("600x440")
        
        self.total_capacity_var = tk.StringVar()
        self.level_vars = {level: tk.BooleanVar() for level in range(1, 6)}
        self.troop_counts = {"Riders": {}, "Archers": {}, "Spearman": {}}
        
        self.setup_ui()
    
    def setup_ui(self):
        tk.Label(self.master, text="Total Capacity:").pack()
        tk.Entry(self.master, textvariable=self.total_capacity_var).pack()
        
        level_frame = tk.Frame(self.master)
        level_frame.pack(pady=10)
        tk.Label(level_frame, text="Select Levels:").pack(side=tk.LEFT)
        for level, var in self.level_vars.items():
            tk.Checkbutton(level_frame, text=f"Level {level}", variable=var).pack(side=tk.LEFT)
        
        columns_frame = tk.Frame(self.master)
        columns_frame.pack()
        for troop_type in self.troop_counts.keys():
            frame = tk.Frame(columns_frame)
            frame.pack(side=tk.LEFT, padx=20)
            tk.Label(frame, text=troop_type).pack()
            for level in range(1, 6):
                tk.Label(frame, text=f"Level {level}").pack()
                self.troop_counts[troop_type][level] = tk.StringVar()
                tk.Entry(frame, textvariable=self.troop_counts[troop_type][level], state='readonly').pack()
        
        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Calculate", command=self.calculate).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=10)
    def calculate(self):
        try:
            total_capacity = int(self.total_capacity_var.get())
        except ValueError:
            return

        selected_levels = sorted([level for level, var in self.level_vars.items() if var.get()])
        if not selected_levels:
            return

        capacity_per_type = total_capacity / 3

        for troop_type in ["Riders", "Archers", "Spearman"]:
            adjusted_capacity = capacity_per_type / (2 if troop_type == "Riders" else 1)
            base_amount = adjusted_capacity / sum([1 / (2 ** i) for i in range(len(selected_levels))])

            for i, level in enumerate(selected_levels):
                # Directly use the adjusted capacity for calculation without additional division
                amount_for_level = base_amount * (1 / (2 ** i))
                self.troop_counts[troop_type][level].set(f"{int(amount_for_level):,}")

            # Clear output for non-selected levels
            for level in range(1, 6):
                if level not in selected_levels:
                    self.troop_counts[troop_type][level].set("")
    def reset(self):
        # This method now clears outputs and unchecks all level selection checkboxes
        for troop_type in self.troop_counts.keys():
            for level in range(1, 6):
                self.troop_counts[troop_type][level].set("")
        for var in self.level_vars.values():
            var.set(False)  # Uncheck all level selection checkboxes

    def clear_all(self):
        # This method clears everything including the total capacity field
        self.reset()  # Reuse the reset functionality to clear checkboxes and outputs
        self.total_capacity_var.set("")  # Clear the total capacity field

def run_app():
    root = tk.Tk()
    app = TroopCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
