import logging
import os.path
from datetime import datetime
import time

import torch
import cv2
import math
from app import LocationsMapping, CarsState
import logging.config

DETECTION_THRESHOLD = 0.8
DETECTION_SIZE_THRESHOLD = 30
DETECTION_CLASSES = ('car', 'truck')
DATE_FORMATTED = datetime.now().strftime("%m-%d-%Y")
HOUR_FORMATTED = datetime.now().strftime("%H:%M:%S")
PATH = os.getcwd()
MODEL = "yolov5"
MODEL_SIZE = "x"
TORCH_MODEL = f"{MODEL}{MODEL_SIZE}"

log_file_path = f"{PATH}/app/logger.conf"
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)


class VideoFeed:

    def __init__(self):
        self.cap = cv2.VideoCapture('rtsp://delarea:delarea6@10.100.102.55:554/stream1')
        self.cars_count = CarsState.CarState()
        self.cars_locations = LocationsMapping.CarsLocations()
        self.frame = None
        self.logger = logging.getLogger("VideoFeed")
        if os.path.isfile(f"f{PATH}/{TORCH_MODEL}"):
            self.model = torch.hub.load(fr'/{TORCH_MODEL}', 'custom',
                                        path=f'{PATH}/{TORCH_MODEL}.pt', source='local')
        else:
            self.model = torch.hub.load('ultralytics/yolov5', TORCH_MODEL)
        self.logger.info("Init succesfuly")

    def __process_detections(self, results):
        df = results.pandas().xyxy[0]
        count = 0
        for i in df.index:
            label = df['name'][i]
            if label in DETECTION_CLASSES:
                x1, y1 = int(df['xmin'][i]), int(df['ymin'][i])
                x2, y2 = int(df['xmax'][i]), int(df['ymax'][i])
                # only add if the diff is really different
                confidence = df.confidence[i]
                confidence = round(confidence, 3)
                is_small_sized = math.fabs(x1 - x2) < DETECTION_THRESHOLD or math.fabs(
                    y1 - y2) < DETECTION_SIZE_THRESHOLD
                if confidence < DETECTION_THRESHOLD or is_small_sized:
                    # mark False Positives to debug
                    cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    cv2.putText(self.frame, str(confidence), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255),
                                1)
                    cv2.putText(self.frame, label, (x1 + 35, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255), 1)
                else:
                    # mark successful detections
                    self.cars_locations.add((x1, x2, y1, y2))
                    count += 1
                    cv2.rectangle(self.frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                    cv2.putText(self.frame, str(confidence), (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255),
                                1)

        if self.cars_count.update_count(count) is True:
            self.__save_snapshot()

    def __save_snapshot(self):
        self.logger.info(f"Amount of cars: {self.cars_count.count}")
        dir_name = f"{PATH}/app/changes/{DATE_FORMATTED}"
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        filename = f"{dir_name}/{HOUR_FORMATTED}-{self.cars_count.count}-cars.jpeg"
        suc = cv2.imwrite(filename, self.frame)
        self.logger.info(f"image save : {suc}")

    def run(self):
        self.logger.info("starting to read video feed")
        while True:
            time.sleep(3)
            self.frame = self.cap.read()[1]
            if self.frame is None:
                self.logger.error("Video-stream is None!")
                time.sleep(5)
                continue

            gray_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            # cv2.imshow('gray', gray_frame)

            # Detect cars
            results = self.model(gray_frame)
            self.__process_detections(results)

            # cv2.imshow('res', self.frame)
            # cv2.waitKey(100)

        self.logger.info("Destroying video feed.")
        self.cap.release()
        cv2.destroyAllWindows()
