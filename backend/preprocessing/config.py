class Config:
    """
    - resize_dimension = video will be resized to this dimension (lxw)
    - area_of_interest_coords = rough coordinates of area of interest within video (AOI)
    - video_path = path to video/uploaded file (TODO)\
    - save_video = True/False on saving video (Default: False)
    - video_path_output = output path of where it will be saved (if saved is turned on)
    
    """

    def __init__(self):
        self.resize_dimension = (640, 480)
        self.area_of_interest_coords = {
            'main-road-and-sidewalk': [(5, 176), (6, 223), (610, 372), (625, 273)],
            'close-sidewalk': [(19, 242), (3, 258), (595, 443), (603, 410)],
        }
        [(100, 100), (300, 100), (300, 250), (100, 250)]
        self.save_video = False
        self.video_path = "C:/Users/wwwsh/OneDrive/Documents/Projects/OptiCommute/OptiCommute Demo Clip.mp4"
        self.video_path_output = "output/processed_vid.mp4"
        self.see_aoi_mask = False
        