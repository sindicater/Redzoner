import tkinter as tk
from tkinter import messagebox
import requests
import json

# Sample data for testing
sample_data = [
    {
        "name": "Karatina Town",
        "coords": {"latitude": -0.6667, "longitude": 37.0833},
        "radius": 1500,
        "type": "safe",
        "crime_type": "theft",
        "crime_time": "2023-10-01T12:00:00Z",
        "safety_status": True
    },
    {
        "name": "Nairobi CBD",
        "coords": {"latitude": -1.286389, "longitude": 36.817223},
        "radius": 2000,
        "type": "unsafe",
        "crime_type": "burglary",
        "crime_time": "2023-10-02T14:30:00Z",
        "safety_status": False
    },
    {
        "name": "Kisumu City",
        "coords": {"latitude": -0.0917, "longitude": 34.7680},
        "radius": 1800,
        "type": "safe",
        "crime_type": "assault",
        "crime_time": "2023-10-03T09:45:00Z",
        "safety_status": True
    }
]

def send_data():
    url = "http://127.0.0.1:5000/data"
    headers = {'Content-Type': 'application/json'}
    for data in sample_data:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Data sent successfully: {data}")
        else:
            messagebox.showerror("Error", f"Failed to send data: {response.text}")

def get_data():
    url = "http://127.0.0.1:5000/data"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        messagebox.showinfo("Data Retrieved", json.dumps(data, indent=2))
    else:
        messagebox.showerror("Error", "Failed to retrieve data")

# Create the main window
root = tk.Tk()
root.title("Flask Backend Tester")

# Create buttons
send_button = tk.Button(root, text="Send Sample Data", command=send_data)
send_button.pack(pady=10)

get_button = tk.Button(root, text="Get Data", command=get_data)
get_button.pack(pady=10)

# Run the application
root.mainloop()
