import sqlite3
from datetime import datetime, timedelta
from flask import Flask, render_template_string, request

app = Flask(__name__)
DB_FILE = 'transit_network_final.db'

# --- PREMIUM MODERN UI DESIGN WITH CONDITIONAL TOGGLE —--
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Passenger Transit Portal</title>
    <style>
        :root { --bg-dark: #090d16; --card-bg: rgba(20, 28, 47, 0.7); --accent-neon: #00ffcc; --accent-pink: #ff007f; --text-muted: #8fa0c4; }
        body { font-family: 'Segoe UI', Roboto, sans-serif; background-color: var(--bg-dark); margin: 0; padding: 15px; color: #f0f4fc; }
        .wrapper { max-width: 650px; margin: 15px auto; background: var(--card-bg); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); padding: 25px; border-radius: 16px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); }
        h2 { text-align: center; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: 2px; font-size: 22px; margin-bottom: 25px; background: linear-gradient(to right, #00ffcc, #ff007f); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .search-block { background: rgba(10, 15, 30, 0.6); padding: 20px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 25px; }
        label { display: block; margin-bottom: 8px; color: var(--accent-neon); font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
        select { width: 100%; padding: 14px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.1); background-color: #0d1324; color: #fff; font-size: 15px; margin-bottom: 20px; outline: none; }
        
        /* Checkbox custom design */
        .checkbox-container { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; cursor: pointer; user-select: none; }
        .checkbox-container input { width: 18px; height: 18px; accent-color: var(--accent-neon); cursor: pointer; }
        .checkbox-label { color: #fff; font-size: 14px; font-weight: 500; text-transform: none; letter-spacing: 0; }

        button { width: 100%; padding: 15px; border-radius: 8px; border: none; font-size: 15px; font-weight: 700; background: linear-gradient(45deg, #00ffcc, #00b3ff); color: #090d16; cursor: pointer; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 15px rgba(0, 255, 204, 0.2); }
        button:hover { box-shadow: 0 6px 20px rgba(0, 255, 204, 0.4); }
        .section-header { color: #fff; font-size: 14px; font-weight: 700; text-transform: uppercase; margin-top: 30px; letter-spacing: 1px; display: flex; align-items: center; gap: 8px; }
        .section-header::after { content: ''; flex-grow: 1; height: 1px; background: rgba(255, 255, 255, 0.1); }
        .ticket-card { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 12px; margin-top: 15px; }
        .connect-card { border-left: 4px solid #00b3ff; }
        .top-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .agency { font-size: 16px; font-weight: 600; color: #fff; }
        .badge { font-size: 11px; font-weight: 600; background: rgba(255, 0, 127, 0.15); color: var(--accent-pink); border: 1px solid rgba(255, 0, 127, 0.2); padding: 4px 10px; border-radius: 20px; }
        .timeline-container { background: rgba(0, 0, 0, 0.2); padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 2px solid var(--accent-neon); }
        .node-line { font-size: 13px; color: var(--text-muted); padding: 5px 0; display: flex; justify-content: space-between; }
        .node-line.highlight { color: var(--accent-neon); font-weight: 600; }
        .info-grid { display: flex; justify-content: space-between; font-size: 14px; background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 6px; margin-top: 12px; }
        .dial-btn { display: block; text-align: center; background: rgba(255, 255, 255, 0.05); color: #fff; text-decoration: none; padding: 12px; border-radius: 8px; margin-top: 15px; font-size: 13px; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.1); }
        .dial-btn:hover { border-color: var(--accent-neon); }
        .hub-banner { background: rgba(0, 179, 255, 0.1); color: #00b3ff; border: 1px solid rgba(0, 179, 255, 0.2); padding: 8px; font-size: 13px; font-weight: 600; text-align: center; border-radius: 6px; margin: 15px 0; }
        .no-bus-msg { color: #ff6b6b; font-size: 13px; line-height: 1.5; background: rgba(255, 107, 107, 0.05); padding: 12px; border-radius: 6px; border-left: 2px solid #ff6b6b; }
    </style>
</head>
<body>

<div class="wrapper">
    <h2>Passenger Transit Portal</h2>
    
    <div class="search-block">
        <form method="POST" action="/">
            <label>Boarding Point:</label>
            <select name="source">
                {% for station in all_stations %}
                    <option value="{{ station }}" {% if selected_source == station %}selected{% endif %}>{{ station }}</option>
                {% endfor %}
            </select>

            <label>Destination Point:</label>
            <select name="destination">
                {% for station in all_stations %}
                    <option value="{{ station }}" {% if selected_destination == station %}selected{% endif %}>{{ station }}</option>
                {% endfor %}
            </select>

            <div class="checkbox-container">
                <input type="checkbox" id="allow_connecting" name="allow_connecting" value="yes" {% if allow_connecting == 'yes' %}checked{% endif %}>
                <label for="allow_connecting" class="checkbox-label">Show connecting services if direct routes are unavailable</label>
            </div>

            <button type="submit">Find Routes</button>
        </form>
    </div>

    {% if results is not none %}
        {% if results.direct %}
            <div class="section-header">Direct Options Found</div>
            {% for row in results.direct %}
                <div class="ticket-card">
                    <div class="top-row"><span class="agency">🚍 {{ row['bus_name'] }}</span><span class="badge">{{ row['bus_type'] }}</span></div>
                    <div class="timeline-container">
                        {% for stop in row['stops_timeline'] %}
                            <div class="node-line {% if stop.name == selected_source or stop.name == selected_destination %}highlight{% endif %}">
                                <span>{% if stop.name == selected_source %}🛫 {% elif stop.name == selected_destination %}🛬 {% else %}• {% endif %}{{ stop.name }}</span>
                                <span>{{ stop.time }}</span>
                            </div>
                        {% endfor %}
                    </div>
                    <div class="info-grid"><span>Departure: <b style="color:var(--accent-neon);">{{ row['boarding_time'] }}</b></span><span>Fare: <b style="color:#fff;">₹{{ row['ticket_fare'] }}</b></span></div>
                    <a href="tel:{{ row['contact_number'] }}" class="dial-btn">📞 Connect with Operator</a>
                </div>
            {% endfor %}
        {% elif results.connecting %}
            <div class="section-header">🔄 Recommended Connecting Routes</div>
            {% for route in results.connecting %}
                <div class="ticket-card connect-card">
                    <div style="font-weight:700; font-size:15px; color:#00b3ff; margin-bottom:12px;">Via Transfer Station: {{ route.hub_station }}</div>
                    
                    <div class="top-row"><span class="agency">1️⃣ {{ route.leg1.bus_name }}</span><span class="badge">{{ route.leg1.bus_type }}</span></div>
                    <div class="node-line" style="padding:0 5px;"><span>Depart {{ selected_source }}:</span><b>{{ route.leg1.boarding_time }}</b></div>
                    <div class="node-line" style="padding:0 5px; margin-bottom:10px;"><span>Arrive {{ route.hub_station }}:</span><b>{{ route.leg1.hub_arrival_time }}</b></div>
                    
                    {% if route.has_second_bus %}
                        <div class="hub-banner">⏳ Transfer Window: {{ route.hub_station }} Interchange ({{ route.layover_mins }} Mins)</div>
                        <div class="top-row"><span class="agency">2️⃣ {{ route.leg2.bus_name }}</span><span class="badge">{{ route.leg2.bus_type }}</span></div>
                        <div class="node-line" style="padding:0 5px;"><span>Depart {{ route.hub_station }}:</span><b>{{ route.leg2.hub_departure_time }}</b></div>
                        <div class="node-line" style="padding:0 5px;"><span>Arrive {{ selected_destination }}:</span><b>{{ route.leg2.final_arrival_time }}</b></div>
                        <div class="info-grid" style="border-top:1px dashed rgba(255,255,255,0.1); margin-top:10px;">
                            <span>Combined Route Distance Fare:</span><b style="color:var(--accent-neon);">₹{{ route.total_fare }}</b>
                        </div>
                    {% else %}
                        <div class="hub-banner" style="background: rgba(255, 107, 107, 0.1); color: #ff6b6b; border-color: rgba(255, 107, 107, 0.2);">⚠️ Direct connecting timetable gap inside this shift window</div>
                        <div class="no-bus-msg">Take Bus 1 straight to <b>{{ route.hub_station }}</b>. Multiple local options or alternate local carriers travel frequently from there toward {{ selected_destination }}.</div>
                        <div class="info-grid"><span>Leg 1 Fare:</span><b style="color:var(--accent-neon);">₹{{ route.total_fare }}</b></div>
                    {% endif %}
                    <a href="tel:{{ route.leg1.contact_number }}" class="dial-btn">📞 Contact First Leg Operator</a>
                </div>
            {% endfor %}
        {% else %}
            <p style="text-align:center; color:var(--text-muted); padding:30px 0; font-style:italic;">No direct operational transit linkages found mapping these search parameters.</p>
        {% endif %}
    {% endif %}
</div>

</body>
</html>
"""

def compute_dynamic_arrival(base_time_str, minutes_to_add):
    base_time = datetime.strptime(base_time_str, "%I:%M %p")
    arrival_time = base_time + timedelta(minutes=minutes_to_add)
    return arrival_time.strftime("%I:%M %p")

def time_difference_minutes(time_str1, time_str2):
    t1 = datetime.strptime(time_str1, "%I:%M %p")
    t2 = datetime.strptime(time_str2, "%I:%M %p")
    if t2 < t1:
        t2 += timedelta(days=1)
    return int((t2 - t1).total_seconds() / 60)

def fetch_bus_leg_data(cursor, source, destination):
    query = """
        SELECT s.id as sched_id, b.bus_name, b.contact_number, b.bus_type, s.base_departure_time, s.per_km_rate, s.route_id,
               rs1.stop_order as src_order, rs1.distance_offset as src_dist, rs1.minutes_offset as src_mins,
               rs2.stop_order as dest_order, rs2.distance_offset as dest_dist, rs2.minutes_offset as dest_mins
        FROM schedules s
        JOIN buses b ON s.bus_id = b.id
        JOIN route_stops rs1 ON s.route_id = rs1.route_id AND rs1.station_name = ?
        JOIN route_stops rs2 ON s.route_id = rs2.route_id AND rs2.station_name = ?
        WHERE rs1.stop_order < rs2.stop_order
    """
    cursor.execute(query, (source, destination))
    return cursor.fetchall()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT station_name FROM route_stops ORDER BY station_name ASC")
    all_stations = [row['station_name'] for row in cursor.fetchall()]

    final_output = {"direct": [], "connecting": []}
    selected_source = None
    selected_destination = None
    allow_connecting = None

    if request.method == 'POST':
        selected_source = request.form.get('source')
        selected_destination = request.form.get('destination')
        allow_connecting = request.form.get('allow_connecting') # Reads the checkbox state ('yes' or None)

        if selected_source != selected_destination:
            # 1. Look for direct runs
            direct_matches = fetch_bus_leg_data(cursor, selected_source, selected_destination)
            
            for sched in direct_matches:
                dist = abs(sched['dest_dist'] - sched['src_dist'])
                fare = int(round(dist * sched['per_km_rate']))
                boarding_time = compute_dynamic_arrival(sched['base_departure_time'], sched['src_mins'])
                
                cursor.execute("SELECT station_name, distance_offset, minutes_offset FROM route_stops WHERE route_id = ? ORDER BY stop_order ASC", (sched['route_id'],))
                stops = cursor.fetchall()
                timeline = [{'name': s['station_name'], 'dist': s['distance_offset'], 'time': compute_dynamic_arrival(sched['base_departure_time'], s['minutes_offset'])} for s in stops]

                final_output["direct"].append({
                    'bus_name': sched['bus_name'], 'contact_number': sched['contact_number'], 'bus_type': sched['bus_type'],
                    'boarding_time': boarding_time, 'ticket_fare': fare, 'stops_timeline': timeline
                })

            # 2. Look for connecting alternatives ONLY if direct fails AND user selected the checkbox
            if not final_output["direct"] and allow_connecting == 'yes':
                cursor.execute("""
                    SELECT DISTINCT r1.station_name as hub 
                    FROM route_stops r1 
                    JOIN route_stops r2 ON r1.route_id = r2.route_id 
                    WHERE r2.station_name = ?
                """, (selected_destination,))
                destination_hubs = [r['hub'] for r in cursor.fetchall() if r['hub'] != selected_destination]

                for hub in destination_hubs:
                    legs1 = fetch_bus_leg_data(cursor, selected_source, hub)
                    if not legs1:
                        continue
                        
                    legs2 = fetch_bus_leg_data(cursor, hub, selected_destination)

                    for l1 in legs1:
                        d1 = abs(l1['dest_dist'] - l1['src_dist'])
                        f1 = int(round(d1 * l1['per_km_rate']))
                        l1_arr = compute_dynamic_arrival(l1['base_departure_time'], l1['dest_mins'])
                        
                        bus2_matched = False
                        
                        for l2 in legs2:
                            l2_dep = compute_dynamic_arrival(l2['base_departure_time'], l2['src_mins'])
                            layover = time_difference_minutes(l1_arr, l2_dep)
                            
                            if 10 <= layover <= 720:  
                                d2 = abs(l2['dest_dist'] - l2['src_dist'])
                                f2 = int(round(d2 * l2['per_km_rate']))
                                
                                final_output["connecting"].append({
                                    "hub_station": hub,
                                    "layover_mins": layover,
                                    "total_fare": f1 + f2,
                                    "has_second_bus": True,
                                    "leg1": {
                                        "bus_name": l1['bus_name'], "bus_type": l1['bus_type'], "contact_number": l1['contact_number'],
                                        "boarding_time": compute_dynamic_arrival(l1['base_departure_time'], l1['src_mins']), "hub_arrival_time": l1_arr
                                    },
                                    "leg2": {
                                        "bus_name": l2['bus_name'], "bus_type": l2['bus_type'],
                                        "hub_departure_time": l2_dep, "final_arrival_time": compute_dynamic_arrival(l2['base_departure_time'], l2['dest_mins'])
                                    }
                                })
                                bus2_matched = True
                                break
                        
                        if not bus2_matched:
                            final_output["connecting"].append({
                                "hub_station": hub,
                                "layover_mins": 0,
                                "total_fare": f1,
                                "has_second_bus": False,
                                "leg1": {
                                    "bus_name": l1['bus_name'], "bus_type": l1['bus_type'], "contact_number": l1['contact_number'],
                                    "boarding_time": compute_dynamic_arrival(l1['base_departure_time'], l1['src_mins']), "hub_arrival_time": l1_arr
                                },
                                "leg2": {}
                            })
                
                final_output["connecting"].sort(key=lambda x: (not x['has_second_bus'], x['layover_mins']))

    conn.close()
    return render_template_string(
        HTML_TEMPLATE, all_stations=all_stations, 
        results=final_output if request.method == 'POST' else None,
        selected_source=selected_source, selected_destination=selected_destination,
        allow_connecting=allow_connecting
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

