# Real-time-iot-scheduler
To run this python code you will the require the below libraries:
  tkinter
  matplotlib
  math

to install the required libraries use the below command in console:
  pip install matplotlib

no need to install tkinter and math as they are pre-installed with python.

This project is a real-time CPU scheduling simulator for IoT devices, built with a graphical interface using Python's `tkinter`. Here's a brief description:

The application allows users to simulate **real-time scheduling algorithms**, specifically:
1. **Rate-Monotonic Scheduling (RMS)** – A static-priority algorithm where tasks with shorter periods are given higher priority.
2. **Earliest Deadline First (EDF)** – A dynamic-priority algorithm where tasks closer to their deadlines are prioritized.

### Features:
- **Task Addition**: Users can add tasks by specifying their period and execution time. Each task is uniquely identified.
- **Simulation Time**: Users can specify the total simulation duration in milliseconds.
- **Utilization Calculation**: The tool calculates the total system utilization and warns the user if the schedulability bound for RMS or EDF is exceeded.
- **Gantt Chart Visualization**: The output schedule is displayed as a Gantt chart, helping users visualize task execution over time.
- **Missed Deadlines Reporting**: The simulation checks for missed deadlines and informs the user.

### How It Works:
1. Users input task details and simulation parameters through an intuitive interface.
2. Tasks are added to a list and their parameters are validated.
3. The scheduler runs the selected algorithm (RMS or EDF), simulating task execution, managing deadlines, and handling task priorities.
4. The results are displayed, including the system's utilization and any missed deadlines. Additionally, a Gantt chart shows the task execution timeline.

This tool is particularly useful for researchers, developers, or students studying real-time operating systems or IoT-based applications. Its modular design and clear visualization make it an excellent educational resource. Let me know if you'd like to improve or expand this project further!
