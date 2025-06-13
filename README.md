# AIFoodStroageTemp

A smart, AI based system integrating Python, C++, Open AI API, GPT-4 Vision, Open CV, Edge TTS and Arduino for measuring temperature and providing AI-driven insights to the ideal temperature and shelf life of the any detected food item in real-time. Edge TTS is used to prompt the user to show the item to the camera though voice. Open CV is then used to caputre the item and it is resized and sent to Chat GPT to detect what food is in the image. Temperature is read through the sensor and the values are sent to the arduino which then print the values to the serial monitor every second. 20 temperature values are retrieved from the serial monitor in python and stored in a list. The median is then calculated and stored. The detected food, as well as the median temperature value are used in a prompt to ChatGPT to give insight on the ideal storage temperature and the projected shelf life in such conditions. The response, to the prompt is printed in the Python terminal and spoken.

Software Requirements:

Arduino IDE

Python 3.x

Required Python libraries: pyserial, statistics, OpenAI, Open CV, Async, Edge TTS

Hardware Requirements:

Arduino Mega 2560

Temperature sensor

Jumper wires

USB cable

Computer with webcam
