class Config:
    """
    - resize_dimension = video will be resized to this dimension (lxw)
    - (list of (x,y)) area_of_interest_coords = rough coordinates of area of interest within video
    - video_path = path to video/uploaded file (TODO)\
    - save_video = True/False on saving video (Default: False)
    - video_path_output = output path of where it will be saved (if saved is turned on)
    
    """

    def __init__(self):
        self.resize_dimension = (640, 480)
        self.area_of_interest_coords = []
        self.save_video = False
        self.video_path = "OptiCommute Demo Clip.mp4"
        self.video_path_output = "output/processed_vid.mp4"
        