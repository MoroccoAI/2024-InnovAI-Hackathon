import sqlite3
import pandas as pd
import os
import glob
import re
from typing import Dict, List, Tuple

def sanitize_table_name(name: str) -> str:
    """Convert a filename to a valid SQLite table name."""
    # Remove any non-alphanumeric characters and convert to lowercase
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
    # Ensure it doesn't start with a number
    if clean_name[0].isdigit():
        clean_name = 'tbl_' + clean_name
    return clean_name

def infer_sql_types(df: pd.DataFrame) -> Dict[str, str]:
    """Infer SQL column types from DataFrame dtypes."""
    type_mapping = {
        'int64': 'INTEGER',
        'float64': 'REAL',
        'bool': 'INTEGER',
        'datetime64[ns]': 'TIMESTAMP',
        'object': 'TEXT'
    }
    
    column_types = {}
    for column in df.columns:
        dtype = str(df[column].dtype)
        sql_type = type_mapping.get(dtype, 'TEXT')
        column_types[column] = sql_type
    
    return column_types

def create_database():
    """Create SQLite database and import all CSV files from the Data directory."""
    # Create a connection to the database
    db_dir = 'SIIR.AI_chatbot'
    db_path = os.path.join(db_dir, 'afcon2025.db')
    
    # Ensure the database directory exists
    os.makedirs(db_dir, exist_ok=True)
    
    # Remove existing database to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create new database connection
    conn = sqlite3.connect(db_path)
    print(f"Created new database: {db_path}")
    
    # Get all CSV files from the Data directory
    csv_files = glob.glob('SIIR.AI_chatbot/Data/*.csv')
    total_files = len(csv_files)
    
    if total_files == 0:
        print("No CSV files found in the Data directory!")
        conn.close()
        return
    
    print(f"Found {total_files} CSV files to process")
    
    # Track successfully created tables
    created_tables: List[Tuple[str, List[str]]] = []
    
    for index, csv_file in enumerate(csv_files, 1):
        try:
            print(f"\nProcessing file {index}/{total_files}: {csv_file}")
            
            # Read CSV file with automatic type inference
            df = pd.read_csv(csv_file)
            
            # Get and sanitize table name from file name
            base_name = os.path.splitext(os.path.basename(csv_file))[0]
            table_name = sanitize_table_name(base_name)
            
            # Infer SQL types
            column_types = infer_sql_types(df)
            
            # Create table with inferred schema
            df.to_sql(table_name, conn, index=False, dtype=column_types)
            
            # Get actual schema from the created table
            cursor = conn.execute(f"SELECT * FROM {table_name} LIMIT 0")
            columns = [f"{desc[0]} ({desc[1]})" for desc in cursor.description]
            
            created_tables.append((table_name, columns))
            print(f"✓ Successfully created table: {table_name}")
            print(f"  Rows: {len(df)}")
            print("  Schema:")
            for col in columns:
                print(f"    - {col}")
            
        except Exception as e:
            print(f"✗ Error processing {csv_file}:")
            print(f"  {str(e)}")
    
    # Print summary
    print("\nDatabase Creation Summary:")
    print("-" * 50)
    if created_tables:
        print(f"Successfully created {len(created_tables)} tables:")
        for table_name, columns in created_tables:
            print(f"\n{table_name}:")
            for column in columns:
                print(f"  - {column}")
    else:
        print("No tables were created!")
    
    conn.close()
    print("\nDatabase creation completed!")

if __name__ == "__main__":
    create_database()
