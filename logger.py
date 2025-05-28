import csv
import os
from datetime import datetime

class PhysicsLogger:
    def __init__(self, filename=None):
        """
        Initialize the physics data logger
        
        Args:
            filename (str): Custom filename for the CSV. If None, generates timestamp-based name
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"projectile_data_{timestamp}.csv"
        
        self.filename = filename
        self.data = []
        self.headers = ['Time', 'X_Position', 'Y_Position', 'Velocity_X', 'Velocity_Y']
        
        # Create CSV file with headers
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
        
        print(f"Physics logger initialized. Data will be saved to: {self.filename}")
    
    def log_data(self, time, x_pos, y_pos, vel_x, vel_y):
        """
        Log physics data point
        
        Args:
            time (float): Time in seconds
            x_pos (float): X position in meters
            y_pos (float): Y position in meters
            vel_x (float): X velocity in m/s
            vel_y (float): Y velocity in m/s
        """
        data_point = [time, x_pos, y_pos, vel_x, vel_y]
        self.data.append(data_point)
        
        # Append to CSV file immediately
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data_point)
    
    def get_data_count(self):
        """Return the number of data points logged"""
        return len(self.data)
    
    def save_final(self):
        """
        Optional method to perform any final operations
        Currently just prints summary
        """
        print(f"Data logging complete. {len(self.data)} data points saved to {self.filename}")
        if self.data:
            print(f"Time range: {self.data[0][0]:.3f}s to {self.data[-1][0]:.3f}s")
    
    def clear_data(self):
        """Clear all logged data and reinitialize the CSV file"""
        self.data = []
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)