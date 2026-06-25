import os
import sqlite3

DB_FILE = 'transit_network_final.db'

def run_clean_db_generation():
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print("Old database cleared successfully.")
        except Exception as e:
            print(f"Bypass Notice: {e}")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE buses (id INTEGER PRIMARY KEY AUTOINCREMENT, bus_name TEXT NOT NULL, contact_number TEXT NOT NULL, bus_type TEXT NOT NULL)')
    cursor.execute('CREATE TABLE routes (id INTEGER PRIMARY KEY AUTOINCREMENT, route_code TEXT UNIQUE NOT NULL, source TEXT NOT NULL, destination TEXT NOT NULL, via_summary TEXT NOT NULL)')
    cursor.execute('CREATE TABLE route_stops (id INTEGER PRIMARY KEY AUTOINCREMENT, route_id INTEGER, stop_order INTEGER NOT NULL, station_name TEXT NOT NULL, distance_offset INTEGER NOT NULL, minutes_offset INTEGER NOT NULL, location_type TEXT NOT NULL, FOREIGN KEY (route_id) REFERENCES routes (id))')
    cursor.execute('CREATE TABLE schedules (id INTEGER PRIMARY KEY AUTOINCREMENT, bus_id INTEGER, route_id INTEGER, base_departure_time TEXT NOT NULL, per_km_rate REAL DEFAULT 2.0, FOREIGN KEY (bus_id) REFERENCES buses (id), FOREIGN KEY (route_id) REFERENCES routes (id))')

    operators = [
        ("Shekhar Travels", "94144XXXXX", "Express Deluxe"),
        ("Salasar Darshan Travels", "98292XXXXX", "Express Seater"),
        ("Gajraj Bus Service", "96100XXXXX", "AC Sleeper"),
        ("Ropia Mahaveer Travel", "70140XXXXX", "Sleeper/Seater"),
        ("Laxmi Traveller", "80035XXXXX", "Local Seater"),
        ("IBS Tour & Travels", "94141XXXXX", "Express"),
        ("Mahaveer Travels", "97840XXXXX", "Deluxe Seater")
    ]
    cursor.executemany("INSERT INTO buses (bus_name, contact_number, bus_type) VALUES (?, ?, ?)", operators)

    routes_list = [
        ("LAD-JOD-KAN", "Ladnun", "Jodhpur", "via Kanuta & Deh Corridor"),
        ("JOD-LAD-KAN", "Jodhpur", "Ladnun", "via Deh & Kanuta [RETURN]"),
        ("LAD-JAI-SIK", "Sujangarh", "Jaipur", "via Sikar Highway Corridor"),
        ("JAI-LAD-SIK", "Jaipur", "Sujangarh", "via Sikar Highway [RETURN]"),
        ("LAD-JAI-DID", "Sujangarh", "Jaipur", "via Didwana Interior Corridor"),
        ("JAI-LAD-DID", "Jaipur", "Sujangarh", "via Didwana Interior [RETURN]")
    ]
    cursor.executemany("INSERT INTO routes (route_code, source, destination, via_summary) VALUES (?, ?, ?, ?)", routes_list)

    stops_data = [
        # 1. Ladnun -> Jodhpur
        (1, 1, "Ladnun", 0, 0, "Main Bus Stand"), (1, 2, "Nimbi Jodha", 16, 20, "Town Crossing"), (1, 3, "Kanuta", 32, 45, "Village T-Point"), (1, 4, "Hudas", 45, 62, "Village Chauraha"), (1, 5, "Deh", 58, 80, "Bypass Chauraha"), (1, 6, "Jayal", 72, 100, "Highway Hub"), (1, 7, "Nagaur", 88, 120, "Krishi Mandi Square"), (1, 8, "Khinvsar (Khimsar)", 133, 175, "Highway Fort Junction"), (1, 9, "Baori", 185, 240, "Toll Plaza Stop"), (1, 10, "Mandore", 215, 280, "Outer Outskirts"), (1, 11, "Jodhpur", 225, 300, "Raika Bagh Terminal"),
        # 2. Jodhpur -> Ladnun (RETURN)
        (2, 1, "Jodhpur", 0, 0, "Raika Bagh Terminal"), (2, 2, "Mandore", 10, 20, "Outer Outskirts"), (2, 3, "Baori", 40, 60, "Toll Plaza Stop"), (2, 4, "Khinvsar (Khimsar)", 92, 125, "Highway Fort Junction"), (2, 5, "Nagaur", 137, 180, "Krishi Mandi Square"), (2, 6, "Jayal", 153, 200, "Highway Hub"), (2, 7, "Deh", 167, 220, "Bypass Chauraha"), (2, 8, "Hudas", 180, 238, "Village Chauraha"), (2, 9, "Kanuta", 193, 255, "Village T-Point"), (2, 10, "Nimbi Jodha", 209, 280, "Town Crossing"), (2, 11, "Ladnun", 225, 300, "Main Bus Stand"),
        
        # 3. Sujangarh -> Sikar -> Jaipur
        (3, 1, "Sujangarh", 0, 0, "Station Road Bypass"), (3, 2, "Ladnun", 14, 20, "Main Bus Stand"), (3, 3, "Salasar", 43, 55, "Dham Temple Entrance"), (3, 4, "Laxmangarh", 72, 95, "NH-52 Flyover Below"), (3, 5, "Sikar", 102, 135, "Kalyan Circle Private Stand"), (3, 6, "Palasana", 128, 165, "Highway Bypass"), (3, 7, "Ringas Junction", 154, 195, "Khatu Shyam Ji Turning"), (3, 8, "Chomu", 182, 230, "Chomu Bypass Chauraha"), (3, 9, "Jaipur", 215, 275, "Sindhi Camp Bus Stand"),
        # 4. Jaipur -> Sikar -> Sujangarh (RETURN)
        (4, 1, "Jaipur", 0, 0, "Sindhi Camp Bus Stand"), (4, 2, "Chomu", 33, 45, "Chomu Bypass Chauraha"), (4, 3, "Ringas Junction", 61, 80, "Khatu Shyam Ji Turning"), (4, 4, "Palasana", 87, 110, "Highway Bypass"), (4, 5, "Sikar", 113, 140, "Kalyan Circle Private Stand"), (4, 6, "Laxmangarh", 143, 180, "NH-52 Flyover Below"), (4, 7, "Salasar", 172, 220, "Dham Temple Entrance"), (4, 8, "Ladnun", 201, 255, "Main Bus Stand"), (4, 9, "Sujangarh", 215, 275, "Station Road Bypass"),

        # 5. Sujangarh -> Didwana -> Jaipur
        (5, 1, "Sujangarh", 0, 0, "Outskirts Tiraha"), (5, 2, "Ladnun", 14, 20, "Main Bus Stand"), (5, 3, "Didwana", 45, 60, "Didwana Mega Highway Cut"), (5, 4, "Sanju", 65, 88, "Village Stand"), (5, 5, "Kuchaman City", 88, 120, "Private Bus Stand"), (5, 6, "Nawa City", 110, 150, "Salt Lake Bypass"), (5, 7, "Parbatsar", 125, 172, "Chauraha Intersection"), (5, 8, "Phulera Bypass", 132, 185, "Railway Crossing Junction"), (5, 9, "Jobner", 152, 210, "Main Market Road"), (5, 10, "Jaipur 200 Ft Bypass", 185, 250, "Ajmer Road Intersection"), (5, 11, "Jaipur", 195, 270, "Sindhi Camp Bus Stand"),
        # 6. Jaipur -> Didwana -> Sujangarh (RETURN)
        (6, 1, "Jaipur", 0, 0, "Sindhi Camp Bus Stand"), (6, 2, "Jaipur 200 Ft Bypass", 10, 20, "Ajmer Road Intersection"), (6, 3, "Jobner", 43, 60, "Main Market Road"), (6, 4, "Phulera Bypass", 63, 85, "Railway Crossing Junction"), (6, 5, "Parbatsar", 70, 98, "Chauraha Intersection"), (6, 6, "Nawa City", 85, 120, "Salt Lake Bypass"), (6, 7, "Kuchaman City", 107, 150, "Private Bus Stand"), (6, 8, "Sanju", 130, 182, "Village Stand"), (6, 9, "Didwana", 150, 210, "Mega Highway Cut"), (6, 10, "Ladnun", 181, 250, "Main Bus Stand"), (6, 11, "Sujangarh", 195, 270, "Outskirts Tiraha")
    ]
    cursor.executemany("INSERT INTO route_stops (route_id, stop_order, station_name, distance_offset, minutes_offset, location_type) VALUES (?, ?, ?, ?, ?, ?)", stops_data)

    schedules = [
        (1, 1, "06:00 AM", 2.0), (2, 1, "08:15 AM", 2.0), (3, 1, "10:30 AM", 2.1), (4, 1, "01:00 PM", 2.1), (5, 1, "03:30 PM", 2.0), (6, 1, "05:45 PM", 2.2), (7, 1, "08:00 PM", 2.4), (3, 1, "10:15 PM", 2.5),
        (1, 2, "05:30 AM", 2.0), (2, 2, "07:45 AM", 2.0), (4, 2, "11:00 AM", 2.1), (5, 2, "02:15 PM", 2.1), (6, 2, "04:30 PM", 2.0), (7, 2, "07:00 PM", 2.3), (1, 2, "09:30 PM", 2.4), (2, 2, "11:15 PM", 2.5),
        (1, 3, "02:15 AM", 1.9), (2, 3, "04:00 AM", 1.9), (7, 3, "05:30 AM", 2.0), (3, 3, "07:30 AM", 2.2), (4, 3, "10:00 AM", 2.0), (5, 3, "12:15 PM", 1.9), (6, 3, "03:00 PM", 2.1), (1, 3, "05:30 PM", 2.2),
        (2, 4, "06:15 AM", 1.9), (3, 4, "09:00 AM", 1.9), (4, 4, "12:30 PM", 2.0), (5, 4, "03:15 PM", 2.2), (6, 4, "05:45 PM", 2.0), (7, 4, "08:00 PM", 2.1), (1, 4, "10:15 PM", 2.3), (2, 4, "11:45 PM", 2.4),
        (5, 5, "05:00 AM", 1.8), (6, 5, "07:15 AM", 1.8), (1, 5, "09:30 AM", 2.0), (2, 5, "11:45 AM", 1.8), (3, 5, "02:00 PM", 2.0), (4, 5, "04:15 PM", 2.1), (5, 5, "06:30 PM", 2.2), (6, 5, "08:45 PM", 2.2),
        (1, 6, "04:30 AM", 1.8), (2, 6, "06:45 AM", 1.8), (3, 6, "09:15 AM", 2.0), (4, 6, "11:30 AM", 1.8), (5, 6, "01:45 PM", 2.0), (6, 6, "04:00 PM", 2.1), (7, 6, "07:15 PM", 2.2), (1, 6, "09:45 PM", 2.3)
    ]
    cursor.executemany("INSERT INTO schedules (bus_id, route_id, base_departure_time, per_km_rate) VALUES (?, ?, ?, ?)", schedules)

    conn.commit()
    conn.close()
    print("Database built cleanly with complete bidirectional cross-corridors.")

run_clean_db_generation()

