# Virtual-Calculator
## Introduction:
Here is source code for an example of hand tracking application (**Virtual calculator**) using **openCV** and **mediapipe**. It is a project for practicing skills in using **openCV** and image processing in computer vision. With this code, you can create a **Virtual calculator** and do basic mathematical calculation.
<p align="center">
  <img src="./result/result.gif" width=600><br/>
  <i>Result</i>
</p>

## How to use:
I track index finger tip and middle finger tip if the distance between these tracking points is less than 35px then it is considered as a click. For more details about hand tracking, you can refer to the following links: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html
<p align="center">
  <img src="./result/hand_landmarks.png" width=600><br/>
  <i>Result</i>
</p>

**Run the following command**
* *Install modules*
```bash
pip install -r requirements.txt
```
* *Run project*
```bash
python app.py
```
