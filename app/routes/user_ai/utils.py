from datetime import datetime
import logging
import json


def save_conversation_entry(db_connection, user_id, title, summary, analysis, emotions):
    query = """
        INSERT INTO journal_entries (user_id, title, summary, analysis, emotions, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    flattened_emotions = emotions["emotions"]
    logging.info("Flattened emotions: %s", flattened_emotions)
    emotions_json = json.dumps(flattened_emotions)
    logging.info("Emotions JSON: %s", emotions_json)
    current_timestamp = datetime.now()

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    user_id,
                    title,
                    summary,
                    analysis,
                    emotions_json,
                    current_timestamp,
                    current_timestamp,
                ),
            )

            db_connection.commit()

            inserted_id = cursor.fetchone()[0]
            return inserted_id
    except Exception:
        db_connection.rollback()
        raise


def get_conversational_entries(db_connection, user_id):
    query = """
        SELECT id, title, summary, analysis, created_at, emotions
        FROM journal_entries
        WHERE user_id = %s
        ORDER BY created_at DESC;
    """

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            entries = []
            for row in rows:
                entry = dict(zip(columns, row))
                created_at = entry.get("created_at")

                if created_at:
                    try:
                        parsed_date = datetime.fromisoformat(str(created_at))
                    except ValueError:
                        parsed_date = datetime.strptime(
                            str(created_at), "%Y-%m-%d %H:%M:%S"
                        )

                    entry["created_at"] = parsed_date.strftime("%d %b %Y at %I:%M %p")

                entries.append(entry)

            return entries

    except Exception as e:
        logging.error("Failed to fetch conversational entries: %s", e)
        raise


def delete_conversational_entry(db_connection, entry_id):
    query = """
        DELETE FROM journal_entries
        WHERE id = %s;
    """

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(query, (entry_id,))
            db_connection.commit()

            if cursor.rowcount == 0:
                raise ValueError("Entry not found")

    except Exception as e:
        db_connection.rollback()
        logging.error("Failed to delete conversational entry: %s", e)
        raise
