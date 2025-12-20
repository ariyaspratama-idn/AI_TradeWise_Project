import asyncio, schedule, threading, time
from src.utils.config import settings
from src.modules.market_analysis import update_market_data
from src.utils.logger import logger

def job():
    asyncio.run(update_market_data())
    logger.info("Pembaruan data pasar otomatis berhasil")

def start_scheduler():
    interval = settings.UPDATE_INTERVAL_MINUTES
    schedule.every(interval).minutes.do(job)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
