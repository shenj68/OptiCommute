import numpy as np
import cv2 as cv

#TODO: add console logger
 
class Preprocess:
    def __init__(self, config):
        """
        init preprocess class with setings from Config class
        """

        self.config = config
        self.cap = cv.VideoCapture(self.config.video_path)

        if not self.cap.isOpened():
            raise FileNotFoundError(f"Cant open file {self.config.video_path}")
        
        # get init vid settings
        self.frame_width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
        self.frame_count = int(self.cap.get(cv.CAP_PROP_FRAME_COUNT))
        
        print(f"found video {self.config.video_path}")
        print(f"video metadata: width: {self.frame_width}, height: {self.frame_height}, fps: {self.fps}, frame_count: {self.frame_count}")

        # if save is turned on, we can enable the video writer
        if self.config.save_video:
            fourcc = cv.VideoWriter_fourcc(*'XVID')
            self.out = cv.VideoWriter(
                self.config.video_path_output,
                fourcc,
                self.fps,
                (self.config.resize_dimension[0], self.config.resize_dimension[1])
            )
        else:
            self.out = None

    @staticmethod
    def preprocess(self):
        """
        go through video and extract frame by frame.

        each frame will:
            - get resized/cropped
            - apply an area of interest (AOI) mask

        """

        processed_frames = []

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # resize frame
            resized_frame = cv.resize(frame, self.config.resize_dimension)

            # apply aoi mask
            aoi_mask, visualized_frame = self.add_aoi_mask(
                resized_frame,
                self.config.area_of_interest_coords,
                visualize=self.config.see_aoi_mask
            )

            masked_frame = cv.bitwise_and(resized_frame, resized_frame, mask=aoi_mask)

            output_frame = visualized_frame if self.config.see_aoi_mask else masked_frame

            processed_frames.append(output_frame)

            if self.config.save_video and self.out:
                self.out.write(output_frame)


        # release/free
        self.cap.release()
        if self.out:
            self.out.release()
        
        return processed_frames
    
    def add_aoi_mask(frame, aoi_coords, visualize_aoi=False):
        """
        draw and apply the aoi mask on the frame
        """
        
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)

        cv.fillPoly(mask, [np.array(aoi_coords, dtype=np.int32)], 255) # 255 = white

        if visualize_aoi:
            visualized_frame = frame.copy()
            cv.polylines(visualized_frame, [np.array(aoi_coords, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
            return mask, visualized_frame

        return mask, frame

