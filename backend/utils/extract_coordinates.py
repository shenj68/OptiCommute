import cv2 as cv
import numpy as np

points = []

def click_event(event, x, y, flags, param):
    """
    capture mouse click events and dynamically draw a polygon.
    """
    global points

    if event == cv.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Added Point: ({x}, {y})")
        frame = param['frame']
        cv.circle(frame, (x, y), radius=5, color=(0, 0, 255), thickness=-1) # red circle for each vertex

        # draw the line (to connect pts)
        if len(points) > 1:
            cv.line(frame, points[-2], points[-1], color=(0, 255, 0), thickness=2)

        cv.imshow("Draw Polygon", frame)

    # use right-click to draw the last pt
    elif event == cv.EVENT_RBUTTONDOWN:  
        if len(points) > 2:
            frame = param['frame']
            cv.polylines(frame, [np.array(points, dtype=np.int32)], isClosed=True, color=(255, 0, 0), thickness=2)
            cv.imshow("Draw Polygon", frame)

def extract_polygon(video_path):
    """
    Extract polygon coordinates from the first frame of a video using mouse clicks.
    """
    global points

    cap = cv.VideoCapture(video_path)

    # only need the first frame
    ret, frame = cap.read()
    original_frame = frame.copy()
    frame = cv.resize(frame, (640, 480))
    cv.imshow("Draw Polygon", frame)

    cv.setMouseCallback("Draw Polygon", click_event, {'frame': frame})

    print("Left click to select points, right click to finalize the polygon. Press 'q' to quit.")

    # r to reseet, q to quit
    while True:
        key = cv.waitKey(1) & 0xFF
        if key == ord('r'):  
            frame[:] = original_frame  
            points = []  
            cv.imshow("Draw Polygon", frame)
            print("Reset the polygon.")
        elif key == ord('q'):
            break

    #print the pts in the console
    print("Selected Polygon Coordinates:")
    print(f"{points[0], points[1], points[2], points[3]}")
    # for point in points:
    #     print(point)

    cap.release()
    cv.destroyAllWindows()


video_path = "C:/Users/wwwsh/OneDrive/Documents/Projects/OptiCommute/OptiCommute Demo Clip.mp4"
extract_polygon(video_path)
