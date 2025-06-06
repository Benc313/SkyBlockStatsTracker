# app.py

import sqlite3
from flask import Flask, jsonify, request
from datetime import datetime, timedelta, time
import subprocess
import sys
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_FILE = 'skyblock_stats.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/trigger_collect', methods=['POST'])
def trigger_collect():
    try:
        subprocess.Popen([sys.executable, 'hypixel_tracker.py'])
        return jsonify({"message": "Data collection started."}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/latest_snapshot_timestamp')
def get_latest_snapshot_timestamp():
    conn = get_db_connection()
    snap = conn.execute('SELECT snapshot_timestamp FROM profile_snapshots ORDER BY snapshot_timestamp DESC LIMIT 1').fetchone()
    conn.close()
    return jsonify({"latest_timestamp": snap['snapshot_timestamp'] if snap else None})

@app.route('/api/profile_stats/<int:timestamp>')
def get_profile_stats(timestamp):
    conn = get_db_connection()
    stats = conn.execute('SELECT purse, death_count, kills, bank_balance FROM profile_snapshots WHERE snapshot_timestamp = ?', (timestamp,)).fetchone()
    conn.close()
    if stats:
        return jsonify(dict(stats))
    return jsonify({"error": "Stats not found"}), 404

def get_start_timestamp(time_range='7d'):
    now = datetime.now()
    if time_range == 'today':
        start_date = datetime.combine(now.date(), time.min)
    elif time_range == '7d':
        start_date = now - timedelta(days=7)
    elif time_range == '30d':
        start_date = now - timedelta(days=30)
    elif time_range == 'all':
        return 0
    else: 
        return 0
    return int(start_date.timestamp())

@app.route('/api/history/skills')
def get_skill_history():
    time_range = request.args.get('range', '7d')
    start_timestamp = get_start_timestamp(time_range)
    conn = get_db_connection()
    rows = conn.execute('SELECT skill_name, total_xp, snapshot_timestamp FROM skill_snapshots WHERE snapshot_timestamp >= ? ORDER BY snapshot_timestamp ASC', (start_timestamp,)).fetchall()
    conn.close()
    history_data = {}
    for row in rows:
        key = row['skill_name']
        if key not in history_data: history_data[key] = []
        history_data[key].append({"timestamp": row['snapshot_timestamp'], "value": row['total_xp']})
    return jsonify(history_data)

@app.route('/api/history/profile_stats')
def get_profile_stats_history():
    time_range = request.args.get('range', '7d')
    start_timestamp = get_start_timestamp(time_range)
    conn = get_db_connection()
    rows = conn.execute('SELECT purse, kills, death_count, bank_balance, snapshot_timestamp FROM profile_snapshots WHERE snapshot_timestamp >= ? ORDER BY snapshot_timestamp ASC', (start_timestamp,)).fetchall()
    conn.close()
    
    history_data = {'total_money': [], 'kills': [], 'deaths': []}
    for row in rows:
        total_money = (row['purse'] or 0) + (row['bank_balance'] or 0)
        history_data['total_money'].append({'timestamp': row['snapshot_timestamp'], 'value': total_money})
        history_data['kills'].append({'timestamp': row['snapshot_timestamp'], 'value': row['kills']})
        history_data['deaths'].append({'timestamp': row['snapshot_timestamp'], 'value': row['death_count']})
        
    return jsonify(history_data)

@app.route('/api/history/collections')
def get_collection_history():
    time_range = request.args.get('range', '7d')
    start_timestamp = get_start_timestamp(time_range)
    conn = get_db_connection()
    rows = conn.execute('SELECT collection_name, amount, snapshot_timestamp FROM collection_snapshots WHERE snapshot_timestamp >= ? ORDER BY snapshot_timestamp ASC', (start_timestamp,)).fetchall()
    conn.close()
    history_data = {}
    for row in rows:
        key = row['collection_name']
        if key not in history_data: history_data[key] = []
        history_data[key].append({"timestamp": row['snapshot_timestamp'], "value": row['amount']})
    return jsonify(history_data)

@app.route('/api/history/bestiary')
def get_bestiary_history():
    time_range = request.args.get('range', '7d')
    start_timestamp = get_start_timestamp(time_range)
    conn = get_db_connection()
    rows = conn.execute(
        'SELECT mob_id, kills, snapshot_timestamp FROM bestiary_snapshots WHERE snapshot_timestamp >= ? ORDER BY snapshot_timestamp ASC',
        (start_timestamp,)
    ).fetchall()
    conn.close()

    history_data = {}
    for row in rows:
        key = row['mob_id']
        if key not in history_data:
            history_data[key] = []
        history_data[key].append({"timestamp": row['snapshot_timestamp'], "value": row['kills']})
            
    return jsonify(history_data)

def get_progress_data(table_name, id_col, val_col, time_range):
    start_boundary_ts = get_start_timestamp(time_range)
    conn = get_db_connection()
    latest_snapshot_query = conn.execute(f'SELECT MAX(snapshot_timestamp) as end_ts FROM {table_name}').fetchone()
    end_ts = latest_snapshot_query['end_ts'] if latest_snapshot_query and latest_snapshot_query['end_ts'] is not None else None
    
    previous_snapshot_query = conn.execute(
        f'SELECT MAX(snapshot_timestamp) as start_ts FROM {table_name} WHERE snapshot_timestamp < ?',
        (start_boundary_ts,)
    ).fetchone()
    start_ts = previous_snapshot_query['start_ts'] if previous_snapshot_query and previous_snapshot_query['start_ts'] is not None else None

    if not start_ts or not end_ts or start_ts == end_ts:
        conn.close()
        return []

    start_data_rows = conn.execute(f'SELECT {id_col}, {val_col} FROM {table_name} WHERE snapshot_timestamp = ?', (start_ts,)).fetchall()
    end_data_rows = conn.execute(f'SELECT {id_col}, {val_col} FROM {table_name} WHERE snapshot_timestamp = ?', (end_ts,)).fetchall()
    conn.close()
    
    start_map = {row[id_col]: row[val_col] for row in start_data_rows}
    end_map = {row[id_col]: row[val_col] for row in end_data_rows}
    
    progress_list = []
    for item_id, end_value in end_map.items():
        try:
            start_value = int(start_map.get(item_id, 0) or 0)
            current_end_value = int(end_value or 0)
        except (ValueError, TypeError): continue
        
        progress = current_end_value - start_value
        if progress > 0:
            progress_list.append({"name": item_id, "progress": progress, "end_value": current_end_value})
            
    progress_list.sort(key=lambda x: x['progress'], reverse=True)
    return progress_list

@app.route('/api/diff/collections')
def get_collection_progress():
    time_range = request.args.get('range', 'today')
    return jsonify(get_progress_data('collection_snapshots', 'collection_name', 'amount', time_range))

@app.route('/api/diff/bestiary')
def get_bestiary_progress():
    time_range = request.args.get('range', 'today')
    return jsonify(get_progress_data('bestiary_snapshots', 'mob_id', 'kills', time_range))

if __name__ == '__main__':
    app.run(debug=True, port=5000)