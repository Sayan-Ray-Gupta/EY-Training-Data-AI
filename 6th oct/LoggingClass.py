import logging


#configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'

)


#example logs
logging.debug("This is a debug message")
logging.info("Application started")
logging.warning("low memory warning")
logging.error("file not found error")
logging.critical("critical system failure")

