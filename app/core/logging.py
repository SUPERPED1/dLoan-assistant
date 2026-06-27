import logging 
import os
from datetime import date

today = date.today()

os.makedirs("log", exist_ok=True)

logging.basicConfig(level=logging.INFO, 
                    filename=f"./log/log_{today}.log", 
                    filemode='a', 
                    encoding='utf-8',
                    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")

def get_logger(name: str):
    return logging.getLogger(name)