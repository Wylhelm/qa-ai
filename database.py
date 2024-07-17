import sqlite3
import json
from test_scenario import TestScenario

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('scenarios.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scenarios
            (id INTEGER PRIMARY KEY, name TEXT, criteria TEXT, scenario TEXT, processed_files TEXT, ui_elements TEXT, timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')))
        ''')
        self.conn.commit()

    def save_scenario(self, test_scenario):
        cursor = self.conn.cursor()
        processed_files_json = json.dumps([{k: v for k, v in file.items() if k != 'image_data'} for file in test_scenario.processed_files])
        cursor.execute('INSERT INTO scenarios (name, criteria, scenario, processed_files, ui_elements) VALUES (?, ?, ?, ?, ?)', 
                       (test_scenario.name, test_scenario.criteria, test_scenario.scenario_text, processed_files_json, json.dumps(test_scenario.ui_elements)))
        self.conn.commit()

    def get_scenarios(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, timestamp FROM scenarios ORDER BY timestamp DESC')
        return cursor.fetchall()

    def clear_history(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM scenarios')
        self.conn.commit()
        cursor.execute('VACUUM')  # This will reclaim the freed space
    def get_scenario_by_criteria(self, criteria):
        scenarios = self.get_scenarios()
        return next((s for s in scenarios if s.criteria == criteria), None)
