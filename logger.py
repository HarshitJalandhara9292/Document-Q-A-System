import logging

def setup_logger():
    logging.basicConfig(
        filename='app.log',
        filemode='a',
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
    )
