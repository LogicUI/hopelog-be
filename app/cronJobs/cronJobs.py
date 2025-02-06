from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from database_init import get_db_connection

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def reset_monthly_entries():
    """Reset entries_this_month to 0 for all users at the start of each month"""
    try:
        for conn in get_db_connection():
            cur = conn.cursor()

            update_query = """
                UPDATE user_journey_summary 
                SET entries_this_month = 0
            """

            cur.execute(update_query)
            conn.commit()
            logger.info("Successfully reset entries_this_month for all users")

    except Exception as e:
        logger.error(f"Error resetting monthly entries: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()


def init_cron_jobs():
    """Initialize and start the cron jobs"""
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        reset_monthly_entries,
        trigger=CronTrigger(day="1", hour="0", minute="0"),
        id="reset_monthly_entries",
        name="Reset entries_this_month counter",
        replace_existing=True,
    )

    # Start the scheduler
    scheduler.start()
    logger.info("Monthly entries reset cron job has been scheduled")

    return scheduler
