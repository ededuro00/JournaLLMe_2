"""
Database migration script to add gender, age, and profile_completed fields.
This script updates the existing database to support the new user profile feature.
"""

import sqlite3
import os

# Path to the database
db_path = os.path.join('instance', 'questionnaire.db')

def migrate_database():
    """Add new columns to users table for existing database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add gender column if it doesn't exist
        if 'gender' not in columns:
            print("Adding 'gender' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN gender VARCHAR(50)")
            print("✓ Added 'gender' column")
        else:
            print("'gender' column already exists")
        
        # Add age column if it doesn't exist
        if 'age' not in columns:
            print("Adding 'age' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
            print("✓ Added 'age' column")
        else:
            print("'age' column already exists")
        
        # Add profile_completed column if it doesn't exist
        if 'profile_completed' not in columns:
            print("Adding 'profile_completed' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN profile_completed BOOLEAN DEFAULT 0 NOT NULL")
            print("✓ Added 'profile_completed' column")
            
            # Set profile_completed to False (0) for all existing users
            cursor.execute("UPDATE users SET profile_completed = 0 WHERE profile_completed IS NULL")
            print("✓ Set profile_completed = False for all existing users")
        else:
            print("'profile_completed' column already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting database migration...")
    print(f"Database path: {db_path}\n")
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("Please run the application first to create the database.")
    else:
        migrate_database()
