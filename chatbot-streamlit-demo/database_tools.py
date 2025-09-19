# database_tools.py
import sqlite3
import os
from typing import List, Dict, Any, Optional

# Database file path
DB_PATH = "sales_data.db"

def init_database():
    """
    Initialize the database with sample tables if they don't exist
    """
    # Create the database file if it doesn't exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        address TEXT
    )
    """)
    
    # Create products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 0
    )
    """)
    
    # Create sales table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        sale_date TEXT NOT NULL,
        total_amount REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
    """)
    
    # Create sale_items table (for items in each sale)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        item_id INTEGER PRIMARY KEY,
        sale_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        price_per_unit REAL NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales (sale_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    """)
    
    # Insert sample data only if tables are empty
    if cursor.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
        # Insert sample customers
        cursor.executemany(
            "INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)",
            [
                ("John Doe", "john@example.com", "555-1234", "123 Main St"),
                ("Jane Smith", "jane@example.com", "555-5678", "456 Oak Ave"),
                ("Bob Johnson", "bob@example.com", "555-9012", "789 Pine Rd"),
                ("Alice Brown", "alice@example.com", "555-3456", "321 Elm St"),
                ("Charlie Davis", "charlie@example.com", "555-7890", "654 Maple Dr")
            ]
        )
        
        # Insert sample products
        cursor.executemany(
            "INSERT INTO products (name, description, price, stock_quantity) VALUES (?, ?, ?, ?)",
            [
                ("Laptop", "High-performance laptop", 1200.00, 10),
                ("Smartphone", "Latest model smartphone", 800.00, 15),
                ("Tablet", "10-inch tablet", 300.00, 20),
                ("Headphones", "Noise-cancelling headphones", 150.00, 30),
                ("Monitor", "27-inch 4K monitor", 350.00, 8)
            ]
        )
        
        # Insert sample sales
        cursor.executemany(
            "INSERT INTO sales (customer_id, sale_date, total_amount) VALUES (?, ?, ?)",
            [
                (1, "2023-01-15", 1200.00),
                (2, "2023-01-20", 950.00),
                (3, "2023-02-05", 300.00),
                (4, "2023-02-10", 500.00),
                (5, "2023-03-01", 1550.00),
                (1, "2023-03-15", 150.00),
                (2, "2023-04-02", 350.00)
            ]
        )
        
        # Insert sample sale items
        cursor.executemany(
            "INSERT INTO sale_items (sale_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)",
            [
                (1, 1, 1, 1200.00),  # John bought a laptop
                (2, 2, 1, 800.00),    # Jane bought a smartphone
                (2, 4, 1, 150.00),    # Jane also bought headphones
                (3, 3, 1, 300.00),    # Bob bought a tablet
                (4, 4, 2, 150.00),    # Alice bought two headphones
                (4, 3, 1, 200.00),    # Alice bought a discounted tablet
                (5, 1, 1, 1200.00),   # Charlie bought a laptop
                (5, 4, 1, 150.00),    # Charlie also bought headphones
                (5, 5, 1, 200.00),    # Charlie also bought a discounted monitor
                (6, 4, 1, 150.00),    # John bought headphones
                (7, 5, 1, 350.00)     # Jane bought a monitor
            ]
        )
    
    conn.commit()
    conn.close()
    
    return "Database initialized with sample data."

def execute_sql_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute an SQL query and return the results as a list of dictionaries
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        # Set row_factory to sqlite3.Row to access columns by name
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query)
        
        # Check if this is a SELECT query
        if query.strip().upper().startswith("SELECT"):
            # Fetch all rows and convert to list of dictionaries
            rows = cursor.fetchall()
            result = [{k: row[k] for k in row.keys()} for row in rows]
        else:
            # For non-SELECT queries, return affected row count
            result = [{"affected_rows": cursor.rowcount}]
            conn.commit()
            
        conn.close()
        return result
    
    except sqlite3.Error as e:
        return [{"error": str(e)}]

def get_table_schema() -> Dict[str, List[Dict[str, str]]]:
    """
    Get the schema of all tables in the database
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        schema = {}
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            schema[table_name] = [
                {
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "pk": bool(col[5])
                }
                for col in columns
            ]
        
        conn.close()
        return schema
    
    except sqlite3.Error as e:
        return {"error": str(e)}

# Function to be used as a tool in the LangGraph agent
def text_to_sql(sql_query: str) -> Dict[str, Any]:
    """
    Execute a SQL query against the database
    
    Args:
        sql_query: The SQL query to execute
        
    Returns:
        Dictionary with SQL query and results
    """
    # Make sure the database exists
    if not os.path.exists(DB_PATH):
        init_database()
    
    # Execute the SQL query
    try:
        results = execute_sql_query(sql_query)
        return {
            "query": sql_query,
            "results": results
        }
    except Exception as e:
        return {
            "query": sql_query,
            "results": [{"error": str(e)}]
        }

def get_database_info() -> Dict[str, Any]:
    """
    Get information about the database schema to help with query construction
    
    Returns:
        Dictionary with database schema and sample data
    """
    # Make sure the database exists
    if not os.path.exists(DB_PATH):
        init_database()
    
    # Get the database schema
    schema = get_table_schema()
    
    # Get sample data for each table (first 3 rows)
    sample_data = {}
    for table_name in schema.keys():
        if isinstance(table_name, str):  # Skip any error entries
            try:
                sample_data[table_name] = execute_sql_query(f"SELECT * FROM {table_name} LIMIT 3")
            except:
                pass
    
    return {
        "schema": schema,
        "sample_data": sample_data
    }

# Script to create the database when run directly
if __name__ == "__main__":
    print(init_database())
    print("Database created with sample data.")