import pymysql
from dotenv import load_dotenv
import os

class DatabaseManager:
    def __init__(self):
        self.conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
        self.cursor = self.conn.cursor()

    def fetch_all(self):
        self.cursor.execute("""
            SELECT s.matricule, s.nom, s.prenom, s.adresse, s.tel, s.datenaissance,
                   c.name, m.name
            FROM stagiaire s
            JOIN classes c ON s.class_id = c.id
            JOIN majors m ON c.major_id = m.id
        """)
        return self.cursor.fetchall()

    def fetch_majors(self):
        self.cursor.execute("SELECT id, name FROM majors")
        return self.cursor.fetchall()

    def fetch_classes_by_major(self, major_id):
        self.cursor.execute("SELECT id, name FROM classes WHERE major_id=%s", (major_id,))
        return self.cursor.fetchall()

    def fetch_by_class(self, class_id):
        self.cursor.execute("""
            SELECT s.matricule, s.nom, s.prenom, s.adresse, s.tel, s.datenaissance,
                   c.name, m.name
            FROM stagiaire s
            JOIN classes c ON s.class_id = c.id
            JOIN majors m ON c.major_id = m.id
            WHERE c.id=%s
        """, (class_id,))
        return self.cursor.fetchall()

    def insert(self, s):
        self.cursor.execute("""
            INSERT INTO stagiaire VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (s["matricule"], s["nom"], s["prenom"], s["adresse"], s["tel"], s["datenaissance"], s["class_id"]))
        self.conn.commit()

    def update(self, s):
        self.cursor.execute("""
            UPDATE stagiaire
            SET nom=%s, prenom=%s, adresse=%s, tel=%s, datenaissance=%s, class_id=%s
            WHERE matricule=%s
        """, (s["nom"], s["prenom"], s["adresse"], s["tel"], s["datenaissance"], s["class_id"], s["matricule"]))
        self.conn.commit()

    def delete_many(self, matricules):
        for m in matricules:
            self.cursor.execute("DELETE FROM stagiaire WHERE matricule=%s", (m,))
        self.conn.commit()

    def search_by_matricule(self, mat):
        self.cursor.execute("""
            SELECT s.matricule, s.nom, s.prenom, s.adresse, s.tel, s.datenaissance,
                   c.name, m.name
            FROM stagiaire s
            JOIN classes c ON s.class_id = c.id
            JOIN majors m ON c.major_id = m.id
            WHERE s.matricule=%s
        """, (mat,))
        return self.cursor.fetchone()

    def sort_by_name(self):
        self.cursor.execute("""
            SELECT s.matricule, s.nom, s.prenom, s.adresse, s.tel, s.datenaissance,
                   c.name, m.name
            FROM stagiaire s
            JOIN classes c ON s.class_id = c.id
            JOIN majors m ON c.major_id = m.id
            ORDER BY s.nom
        """)
        return self.cursor.fetchall()

    def update_class_for_many(self, matricules, class_id):
        for m in matricules:
            self.cursor.execute(
                "UPDATE stagiaire SET class_id=%s WHERE matricule=%s",
                (class_id, m)
            )
        self.conn.commit()
