
# Krishi Connect

A smart IoT-based system for automating, predicting and monitoring farming-related tasks. The users of this initiative are specifically farmers.


## Requirements

For hardware part:
https://github.com/MrKnightmare007/KrishiConnect/blob/main/hardware.txt

For software part
```
pip install -r requirements.txt
```
## Usage

```git
git clone https://github.com/MrKnightmare007/KrishiConnect.git
cd KrishiConnect
```
Connect your ATmega328P + Node MCU ESP8266 board to your computer.
Then switch on the 3 & 4 dip switches on the board.
Upload the 4_sen_esp.ino file by selecting Arduino Uno as the board.

Repeat the process by switching 5, 6 & 7 switches and selecting ESP8266 as board and final_send_data_flask.ino as the upload file.

Finally for the connection of atmega and esp switch on 1,2,5 & 6 dip switches which will host the sensor values onto different routes.

Then type in terminal:

For Windows
```python
python app.py
```
For Linux
```python
python3 app.py
```

Final Step: 
access http://localhost:5000 for the website.

## Screenshots

![App Screenshot](https://i.ibb.co/dWWxzzQ/image.png)

![App Screenshot](https://i.ibb.co/bWn0Sz9/image.png)

![App Screenshot](https://i.ibb.co/vh0F0qj/image.png)

![App Screenshot](https://i.ibb.co/8KrwG0X/image.png)




## Authors

- [@aroproduction](https://www.github.com/aroproduction)
- [@MrKnightmare007](https://github.com/MrKnightmare007)



## Tech Stack

- Python
- HTML
- CSS
- Javascript
- Arduino (C, C++, Java)


## License

License Free for the time being.

