import psycopg2

# Database connection parameters
dbname = "mktg"
user = "root"
password = "password"
host = "localhost"
port = "10625"

# Function to establish a database connection
def connect():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return conn

# Function to create a new record in the table
def select_record(conn, version_num):
    cursor = conn.cursor()
    cursor.execute("SELECT * from alembic_version WHERE version_num = %s", (version_num,))
    records = cursor.fetchall()
    cursor.close()
    return records

# Function to create a new record in the table
def create_record(conn, version_num):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO alembic_version (version_num) VALUES (%s)", (version_num,))
    conn.commit()
    cursor.close()

# Function to update an existing record in the table
def update_record(conn, version_num, new_version_num):
    cursor = conn.cursor()
    cursor.execute("UPDATE alembic_version SET version_num = %s WHERE version_num = %s", (new_version_num, version_num))
    conn.commit()
    cursor.close()

# Function to delete a record from the table
def delete_record(conn, version_num):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alembic_version WHERE version_num = %s", (version_num,))
    conn.commit()
    cursor.close()

# Main function to demonstrate database operations
def main():
    conn = connect()

    alembic_version = 'jhgdjo34khdkhj'
    new_alembic_version = 'djh6wo34kjh6s9'

    # # Create a new record
    create_record(conn, alembic_version)

    records = select_record(conn, alembic_version)

    # Update the record with id=1
    update_record(conn, alembic_version, new_alembic_version)

    # Delete the record with id=2
    delete_record(conn, new_alembic_version)

    conn.close()

if __name__ == "__main__":
    main()