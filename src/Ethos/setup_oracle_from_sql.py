# setup_oracle_from_sql.py
# (venv) C:\big20\final\src\Ethos> pip install oracledb python-dotenv
import os
import oracledb
from dotenv import load_dotenv

# Load environment variables
load_dotenv(r'c:\big20\final\.env')

def get_connection():
    try:
        host = os.getenv('ORACLE_HOST')
        port = os.getenv('ORACLE_PORT')
        service = os.getenv('ORACLE_SERVICE_NAME')
        user = os.getenv('ORACLE_USER')
        
        print(f"Connecting to Oracle at {host}:{port}/{service} as {user}...")
        
        dsn = f"{host}:{port}/{service}"
        conn = oracledb.connect(
            user=user,
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=dsn
        )
        print("Connected to Oracle DB successfully.")
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def execute_sql_file(cursor, file_path, log_func):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        buffer = []
        in_plsql = False
        
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("--"):
                continue
                
            # Check for PL/SQL Block Start
            if not buffer and (stripped.upper().startswith("BEGIN") or stripped.upper().startswith("DECLARE")):
                in_plsql = True
                
            if stripped == '/':
                # Execute Buffer (PL/SQL or previous statement ending in /)
                if buffer:
                    sql = "\n".join(buffer)
                    try:
                        cursor.execute(sql)
                        log_func(f"Executed Block: {sql[:30]}...")
                    except oracledb.DatabaseError as e:
                        log_func(f"Error executing block: {e}")
                    buffer = []
                    in_plsql = False
                continue

            # Add line to buffer
            buffer.append(line.rstrip())
            
            # Check for generic SQL terminator ';'
            if not in_plsql and stripped.endswith(';'):
                # Remove trailing semicolon for ORA-00911: invalid character
                # (Oracle DB API usually doesn't want the semicolon for simple statements)
                
                # Reconstruct SQL from buffer
                sql = "\n".join(buffer).strip()
                if sql.endswith(';'):
                    sql = sql[:-1] # Remove last char
                
                try:
                    cursor.execute(sql)
                    log_func(f"Executed: {sql[:50]}...")
                except oracledb.DatabaseError as e:
                    # Ignore comment errors or harmless ones if needed
                    error, = e.args
                    log_func(f"Error executing SQL: {e}")
                
                buffer = []
        
        # Process remaining buffer if any (e.g. no semicolon at very end)
        if buffer and not in_plsql:
             sql = "\n".join(buffer).strip()
             if sql:
                 if sql.endswith(';'): sql = sql[:-1]
                 try:
                    cursor.execute(sql)
                    log_func(f"Executed: {sql[:50]}...")
                 except Exception as e:
                    log_func(f"Error executing remaining SQL: {e}")

    except Exception as e:
         log_func(f"Error reading SQL file: {e}")

def setup_db():
    log_path = r'c:\big20\final\setup_log.txt'
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("Starting setup from SQL file...\n")
        
    def log(msg):
        print(msg)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(msg + "\n")
            
    conn = get_connection()
    if not conn:
        log("Connection failed.")
        return

    cursor = conn.cursor()

    log("\n--- Executing oracle_schema.sql ---")
    execute_sql_file(cursor, r'c:\big20\final\docs\oracle_schema.sql', log)

    conn.commit()
    log("SUCCESS: SQL script executed completely.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_db()
