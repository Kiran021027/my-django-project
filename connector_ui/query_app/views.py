
import mysql.connector
import psycopg2
import sqlite3
import clickhouse_connect
from django.shortcuts import render


# Define the function to validate database credentials
def validate_database_credentials(db_type, host, user, password, database, port):
    """Validate the database credentials."""
    try:
        if db_type == "mysql":
            connection = mysql.connector.connect(
                host=host, user=user, password=password, database=database, port=port)
            connection.close()

        elif db_type == "postgresql":
            connection = psycopg2.connect(
                host=host, user=user, password=password, dbname=database, port=port)
            connection.close()

        elif db_type == "sqlite":
            connection = sqlite3.connect(database)  # SQLite only needs a file path
            connection.close()

        elif db_type == "clickhouse":
            client = clickhouse_connect.get_client(
                host=host, port=port, username=user, password=password, database=database)
            client.query("SELECT 1")  # Try a simple query to validate the connection
            client.close()

        else:
            return False, "Unsupported database type."

        return True, "Database credentials are valid."

    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def query_page(request):
    """Handles SQL query execution for different databases."""
    context = {'error': None, 'result': None}

    if request.method == 'POST':
        # Get user input for database credentials and query
        db_type = request.POST.get('db_type')
        host = request.POST.get('host')
        user = request.POST.get('user')
        password = request.POST.get('password')
        database = request.POST.get('database')
        port = request.POST.get('port', 3306)  # Default to MySQL port if not provided
        query = request.POST.get('query')

        # Validate the provided database credentials
        is_valid, validation_message = validate_database_credentials(
            db_type, host, user, password, database, port)

        if not is_valid:
            context['error'] = validation_message
        else:
            try:
                if db_type == "clickhouse":
                    # ✅ ClickHouse Query Execution
                    client = clickhouse_connect.get_client(
                        host=host, port=port, username=user, password=password, database=database)
                    result = client.query(query)
                    context['result'] = result.result_rows
                    client.close()

                else:
                    # ✅ MySQL/PostgreSQL/SQLite Execution zdcs
                    if db_type == "mysql":
                        connection = mysql.connector.connect(
                            host=host, user=user, password=password, database=database, port=port)
                    elif db_type == "postgresql":
                        connection = psycopg2.connect(
                            host=host, user=user, password=password, dbname=database, port=port)
                    elif db_type == "sqlite":
                        connection = sqlite3.connect(database)
                    cursor = connection.cursor()
                    cursor.execute(query)
                    context['result'] = cursor.fetchall()
                    connection.close()

                context['error'] = None  # Reset error if successful

            except Exception as e:
                context['error'] = f"Database Error: {str(e)}"

    return render(request, "query_app/query_page.html", context)


# Function to simulate the local test of querying different databases
def test_query_locally(db_type, host, user, password, database, port, query):
    """Test database connection and query execution locally."""
    is_valid, validation_message = validate_database_credentials(
        db_type, host, user, password, database, port)

    if not is_valid:
        return f"Validation Error: {validation_message}"

    try:
        if db_type == "clickhouse":
            # ✅ ClickHouse Query Execution
            client = clickhouse_connect.get_client(
                host=host, port=port, username=user, password=password, database=database)
            result = client.query(query)
            result_data = result.result_rows
            client.close()

        else:
            # ✅ MySQL/PostgreSQL/SQLite Execution
            if db_type == "mysql":
                connection = mysql.connector.connect(
                    host=host, user=user, password=password, database=database, port=port)
            elif db_type == "postgresql":
                connection = psycopg2.connect(
                    host=host, user=user, password=password, dbname=database, port=port)
            elif db_type == "sqlite":
                connection = sqlite3.connect(database)
            cursor = connection.cursor()
            cursor.execute(query)
            result_data = cursor.fetchall()
            connection.close()

        return {"error": None, "result": result_data}

    except Exception as e:
        return {"error": f"Database Error: {str(e)}", "result": None}


# Function to simulate a POST request for testing purposes
def test_query_with_post(db_type, host, user, password, database, port, query):
    """Test database connection and query execution locally."""
    is_valid, validation_message = validate_database_credentials(
        db_type, host, user, password, database, port)

    if not is_valid:
        return f"Validation Error: {validation_message}"

    try:
        if db_type == "clickhouse":
            # ✅ ClickHouse Query Execution
            client = clickhouse_connect.get_client(
                host=host, port=port, username=user, password=password, database=database)
            result = client.query(query)
            result_data = result.result_rows
            client.close()

        else:
            # ✅ MySQL/PostgreSQL/SQLite Execution
            if db_type == "mysql":
                connection = mysql.connector.connect(
                    host=host, user=user, password=password, database=database, port=port)
            elif db_type == "postgresql":
                connection = psycopg2.connect(
                    host=host, user=user, password=password, dbname=database, port=port)
            elif db_type == "sqlite":
                connection = sqlite3.connect(database)
            cursor = connection.cursor()
            cursor.execute(query)
            result_data = cursor.fetchall()
            connection.close()

        return {"error": None, "result": result_data}

    except Exception as e:
        return {"error": f"Database Error: {str(e)}", "result": None}





# Example for Testing
# if __name__ == "__main__":
#     # Example credentials and query for testing MySQL/m/ef/sdc
#     db_details = {
#         "db_type": "",
#         "host": "",
#         "user": m",
#         "password": "",
#         "database": "",
#         "port": ,
#         "query": "SELECT * FROM nlp_hiring_data LIMIT 5;"
#     }
#
#     # Simulate a local POST request and test the query
#     result = test_query_with_post(
#         db_details["db_type"],
#         db_details["host"],
#         db_details["user"],
#         db_details["password"],
#         db_details["database"],
#         db_details["port"],
#         db_details["query"]
#     )
#
#     print(f"Test Result: {result}")
