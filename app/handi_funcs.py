import os
import string
import random
import time
import psycopg
from db import get_connection

class handi_funcs:
    def generate_unique_rid(self, cursor):
        while True:
            rid = random.randint(10000, 99999)
            cursor.execute("SELECT rid FROM rounds WHERE rid = %s", (uid,))
            if not cursor.fetchone():
                return rid

    def add_round(self, username, score):
        try:
            conn = get_connection
            cur = conn.cursor()
            rid = self.generate_unique_rid()
            cur.execute("INSERT INTO rounds (rid, username, score) VALUES (%s, %s, %s)", (rid, username, score))
            conn.commit()
            print(f"Round added with rid: {rid}, username: {username}, score: {score}")
            conn.close()
            return rid
        except Exception as e:
            print(f"Error adding round: {e}")
            if conn:
                conn.rollback()
            return None
        

    def get_rounds(self, username):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT rid, score FROM rounds WHERE username = %s", (username,))
            rounds = cur.fetchall()
            conn.close()
            return rounds
        except Exception as e:
            print(f"Error fetching rounds: {e}")
            return None
    
    def delete_round(self, rid):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM rounds WHERE rid = %s", (rid,))
            conn.commit()
            print(f"Round with rid {rid} deleted successfully.")
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting round: {e}")
            if conn:
                conn.rollback()
            return False

    def calc_handicap(self, username):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT score FROM rounds WHERE username = %s", (username,))
            scores = cur.fetchall()
            if not scores:
                print(f"No rounds found for user {username}.")
                return None
            if len(scores) < 20:
                print(f"Only {len(scores)} scores found for user {username}. Handicap calculation requires at least 20 rounds.")
                return None
            
            total_score = sum(score[0] for score in scores)
            num_rounds = len(scores)
            handicap = total_score / num_rounds
            print(f"Calculated handicap for {username}: {handicap}")
            conn.close()
            return handicap
        except Exception as e:
            print(f"Error calculating handicap: {e}")
            return None