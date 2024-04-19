import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from math import radians, sin, cos, sqrt, asin
import uuid


class CityManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def add_city(self, city_name, latitude, longitude):
        city_id = str(uuid.uuid4())
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cities (city_id, city_name, latitude, longitude) VALUES (?, ?, ?, ?)",
                       (city_id, city_name, latitude, longitude))
        conn.commit()
        conn.close()

    def load_cities_data(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT city_name, latitude, longitude FROM cities ORDER BY city_name;")
        cities_data = cursor.fetchall()
        conn.close()
        return cities_data


class CityDistanceCalculator:
    EARTH_RADIUS = 6371

    def __init__(self, root_widget, city_manager_instance):
        self.result_label = None
        self.calculate_button = None
        self.add_city_button = None
        self.city2_combobox = None
        self.city2_label = None
        self.city1_combobox = None
        self.city1_label = None
        self.cities_data = None
        self.root = root_widget
        self.root.title("Calculation of distance between cities")

        # Setting window size
        self.root.geometry("400x200")

        # Getting screen sizes
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculating coordinates to position the window in the center of the screen
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2

        # Setting the window position
        self.root.geometry(f"400x200+{x}+{y}")

        self.city_manager = city_manager_instance

        self.load_cities_data()
        self.create_widgets()

    def load_cities_data(self):
        self.cities_data = self.city_manager.load_cities_data()

    def create_widgets(self):
        self.city1_label = ttk.Label(self.root, text="Select first city:")
        self.city1_label.grid(row=0, column=0, padx=10, pady=10)
        self.city1_combobox = ttk.Combobox(self.root, values=[city[0] for city in self.cities_data])
        self.city1_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.city2_label = ttk.Label(self.root, text="Select second city:")
        self.city2_label.grid(row=1, column=0, padx=10, pady=10)
        self.city2_combobox = ttk.Combobox(self.root, values=[city[0] for city in self.cities_data])
        self.city2_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.add_city_button = ttk.Button(self.root, text="Add new city", command=self.add_new_city)
        self.add_city_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.calculate_button = ttk.Button(self.root, text="Calculate distance", command=self.calculate_distance)
        self.calculate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.result_label = ttk.Label(self.root, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def add_new_city(self):
        # Creating a Dialog Box
        dialog = tk.Toplevel(self.root)
        dialog.title("Adding a new city")

        # Creating and placing widgets in a dialog box
        city_label = ttk.Label(dialog, text="City:")
        city_label.grid(row=0, column=0, padx=10, pady=5)
        city_entry = ttk.Entry(dialog)
        city_entry.grid(row=0, column=1, padx=10, pady=5)

        latitude_label = ttk.Label(dialog, text="Latitude:")
        latitude_label.grid(row=1, column=0, padx=10, pady=5)
        latitude_entry = ttk.Entry(dialog)
        latitude_entry.grid(row=1, column=1, padx=10, pady=5)

        longitude_label = ttk.Label(dialog, text="Longitude:")
        longitude_label.grid(row=2, column=0, padx=10, pady=5)
        longitude_entry = ttk.Entry(dialog)
        longitude_entry.grid(row=2, column=1, padx=10, pady=5)

        save_button = ttk.Button(dialog, text="Save new city",
                                 command=lambda: self.save_city(dialog, city_entry.get(), latitude_entry.get(),
                                                                longitude_entry.get()))
        save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Centering a window on the screen
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        x = (screen_width - dialog.winfo_width()) // 2
        y = (screen_height - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Binding to the window close event
        dialog.protocol("WM_DELETE_WINDOW", lambda: self.on_close(dialog))

    def save_city(self, dialog, city_name, latitude, longitude):
        if not city_name or not latitude or not longitude:
            tk.messagebox.showerror("Error", "Enter city name, latitude and longitude")
            return

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            tk.messagebox.showerror("Error", "Enter correct coordinates")
            return

        # Checking if entered city exists in the database to avoid duplicates
        for city_data in self.cities_data:
            if city_name == city_data[0]:
                tk.messagebox.showerror("Error", f"City '{city_name}' already exists in the database")
                return

        self.city_manager.add_city(city_name, latitude, longitude)
        self.load_cities_data()
        self.update_combobox_values()
        dialog.destroy()

    @staticmethod
    def on_close(dialog):
        dialog.destroy()

    def update_combobox_values(self):
        self.city1_combobox["values"] = [city[0] for city in self.cities_data]
        self.city2_combobox["values"] = [city[0] for city in self.cities_data]

    def calculate_distance(self):
        city1_index = self.city1_combobox.current()
        city2_index = self.city2_combobox.current()

        if city1_index == city2_index:
            self.result_label.config(text="Error: Choose different cities!")
            return

        city1_data = self.cities_data[city1_index]
        city2_data = self.cities_data[city2_index]

        city1_name, city1_lat, city1_lon = city1_data
        city2_name, city2_lat, city2_lon = city2_data

        city1_lat_rad, city1_lon_rad = radians(float(city1_lat)), radians(float(city1_lon))
        city2_lat_rad, city2_lon_rad = radians(float(city2_lat)), radians(float(city2_lon))

        delta_lat = city2_lat_rad - city1_lat_rad
        delta_lon = city2_lon_rad - city1_lon_rad

        a = sin(delta_lat / 2) ** 2 + cos(city1_lat_rad) * cos(city2_lat_rad) * sin(delta_lon / 2) ** 2
        c = 2 * asin(sqrt(a))
        distance = self.EARTH_RADIUS * c

        self.result_label.config(text=f"Distance between cities {city1_name} and {city2_name}: {distance:.2f} km")


if __name__ == "__main__":
    root = tk.Tk()
    city_manager = CityManager("cities.db")
    app = CityDistanceCalculator(root, city_manager)
    root.mainloop()
