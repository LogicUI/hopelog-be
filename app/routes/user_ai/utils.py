from datetime import datetime
from pytz import timezone as pytz_timezone
import logging
import json


def get_current_time(timezone):
    current_time = datetime.now(pytz_timezone(timezone))
    logging.info("Current time: %s", current_time)
    return current_time.strftime("%d %b %Y at %I:%M%p").replace(" 0", " ")


def get_user_journal_stats(db_connection, user_id):
    query = """
        SELECT total_no_of_entries, entries_this_month, is_subscribed
        FROM user_journal_summary 
        WHERE user_id = %s;
    """

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                return {
                    "total_entries": result[0],
                    "entries_this_month": result[1],
                    "is_subscribed": result[2],
                }
            return {"total_entries": 0, "entries_this_month": 0, "is_subscribed": False}

    except Exception:
        db_connection.rollback()
        raise


def save_test_conversation_entry(
    db_connection, title, summary, analysis, emotions, current_time, test_user_id
):

    insert_query = """
        INSERT INTO test_user_journal_entries (user_id, title, summary, analysis, emotions, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id) 
        DO UPDATE SET
            title = EXCLUDED.title,
            summary = EXCLUDED.summary,
            analysis = EXCLUDED.analysis, 
            emotions = EXCLUDED.emotions,
            updated_at = EXCLUDED.updated_at
        RETURNING id;
    """

    try:
        with db_connection.cursor() as cursor:
            # Convert emotions dict to JSON string
            emotions_json = json.dumps(emotions["emotions"])

            cursor.execute(
                insert_query,
                (
                    test_user_id,
                    title,
                    summary,
                    analysis,
                    emotions_json,
                    current_time,
                    current_time,
                ),
            )

            db_connection.commit()
            inserted_id = cursor.fetchone()[0]
            return inserted_id

    except Exception:
        db_connection.rollback()
        raise


def save_conversation_logs(db_connection, user_text: str, therapist_response: str):
    """
    Save conversation logs between user and AI therapist

    Args:
        db_connection: Database connection object
        user_text: Text input from the user
        therapist_response: Response from the AI therapist

    Returns:
        int: ID of the inserted conversation log
    """
    query = """
        INSERT INTO conversation_logs (user_text, therapist_response)
        VALUES (%s, %s)
        RETURNING id;
    """

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    user_text,
                    therapist_response,
                ),
            )

            db_connection.commit()
            inserted_id = cursor.fetchone()[0]
            return inserted_id

    except Exception:
        db_connection.rollback()
        raise


async def get_user_account_details(db_connection, user_id):
    query = """
        SELECT 
            user_journals.total_no_of_entries as total_entries,
            user_journals.entries_this_month ,
            user_journals.is_subscribed, 
            user_journals.subscription_start_date as subscription_start,
            user_journals.subscription_end_date as subscription_end,
            user_journals.subscription_current_period_end as subscription_current_period_end,
            user_journals.subscription_id as subscription_id,
            auth_user.email,
            auth_user.raw_user_meta_data
        FROM 
            user_journal_summary AS user_journals
        JOIN  
            auth.users AS auth_user 
        ON 
            user_journals.user_id = auth_user.id
        WHERE auth_user.id = %s
    """

    try:
        logging.info("executing results")
        with db_connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            logging.info("Result: %s", result)
            if result:
                # Convert result tuple to dict with column names
                columns = [
                    "total_entries",
                    "entries_this_month",
                    "is_subscribed",
                    "subscription_start",
                    "subscription_end",
                    "subscription_current_period_end",
                    "subscription_id",
                    "email",
                    "raw_user_meta_data",
                ]
                logging.info("Result: %s", result)
                logging.info("Columns: %s", columns)
                result_dict = dict(zip(columns, result))
                result_dict["user_id"] = user_id
                return result_dict
            return None
    except Exception:
        db_connection.rollback()
        raise


def cancel_user_subscription(db_connection, user_id, current_period_end):
    query = """
        UPDATE user_journal_summary 
        SET subscription_end_date = date(to_timestamp(%s))
        WHERE user_id = %s
        RETURNING user_id;
    """

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(query, (current_period_end, user_id))
            db_connection.commit()
            updated_id = cursor.fetchone()
            return bool(updated_id)

    except Exception:
        db_connection.rollback()
        raise


def update_user_subscription(
    db_connection, user_id, current_period_end, subscription_id
):
    query = """
            UPDATE user_journal_summary 
            SET is_subscribed = true,
                subscription_start_date = CURRENT_DATE,
                subscription_current_period_end  = date(to_timestamp(%s)),
                subscription_id = %s
            WHERE user_id = %s
            RETURNING user_id;
    """

    try:
        with db_connection.cursor() as cursor:
            cursor.execute(query, (current_period_end, subscription_id, user_id))
            db_connection.commit()
    except Exception:
        db_connection.rollback()
        raise


def save_conversation_entry(
    db_connection, user_id, title, summary, analysis, emotions, current_time
):
    query = """
        INSERT INTO journal_entries (user_id, title, summary, analysis, emotions, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """
    flattened_emotions = emotions["emotions"]
    logging.info("Flattened emotions: %s", flattened_emotions)
    emotions_json = json.dumps(flattened_emotions)
    logging.info("Emotions JSON: %s", emotions_json)
    current_timestamp = current_time
    logging.info("Current timestamp: %s", current_timestamp)

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


def get_test_user_entries(db_connection, user_id):
    query = """
        SELECT id, title, summary, analysis, created_at, emotions
        FROM test_user_journal_entries
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
        logging.error("Failed to fetch test user entries: %s", e)
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
