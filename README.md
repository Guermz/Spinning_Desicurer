# Spinning Desicurer and Controller

These scripts were developed to control an upgraded version of the Spinning Desicurer, originally described in the publication:
"Spinning Desicurer: A Cost-Effective and Generalizable Post-Processing Method for Enhanced Optical Quality in 3D-Printed Microfluidics"
Published in MRS Communications, 2024. (https://link.springer.com/article/10.1557/s43579-024-00594-9)

The hardware has since been enhanced with a brushless DC motor to enable smoother and more consistent layer formation.

The Spinning Desicurer is a post-processing device for resin-based 3D printing that integrates spin coating, vacuum drying, and UV curing into a single system. It enables solvent-free resin removal, surface smoothing, and efficient curing, resulting in transparent, fully cured, and non-sticky 3D-printed parts.

This GUI application is designed to control your own Spinning Desicurer for timed motor and UV LED operations using an Arduino. It allows for automated curing sequences useful in microfabrication, polymerization, or lab prototyping tasks.

<p align="center">
  <img src="/images/spinning_desicurer_process.png" alt="Desicurer Setup" width="550">
  <br>
  <em>Spinning Desicurer Process (The chip is a REAL IMAGE not a render!).</em>
</p>


---

## Features (Full Version)

- **Step 1 Sequence**:
  - Spins motor for a user-defined time (default: 3 minutes)
  - Then activates UV LED while spinning for a user-defined time (default: 5 minutes)

- **Step 2 Sequence**:
  - Simultaneously activates motor and UV LED for a set duration (default: 3 minutes)

- **Custom Commands**:
  - Manually send serial commands like `LED ON MOTOR 1200`

- **Timer Display**:
  - Live countdown during each step phase

- **Stop Button**:
  - Interrupts any running sequence immediately

- **Custom Settings Panel**:
  - Adjust spin/LED times and motor speed before running steps

- **Automatic Arduino Detection**:
  - The GUI connects to your Arduino automatically at startup

---

## How to Use

1. Connect your Arduino and open the app.
2. Select or modify your desired durations and motor speed.
3. Click **Step 1** or **Step 2** to run an automated curing sequence.
4. Use **STOP** to cancel at any time.
5. Use the **Custom Command** box for manual control.

---

## Required Hardware

| Component         | Description                             | Link                            |
|------------------|-----------------------------------------|---------------------------------|
| Arduino Uno      | Central Microcontroller | [Buy on Amazon](https://amzn.to/4lwfcT1)             |
| UV LED           | For photopolymerization curing         | [Buy on Amazon](https://amzn.to/4nWaHmj)             |
| ESC (Electronic Speed Controller) | Controls brushless motor       | [Buy on Amazon](https://amzn.to/4eSz1RX)             |
| Brushless DC Motor | Drives the spinning platform           | [Buy on Amazon](https://amzn.to/4lyWeLw)             |
| Power Supply (12V) | Powers motor and LED          | [Buy on Amazon](https://amzn.to/3IS3vYg)             |
| LED Controller     | Microntroller to control LED           |[Buy on Amazon](https://amzn.to/4lTCz8S)             |
| Dessicator | For housing UV led and motor | [Buy on Amazon](https://amzn.to/3IwXsZ5)             |
| LED Heatsink + Mount | For mounting LED to dessicator | [Buy on Amazon](https://amzn.to/4lHWZlO)             |
| Thermal Pad | For attaching LED to LED heatsink | [Buy on Amazon](https://amzn.to/44JokMQ)             |
| Aluminum Extrusions | For housing all the components | [Buy on Amazon](https://amzn.to/44ATcAt)             |
| Aluminum Extrusions Connectors | For connecting the aluminum extrusions | [Buy on Amazon](https://amzn.to/44Uotxd)             |
---

## Construction

### Desiccator Drilling
- Drill **four holes** on the top of the desiccator to mount the LED heatsink (aligned with the heatsink's mounting pattern).
- Drill **one hole on the side** to route the LED wiring out of the chamber.
- Drill **one hole at the bottom** of the desiccator for the motor and ESC wiring.

> *This is the most challenging part of the build.*  
We sealed the holes with **silicone epoxy** (commercial caulk).  
Although we have designed a **3D-printable desiccator**, it is currently made with **PLA**, which is somewhat permeable and allows air into the chamber.  
We haven’t yet tested applying a sealant coating to improve airtightness.  
Let us know if you'd like access to the printable file.

### 3D Printed Parts > *Let us know if you need access to these. We'll gladly direct you to a link where you can modify and download these.*
- **Base Motor Mount**  
  Flat semi-circular part where the motor is screwed in. It rests directly inside the desiccator.
  
- **Motor-to-Chuck Connector**  
  Connects the motor to the chuck. This part screws directly onto the motor shaft.

- **Chuck**  
  Holds the devices to be spun. It fits onto the chuck connector.

- **Desiccator External Mounts**  
  Printed brackets that support the power supply, Arduino, and the upper mount where the desiccator sits. These parts integrate with a 20×20cm aluminum extrusion frame to form the external structure.

### LED and Mounting
- **Soldering**  
  Solder the wires to the LED and LED controller: `PWM`, `GND`, `+`, and `−` lines must be correctly connected.

- **Cable Routing**  
  Drill **two holes** into the LED mount bracket to allow LED wires to pass through.

- **Thermal Interface**  
  Place a **thermal pad** between the LED and heatsink to ensure proper heat transfer.

### Desiccator Painting
To reduce internal UV reflections, we recommend painting the desiccator **matte black**:

- Sand the surface lightly.
- Apply **matte black spray paint**.
- Let dry fully before use.

### Desiccator Mounting Frame
Assemble a 3D-printed mounting base and connect it to a **20×20×20 cm aluminum extrusion frame**. This serves as the structural housing for the desiccator system.

---
## Wiring Instructions 

### Arduino to ESC (Electronic Speed Controller)
- `Pin 6` (digital output) → ESC signal input  
- `5V` (from Arduino) → Red signal wire on ESC  
- `GND` → Black ground wire on ESC

### ESC to Power Supply
- `+12V` from power supply → ESC power input (`+12V`)  
- `GND` from power supply → ESC ground

### ESC to Motor
- Connect the **three output wires** from the ESC to the **three leads** of the brushless DC motor

### Arduino to LD24AJTA (LED Controller)
- `Pin 9` → Signal input of LD24AJTA  
- `GND` → GND on LD24AJTA

### LD24AJTA to Power Supply
- `+12V` from power supply → `+12V` input of LD24AJTA  
- `GND` from power supply → GND on LD24AJTA

## License

This project is licensed under the MIT License.

---

## Maintained By

**Guillermo Ramirez-Alvarado**  
GitHub: [github.com/Guermz](https://github.com/Guermz)  
Email: guillermo.ramirez@utsa.edu

Feel free to reach out! We also have 3D-printable parts for the desicurer that are not included in this repository, but we’re happy to share them and help you build your own.

Don’t hesitate to contact us with any questions or suggestions for future improvements. We’d love to hear your ideas!

