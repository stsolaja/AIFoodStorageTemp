from openai import OpenAI
import cv2
import base64
import serial
import statistics
import edge_tts
import asyncio

async def speak_text(text, voice="en-US-AriaNeural", output_file="output4.mp3"):
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save(output_file)

    # Optionally, play it with macOS's built-in `afplay`
    import os
    os.system(f"afplay {output_file}")

print("Show the food item to the camera!")
asyncio.run(speak_text("Show the food item to the camera"))

def capture_and_resize_image(image_path="food.jpg", max_size=512):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        # Resize the image to reduce file size
        height, width = frame.shape[:2]
        if height > max_size or width > max_size:
            scale = max_size / max(height, width)
            frame = cv2.resize(frame, (int(width * scale), int(height * scale)))
        cv2.imwrite(image_path, frame)
        print("Image captured and resized successfully!")
        asyncio.run(speak_text("Image captured and resized successfully!"))
    else:
        print("Failed to capture image.")
        asyncio.run(speak_text("Failed to capture image."))
    cap.release()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Capture and resize image
image_path = "food.jpg"
capture_and_resize_image(image_path)

# Get the Base64 string
base64_image = encode_image(image_path)


def read_arduino_data(port='/dev/cu.usbmodem1101', baud_rate=9600, num_readings = 10): #'/dev/cu.usbmodem1101' is the port in the arduino IDE. May differ on devices and USB port used 
    readings = [] #list to store temperature readings
    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            print("Reading data from Arduino...")
            asyncio.run(speak_text("Reading data from Arduino"))
            for _ in range(num_readings):
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        readings.append(float(line))  # Convert to float if numerical data
                    except ValueError: #error handling for invalid data
                        print(f"Skipping invalid data: {line}")
    except serial.SerialException as e:
        print(f"Error: {e}")
    return readings

def find_median(readings):
    if readings:
        return statistics.median(readings)
    return None

sensor_readings = read_arduino_data('/dev/cu.usbmodem1101', 9600, 10) #'/dev/cu.usbmodem1101' is the port in the arduino IDE. May differ on devices and USB port used 
median_value = find_median(sensor_readings) # median value of 20 stored temperature readings to prevent outliers from afffecting results
print("Stored Readings:", sensor_readings) 
print("Median Temperature:", median_value, " degrees Celcius") 
asyncio.run(speak_text(f"Median Temperature: {median_value} degrees Celcius"))


client = OpenAI(api_key="API KEY GOES HERE")#Replace the text here with your OPEN AI API key

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": "in 3 words or less, What kind of food is in this image? Be as specific as possible. if theres no food, return No food detected"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=300  # Limit the response length
)
food = response.choices[0].message.content
print("Detected food:", food)

asyncio.run(speak_text(f"Detected food: {food}"))
            
if (food == "No food detected."):
    print("Scan a food item!")
    asyncio.run(speak_text("Scan a food item!"))
else:
    
    prompt = "in 50 words or less, is " + str(median_value) + " degrees celcius ideal for storing " + food + "? Also what is its shelf life in the current condition? " #ChatGPT prompt

    response = client.responses.create(
        model="gpt-4",
        input= prompt
    )
    chat = response.output_text
    print(response.output_text)
    # Run the async function
    if __name__ == "__main__":
        asyncio.run(speak_text(str(chat)))