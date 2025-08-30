# Smart Safety System with Raspberry Pi Pico

## Project Overview
This project is a **Smart Safety System** designed using **Raspberry Pi Pico**.  
The system can detect **fire**, **gas/smoke leaks**, and **motion** and alert the user through **RGB LEDs**, **buzzer**, and **OLED display**.  
Additionally, the system can be controlled using a **physical button** or a **HC-05 Bluetooth module**.

---

## Features
- **Fire Detection** using a Flame Sensor
- **Gas/Smoke Detection** using MQ-5 Sensor
- **Motion Detection** using Ultrasonic Sensor HC-SR04
- **Real-time Alert Display** on an OLED
- **Audio Alert** using a Buzzer
- **System Status Display** with RGB LED:
  - Green: Normal Status
  - Red: Danger
  - White: System Off
- **System Control**:
  - Physical Button
  - Bluetooth (on/off)

---

## Components Used

| Component                   | Quantity | Description                    |
|------------------------------|---------|--------------------------------|
| Raspberry Pi Pico            | 1       | Main controller               |
| LED RGB                      | 1       | Status Indicator              |
| Buzzer                       | 1       | Audio Alert                   |
| Flame Sensor                 | 1       | Fire Detection                |
| MQ-5 Gas Sensor              | 1       | Gas/Smoke Detection           |
| Ultrasonic Sensor HC-SR04    | 1       | Motion Detection              |
| Push Button                  | 1       | Manual Control                |
| HC-05 Bluetooth Module       | 1       | Remote Control                |
| OLED Display SSD1306         | 1       | Display Alerts & Status       |

---

## Software Structure

### Pin Configuration
- LED RGB: 11, 12, 13  
- Buzzer: 19  
- Flame Sensor: 15  
- MQ-5 Gas Sensor: 14  
- Ultrasonic Sensor: Echo=5, Trigger=4  
- Push Button: 20 (with Pull-up)  
- HC-05: UART1 (TX=8, RX=9)  
- OLED: I2C (SCL=17, SDA=16)  

---

### Main Functions
- `rgb(r, g, b)` → Controls RGB LED color  
- `oled_write(text, x, y)` → Displays text on OLED  
- `oled_clear()` → Clears the OLED display  
- `get_rtc_time()` → Returns the current time  
- `show_flame(duration)` → Displays fire alert  
- `show_gass(duration)` → Displays gas/smoke alert  
- `movement_oled()` → Displays proximity alert  
- `motion_detector(ds)` → Detects motion  
- `flame_detector()` → Detects fire  
- `smoke_detector()` → Detects gas/smoke  
- `detectors(ds)` → Checks all sensors simultaneously  
- `uart_control(last_flag, uart1)` → Controls the system via Bluetooth  
- `flag_state(button, uart1, last_flag)` → Determines the system status  

---

### Main Loop
```python
while True:
    flag = flag_state(button, uart1, flag)
    if flag:
        detectors(ds)  # Active monitoring
    else:
        rgb(1, 1, 1)   # System Off
