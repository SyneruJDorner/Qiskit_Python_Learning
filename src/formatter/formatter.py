import os, time
from src.config import config

class formatter():
    @classmethod
    def clear_images(cls):
        for file in os.listdir(config.IMAGES_PATH):
            os.remove(os.path.join(config.IMAGES_PATH, file))

    @classmethod
    def file(cls, file_name: str, file_format: str):
        date_time_formated = time.strftime("%Y_%m_%d_%H_%M_%S")
        formated_name = f"{file_name}_{date_time_formated}.{file_format}"
        
        #Check if file exists and if it does, add a number to the end of the file name each time in a while loop
        number = 0
        while True:
            if os.path.exists(os.path.join(config.IMAGES_PATH, formated_name)):
                number += 1
                formated_name = f"{file_name}_{date_time_formated}_{number}.{file_format}"
            else:
                break
        
        return os.path.join(config.IMAGES_PATH, formated_name)