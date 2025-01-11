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
        print(f"video metadata: \n\t-width: {self.frame_width}, \n\t-height: {self.frame_height}, \n\t-fps: {self.fps}, \n\t-frame_count: {self.frame_count}")

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
        
            # combine and apply aoi mask
            combined_mask = self.create_combined_aoi_mask(resized_frame, self.config.area_of_interest_coords)

            # visualize aoi if enabled
            if self.config.see_aoi_mask:
                visualized_frame = self.visualize_multiple_masks(resized_frame, self.config.area_of_interest_coords)
                output_frame = visualized_frame
            else:
                output_frame = cv.bitwise_and(resized_frame, resized_frame, mask=combined_mask)

            #output_frame = visualized_frame if self.config.see_aoi_mask else masked_frame

            processed_frames.append(output_frame)

            if self.config.save_video and self.out:
                self.out.write(output_frame)


        # release/free
        self.cap.release()
        if self.out:
            self.out.release()
        
        return processed_frames
    
    def create_combined_aoi_mask(self, frame, masks):
        """
        combine multiple AOI masks into a single mask.
        """
        combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        for mask_coords in masks.values():
            cv.fillPoly(combined_mask, [np.array(mask_coords, dtype=np.int32)], 255)
        return combined_mask

    def visualize_multiple_masks(self, frame, masks):
        """
        visualize multiple AOI masks on the frame.
        """
        visualized_frame = frame.copy()
        for mask_coords in masks.values():
            cv.polylines(visualized_frame, [np.array(mask_coords, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
        return visualized_frame

