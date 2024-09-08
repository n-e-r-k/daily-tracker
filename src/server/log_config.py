import logging

program_logging_level = logging.DEBUG

# quite literally just to have the changes in logging format be full program wide
def create_logger(name):
    logging.basicConfig(level=program_logging_level, format="[%(name)s] %(levelname)s | %(message)s")
    return logging.getLogger(name)
