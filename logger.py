import logging
import time


class Logger:
    def start_log():
        date_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        log_file_name = f"./logs/{str(date_time)}.log"
        logging.basicConfig(filename=log_file_name, filemode='w', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info("Log - START")

    def write_info(msg):
        logging.info(msg)
        print("> INFO: ", msg)

    def write_debug(msg):
        logging.debug(msg)
        print("> DEBUG: ", msg)

    def write_warning(msg):
        logging.warning(msg)
        print("> WARNING: ", msg)

    def write_error(msg):
        logging.error(msg)
        print("> ERROR: ", msg)

    def write_critical(msg):
        logging.critical(msg)
        print("> CRITICAL: ", msg)

    def end_log():
        logging.info("Log - END")
        logging.shutdown()
