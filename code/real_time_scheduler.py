import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class Task:
    def __init__(self, id, period, execution_time):
        self.id = id
        self.period = period
        self.execution_time = execution_time
        self.deadline = period  # Deadline equals period
        self.remaining_time = execution_time
        self.next_deadline = period

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time CPU Scheduling for IoT Devices")
        self.tasks = []
        self.task_id = 1

        # UI Elements
        tk.Label(root, text="Period (ms):").grid(row=0, column=0, padx=5, pady=5)
        self.period_entry = tk.Entry(root)
        self.period_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Execution Time (ms):").grid(row=1, column=0, padx=5, pady=5)
        self.exec_entry = tk.Entry(root)
        self.exec_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(root, text="Add Task", command=self.add_task).grid(row=2, column=0, columnspan=2, pady=5)

        tk.Label(root, text="Tasks Added:").grid(row=3, column=0, padx=5, pady=5)
        self.task_list = tk.Text(root, height=5, width=40)
        self.task_list.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(root, text="Simulation Time (ms):").grid(row=4, column=0, padx=5, pady=5)
        self.time_entry = tk.Entry(root)
        self.time_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(root, text="Run RMS", command=lambda: self.run_simulation("RMS")).grid(row=5, column=0, pady=5)
        tk.Button(root, text="Run EDF", command=lambda: self.run_simulation("EDF")).grid(row=5, column=1, pady=5)

        self.result_label = tk.Label(root, text="Results: ")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=5)

    def add_task(self):
        try:
            period = int(self.period_entry.get())
            execution_time = int(self.exec_entry.get())
            if period <= 0 or execution_time <= 0 or execution_time > period:
                messagebox.showerror("Error", "Invalid period or execution time!")
                return
            task = Task(self.task_id, period, execution_time)
            self.tasks.append(task)
            self.task_list.insert(tk.END, f"Task {self.task_id}: Period={period}, Exec={execution_time}\n")
            self.task_id += 1
            self.period_entry.delete(0, tk.END)
            self.exec_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers!")

    def calculate_utilization(self):
        return sum(task.execution_time / task.period for task in self.tasks)

    def lcm(self, numbers):
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        def lcm_pair(a, b):
            return abs(a * b) // gcd(a, b)
        result = numbers[0]
        for i in range(1, len(numbers)):
            result = lcm_pair(result, numbers[i])
        return result

    def run_simulation(self, algorithm):
        if not self.tasks:
            messagebox.showerror("Error", "No tasks added!")
            return
        try:
            total_time = int(self.time_entry.get())
            if total_time <= 0:
                messagebox.showerror("Error", "Invalid simulation time!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid simulation time!")
            return

        utilization = self.calculate_utilization()
        if algorithm == "RMS":
            hyperperiod = self.lcm([task.period for task in self.tasks])
            total_time = min(total_time, hyperperiod)  # Limit to hyperperiod for RMS
            if utilization > 0.693:
                messagebox.showwarning("Warning", "Utilization exceeds RMS schedulability bound (69.3%)!")
        else:
            if utilization > 1.0:
                messagebox.showwarning("Warning", "Utilization exceeds EDF schedulability bound (100%)!")

        schedule, missed_deadlines = self.simulate(algorithm, total_time)
        self.show_schedule(schedule, total_time, algorithm)
        self.result_label.config(text=f"Results: Utilization={utilization:.2%}, Missed Deadlines={missed_deadlines}")

    def simulate(self, algorithm, total_time):
        schedule = []
        missed_deadlines = 0
        tasks = [Task(t.id, t.period, t.execution_time) for t in self.tasks]
        
        for t in range(total_time):
            # Reset tasks at their period boundaries
            for task in tasks:
                if t % task.period == 0:
                    task.remaining_time = task.execution_time
                    task.next_deadline = t + task.deadline

            # Check for missed deadlines
            for task in tasks:
                if t == task.next_deadline and task.remaining_time > 0:
                    missed_deadlines += 1

            # Select task to run
            running_task = None
            if algorithm == "RMS":
                available = [task for task in tasks if task.remaining_time > 0]
                if available:
                    running_task = min(available, key=lambda x: x.period)
            else:  # EDF
                available = [task for task in tasks if task.remaining_time > 0]
                if available:
                    running_task = min(available, key=lambda x: x.next_deadline)

            # Execute task
            if running_task:
                schedule.append(running_task.id)
                running_task.remaining_time -= 1
            else:
                schedule.append(0)  # Idle

        return schedule, missed_deadlines

    def show_schedule(self, schedule, total_time, algorithm):
        # Create a new Tkinter window for the Gantt chart
        chart_window = tk.Toplevel(self.root)
        chart_window.title(f"{algorithm} Gantt Chart")

        # Create Matplotlib figure
        fig, ax = plt.subplots(figsize=(10, len(self.tasks) * 0.5 + 1))
        for task in self.tasks:
            y = task.id
            for t in range(total_time):
                if schedule[t] == task.id:
                    ax.fill_between([t, t+1], [y-0.4, y-0.4], [y+0.4, y+0.4], color=f"C{task.id}")
        ax.set_yticks([task.id for task in self.tasks])
        ax.set_yticklabels([f"Task {task.id}" for task in self.tasks])
        ax.set_xticks(range(0, total_time + 1, max(1, total_time // 10)))
        ax.set_xlabel("Time (ms)")
        ax.set_ylabel("Tasks")
        ax.set_title(f"{algorithm} Scheduling Timeline")
        ax.grid(True, axis='x')

        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Save the plot as well
        plt.savefig('schedule.png')
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()