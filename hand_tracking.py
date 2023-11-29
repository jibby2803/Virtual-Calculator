import cv2
import mediapipe as mp

class Tracker():
    def __init__(self, static_image_mode=False, max_num_hands=1, 
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        
        self.hands = mp.solutions.hands.Hands(static_image_mode=self.static_image_mode,
                                              max_num_hands=self.max_num_hands,
                                              min_detection_confidence=self.min_detection_confidence,
                                              min_tracking_confidence=self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.tracking_id = [8, 12]
           
    
    def hand_landmark(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        return img
    
    def tracking(self, img):
        tracking_points = []
        dist = 10e5 
        x1 = -1
        y1 = -1
        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(hand_landmarks.landmark):
                if id in self.tracking_id:
                    h, w, c = img.shape
                    x, y = int(lm.x*w), int(lm.y*h)
                    tracking_points.append((x, y))
                    cv2.circle(img, (x, y), 10, (255, 0, 255), cv2.FILLED)  
            x1, y1 = tracking_points[0]
            x2, y2 = tracking_points[1]
            x_c = (x1+x2)//2
            y_c = (y1+y2)//2
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (x_c, y_c), 10, (255, 0, 255), cv2.FILLED)  
            dist = ((x1-x2)**2 + (y1-y2)**2)**0.5    
            cv2.putText(img, f'distance: {dist}', (40, 40),cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)         
        
        return img, dist, x1, y1
    
    
    
if __name__ == '__main__':   
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    tracker = Tracker()
    while True:
        success, img = cap.read()
        img = tracker.hand_landmark(img)
        img, dist, x_1, y_1 = tracker.tracking(img)
        cv2.imshow('Image', img)
        cv2.waitKey(1)
                    