from datetime import datetime
import psycopg2 



def save_conversation_entry(db_connection, user_id, title, content, is_draft=True):
    query = """
        INSERT INTO journal_entries (user_id, title, content, is_draft, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    
    current_timestamp = datetime.now()
    
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(
                query,
                (user_id, title, content, is_draft, current_timestamp, current_timestamp)
            )
            
            db_connection.commit()
            
            inserted_id = cursor.fetchone()[0]
            return inserted_id
    except Exception as e:
        db_connection.rollback()  
        raise e
    
