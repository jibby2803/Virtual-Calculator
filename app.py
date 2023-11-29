import cv2 
from hand_tracking import Tracker
from calculator import Button, draw_calculator

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
            if button.value == 'DEL':
                if equation=='':
                    equaion = ''
                elif equation == 'error':
                    equation = ''
                else:
                    equation = equation[:-1]
                delay = 1
            elif button.value == '^':
                if equation == 'error':
                    equation = ''
                equation += '**'
                delay = 1
            elif button.value == 'CLEAR':
                if equation == 'error':
                    equation = ''
                equation = ''
                delay = 1
            elif button.value == '=':
                if equation == 'error':
                    equation = ''
                if equation=='':
                    equation=''
                else:
                    try:
                        equation = str(eval(equation))
                    except:
                        equation = 'error'
                delay = 1
            else:
                if equation=='error':
                    equation = ''
                equation += button.value
                cv2.putText(img, equation, (600, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
                delay = 1
    if delay:
        delay += 1
        if delay > 10:
            delay = 0
        
    cv2.putText(img, equation, (600, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    cv2.imshow('Image', img)
    cv2.waitKey(1)