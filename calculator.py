import cv2
from hand_tracking import Tracker

class Button:
    def __init__(self, x, y, w, h, value, 
                 font=cv2.FONT_HERSHEY_COMPLEX, 
                 font_color=(255, 255, 255), 
                 thick=1, font_size=1.2):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = value
        
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.font_color = (255, 255, 255)
        self.thick = 1
        self.font_size = 1.2
        self.text_width, self.text_height = cv2.getTextSize(self.value, self.font, self.font_size, self.thick)[0]
    
    def draw(self, img):
        cv2.rectangle(img , (self.x, self.y), (self.x + self.w, self.y + self.h),
                      (50, 50, 50), cv2.FILLED)
        cv2.rectangle(img , (self.x, self.y), (self.x + self.w, self.y + self.h),
                      (10, 10, 10), 3)
        cv2.putText(img, self.value, 
                    (self.x + (self.w - self.text_width)//2, 
                    self.y + (self.h + self.text_height)//2),
                    self.font, self.font_size, self.font_color, self.thick)
        
        return img
    
    def check_click(self, img, dist, x1, y1):
        if (self.x <= x1 <= self.x+self.w) and (self.y <= y1 <= self.y+self.h) and dist <= 35:
            cv2.rectangle(img , (self.x, self.y), (self.x + self.w, self.y + self.h),
                          (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img , (self.x, self.y), (self.x + self.w, self.y + self.h),
                          (10, 10, 10), 3)
            cv2.putText(img, self.value, 
                        (self.x + (self.w - self.text_width)//2, 
                        self.y + (self.h + self.text_height)//2),
                        self.font, self.font_size, self.font_color, self.thick)
            return True
        return False

def draw_calculator(img):
    button_list_values = [['7', '8', '9', '^', '('],
                        ['4', '5', '6', '*', ')'],
                        ['1', '2', '3', '-', 'DEL'],
                        ['0', '.', '/', '+', '=']]
    button_list = []
    for i in range(4):
        for j in range(5):
            button_list.append(Button(600 + 80*j, 200 + 80*i, 80, 80, button_list_values[i][j]))
    clear_button = Button(840, 520, 160, 80, 'CLEAR')
    button_list.append(clear_button)
    for button in button_list:
        img = button.draw(img)
    img = cv2.rectangle(img, (600, 100), (1000, 200), (50, 50, 50), cv2.FILLED)
    img = cv2.rectangle(img, (600, 100), (1000, 200), (10, 10, 10), 3)
    return img, button_list
    

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    tracker = Tracker()
    equation = ''
    result = ''
    delay = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = tracker.hand_landmark(img)
        img, button_list = draw_calculator(img)
        img, dist, x1, y1 = tracker.tracking(img)
        
        for button in button_list:
            if button.check_click(img, dist, x1, y1) and delay == 0:
                print('click')


        # print(x1, y1)
        cv2.imshow('Image', img)
        cv2.waitKey(1)