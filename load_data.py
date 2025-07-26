# load_data.py
import pandas as pd
from .database import SessionLocal, engine
from . import models
import os
from pathlib import Path

# Define the order of loading to respect foreign key constraints
CSV_FILES_ORDER = {
    'distribution_centers': models.DistributionCenter,
    'products': models.Product,
    'users': models.User,
    'orders': models.Order,
    'inventory_items': models.InventoryItem,
    'order_items': models.OrderItem,
}

# Get the path to the directory where this script is located
SCRIPT_DIR = Path(__file__).resolve().parent
# Set the data directory relative to the script's location
DATA_DIR = SCRIPT_DIR / "data"

def clean_and_load_data():
    # Create all tables in the database
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("Tables created.")

    db = SessionLocal()
    valid_user_ids = set()
    try:
        for filename, model in CSV_FILES_ORDER.items():
            # Check if table is already populated
            if db.query(model).count() > 0:
                print(f"Table '{model.__tablename__}' is not empty. Skipping.")
                continue

            csv_path = os.path.join(DATA_DIR, f"{filename}.csv")
            print(f"Loading data from '{csv_path}' into '{model.__tablename__}'...")
            
            # Use pandas to read CSV
            df = pd.read_csv(csv_path)
            df = df.where(pd.notna(df), None)

            # --- ADD THIS BLOCK TO HANDLE DUPLICATE USERS ---
           

            # if filename == 'users':
            #     print("Dropping duplicate users based on email...")
            #     df.drop_duplicates(subset=['email'], keep='first', inplace=True)
            #     # Store the IDs of the users we are keeping
            #     # valid_user_ids = set(df['id'].unique())

            # # --- STEP 3: ADD THIS ENTIRE BLOCK ---
            # elif filename == 'orders':
            #     print("Filtering orders to ensure they belong to valid users...")
            #     df = df[df['user_id'].isin(valid_user_ids)]
            
            records = df.to_dict(orient='records')
            # For tables with datetime, convert strings to datetime objects
            for record in records:
                for key, value in record.items():
                    if 'at' in key and isinstance(value, str): # Simple check for datetime columns
                        record[key] = pd.to_datetime(value, errors='coerce').to_pydatetime() if pd.notna(value) else None

            db.bulk_insert_mappings(model, records)
            db.commit()
            print(f"Successfully loaded {len(records)} records into '{model.__tablename__}'.")

    except FileNotFoundError as e:
        print(f"ERROR: File not found. Make sure '{e.filename}' exists in the '{DATA_DIR}' directory.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_and_load_data()