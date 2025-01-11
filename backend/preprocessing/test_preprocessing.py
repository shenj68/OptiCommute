from Preprocess import Preprocess
from Config import Config
import cv2 as cv
import numpy as np

config = Config()
config.video_path = "C:/Users/wwwsh/OneDrive/Documents/Projects/OptiCommute/OptiCommute Demo Clip.mp4"  
config.video_path_output = "output_test.avi"  
config.area_of_interest_coords = {
            'main-road-and-sidewalk': [(5, 176), (6, 223), (610, 372), (625, 273)],
            'close-sidewalk': [(19, 242), (3, 258), (595, 443), (603, 410)],
        }
config.resize_dimension = (640, 480)
config.save_video = False
config.see_aoi_mask = False  

preprocessor = Preprocess(config)
print("Processing video...")
processed_frames = preprocessor.preprocess()
print(f"Processed {len(processed_frames)} frames.")

# display frames
print("Displaying processed video. Press 'q' to exit.")
for frame in processed_frames:
    cv.imshow("Processed Frame", frame)
    if cv.waitKey(30) & 0xFF == ord('q'): 
        break

cv.destroyAllWindows()

if config.save_video:
    print(f"Saved processed video to {config.video_path_output}")
    saved_cap = cv.VideoCapture(config.video_path_output)
    if not saved_cap.isOpened():
        print("Error: Could not open the saved video.")
    else:
        saved_frame_count = int(saved_cap.get(cv.CAP_PROP_FRAME_COUNT))
        print(f"Saved video frame count: {saved_frame_count}")
        saved_cap.release()
