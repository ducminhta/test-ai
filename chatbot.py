import sqlite3
from openai import OpenAI
from datetime import datetime

# Set your OpenAI API key here
OPENAI_API_KEY 
client = OpenAI(api_key=OPENAI_API_KEY)

def connect_db():
    return sqlite3.connect('facility_management.db')

def format_result(cursor, rows, headers=None):
    if not rows:
        return "No results found."
    
    if headers is None:
        headers = [description[0] for description in cursor.description]
    
    # Calculate column widths
    widths = [len(str(header)) for header in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))
    
    # Create format string for rows
    format_str = " | ".join(f"{{:<{width}}}" for width in widths)
    separator = "-+-".join("-" * width for width in widths)
    
    # Format the results
    result = []
    result.append(format_str.format(*headers))
    result.append(separator)
    for row in rows:
        result.append(format_str.format(*[str(val) if val is not None else "" for val in row]))
    
    return "\n".join(result)

def get_schema_info():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get table schemas
    cursor.execute("""
        SELECT name, sql FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
    """)
    
    schema_info = []
    for table_name, create_sql in cursor.fetchall():
        schema_info.append(f"Table: {table_name}")
        schema_info.append(create_sql)
        
        # Get sample data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        columns = [description[0] for description in cursor.description]
        schema_info.append(f"Columns: {', '.join(columns)}\n")
    
    conn.close()
    return "\n".join(schema_info)

def natural_to_sql(query):
    schema = get_schema_info()
    
    system_prompt = f"""You are a SQL expert that converts natural language questions to SQL queries.
    You will be given the database schema and a natural language question.
    Respond ONLY with the SQL query that answers the question.
    Do not include any explanations or additional text.
    
    Database Schema:
    {schema}
    
    Rules:
    1. Use only the tables and columns shown in the schema
    2. Return only the SQL query, nothing else
    3. Use proper JOIN syntax when combining tables
    4. Order results in a logical way (e.g., by date for tasks, by name for people)
    5. Keep queries simple and efficient
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0,
            max_tokens=200
        )
        
        sql_query = response.choices[0].message.content.strip()
        return sql_query
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

def chat():
    print("Facility Management AI Chatbot")
    print("Ask me anything about rooms, people, or tasks!")
    print("Type 'exit' to quit.")
    print("\nExample questions:")
    print("- Which rooms are available on the first floor?")
    print("- Who is responsible for maintenance tasks?")
    print("- Show me all pending tasks in room 101")
    print("- What is the capacity of each room?")
    print("- List all tasks assigned to John")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    while True:
        try:
            query = input("\nYour question: ").strip()
            
            if query.lower() in ['exit', 'quit', 'bye']:
                break
            
            sql = natural_to_sql(query)
            
            if sql:
                print("\nExecuting SQL query:", sql)  # Show the generated SQL query
                cursor.execute(sql)
                rows = cursor.fetchall()
                print("\n" + format_result(cursor, rows))
            else:
                print("\nI couldn't generate a SQL query for that question. Please try rephrasing it!")
                
        except sqlite3.Error as e:
            print(f"\nDatabase error: {e}")
        except Exception as e:
            print(f"\nError: {e}")
    
    conn.close()
    print("\nGoodbye!")

if __name__ == '__main__':
    if OPENAI_API_KEY == "your_api_key_here":
        print("Please set your OpenAI API key in the script first!")
    else:
        chat()
