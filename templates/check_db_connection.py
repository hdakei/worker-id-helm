import MySQLdb
import os
# Get following env from environment
def check_mysql_connection():
    db_host = os.environ.get('DB_HOST', 'localhost')   
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')

    try:
        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        conn.close()
        return True  # Connection successful
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return False

if __name__ == "__main__":
    if check_mysql_connection():
        exit(0)  # Exit with success code if connection works
    else:
        exit(1)  # Exit with error code if connection fails 
