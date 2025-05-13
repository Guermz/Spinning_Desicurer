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
| Arduino Uno      | Central Microcontroller | [Buy on Amazon](https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/ref=sr_1_5?crid=28YRPWR3AXFE0&dib=eyJ2IjoiMSJ9.VZl_WiFg-4H_p0-BXr9pa0HoKSbb-SFea21hVZZ6cALU8pwAELbygBcjFL03D8MMjRtwqyz59Jvp4YYmEdUap3MpKeozJvDxvwig6L2iVhVXsriMFErl9ETMgpmSO-ahf6IrtGsRTevHpcYVJShXXmi6A4qOGW9q3ZWwIVUPviCdzaYyR0JX0N8edYo_liEQlyRgPFWuNkwM-dGEaxXo5pxmemN8F0KNog--RsqUtbQ.78hK3veeR6hJv7zEipbFKVC3KxY1hRzStcLQebcx2tk&dib_tag=se&keywords=arduino&qid=1747169415&sprefix=arduino+uno%2Caps%2C302&sr=8-5)             |
| UV LED           | For photopolymerization curing         | [Buy on Amazon](https://www.amazon.com/Chanzon-Ultraviolet-Emitter-Components-Lighting/dp/B01DBZK2C6?th=1)             |
| ESC (Electronic Speed Controller) | Controls brushless motor       | [Buy on Amazon](https://www.amazon.com/RC-Brushless-Electric-Controller-bullet/dp/B0754H7XZZ/ref=sr_1_8?crid=SARKJWAQ9XVZ&dib=eyJ2IjoiMSJ9.Li96wegYvrs7mtYR8L0iICDO5JP0YEMfBC20ueTgDGn5Qrbxqm6M3NYRAWXMZ7RAxehmZUTbfJPNKaybZGmtcuZZMuyrPsp-jooFE6lO_KpIxnGU746vGZOUvcpUFtdvLnPFL8sPsnn4v_wlzPVZ8Lj0Wkw31rlliG9idndn_2Tv2U1lEZHWM7mKWnQaJAYzrcA0ggcBsFUJEwWAF-HaOT1KvIBdl0tcmGClWsdZunQPzXG-JwI3hx2nDh8bAK3BOFgXRIU3A-T38pGOojfXVwb6Ves7_Xmidp3QFoy6Nh236NjvJM8YcC1ITFq3mgmoX6kwZ9-Y3d1SQ8rNIw77MoeEyxRsRlFKrVLDOhSpqR9l1VU3-xh6yZrqh4UrIE9T2Z43BU4pJrhLyuzsTapYe46jBRmzlmEmfTHf7n7sbr3ueRxS2_qkdtw-5l4xDQ4f.4uH1uNzvZOuYMWVUr1DTc2slQ4TrFTgDHD-G8wAtcjo&dib_tag=se&keywords=electronic%2Bspeed%2Bcontroller%2Bbrushless%2Bmotor&qid=1743444372&sprefix=electronic%2Bspeed%2Bcontroller%2Bbrushless%2Bmotor%2Caps%2C300&sr=8-8&th=1)             |
| Brushless DC Motor | Drives the spinning platform           | [Buy on Amazon](https://www.amazon.com/dp/B0841TWF7N/?coliid=I2BD8XCIV34OAP&colid=YT4QZJ7KA01P&ref_=list_c_wl_lv_ov_lig_dp_it&th=1)             |
| Power Supply (12V) | Powers motor and LED          | [Buy on Amazon](https://www.amazon.com/BOSYTRO-Converter-Switching-Electronic-Instruments/dp/B0DJQT5MB9/ref=sr_1_3?crid=3V6433N3CGGV1&dib=eyJ2IjoiMSJ9.F6tb4Ttf-JNKrwLe6btLkkMSQUbBT9c53bL0_n0sO7vq2H3s5pXDK-74I7mqGaDuXrkVkF63cWDoAOVT6HfqjkeMXf5gkYa81xUP1NvWcfJtq5scpF2zMcXKFp7elfdrmcqr2xDyKh-UrBllPcrNqtzQwzMvTyTfV4MoZkjPcPPXu8-LRt-oimWB_Am9KdwGCuMU9NTpEYEwUlzRKo_vgbtRMrl37xs33PMB86j7_Rg.L-_cWpO140QQmVQbqeRlRVcUewc-qIbbFJX7WW1IMt8&dib_tag=se&keywords=power%2Bsupply%2B40A&qid=1743186990&sprefix=power%2Bsupply%2B40a%2Caps%2C147&sr=8-3&th=1)             |
| LED Controller     | Microntroller to control LED           |[Buy on Amazon](https://www.amazon.com/dp/B08T9JJW6Y?ref=ppx_yo2ov_dt_b_fed_asin_title)             |
| Dessicator | For housing UV led and motor | [Buy on Amazon](https://www.amazon.com/Bel-Art-Polycarbonate-Desiccator-Polypropylene-F42020-0000/dp/B002VBW9RS/ref=sr_1_5?crid=PBMCREC7RRU8&dib=eyJ2IjoiMSJ9.iqb1nQx9tdvalGNQpwYILNzb5Se0UqYZvOLdoLveOnJDIfeqIIz7GMO1oah5vCMVf8f88eUK7MeuNWVyFJJB1GnIJDdjem78BFcvYw_psaucFqk0lm6GOWIssqhsJIhSt8CDqBMb0VLihxMxqyGVqnuHSAFF0Et4ko0nVVSg0C8imnI6AoKkOOTjnzoP-zG7r4BxRi9h35wCe84qOLvk_8vh81RhMCrjRWO7pq9Rc24.q8-ptPEVycTNPJxpRL0HcImCTo7V7SFc3eOKkl2u6dg&dib_tag=se&keywords=dessicator&qid=1747169595&sprefix=dessicat%2Caps%2C230&sr=8-5&ufe=app_do%3Aamzn1.fos.9fe8cbfa-bf43-43d1-a707-3f4e65a4b666&th=1)             |
| LED Heatsink + Mount | For mounting LED to dessicator | [Buy on Amazon](https://www.amazon.com/dp/B01D1LD68C?ref=nb_sb_ss_w_as-reorder_k0_1_10&amp=&crid=N1WFROHUK8G7&sprefix=led%2Bheatsi&th=1)             |
| Thermal Pad | For attaching LED to LED heatsink | [Buy on Amazon](https://www.amazon.com/OwlTree-100x100mm-Efficient-Conductivity-Resistant/dp/B096ZNHY8F/ref=sr_1_5?crid=1E5BKWSNEWX0X&dib=eyJ2IjoiMSJ9.mdPgm-FFvpUYc_rr3U4C0Ayaqb-PCSDqblBpTRXwboqnR4IPPXCthKeCIKmInbS7fef-73_n4n7YzVXtgX6NvSW8pQswNQoUpPJYhYSCnl-xjyg7luyfIBKrIaWvpYua-bimqTXSK5PSBbjMHtmWt4-NgG3r-LIa_Ek6c_YXhga8q2dUDSp-3Wp3KxiNf7hk6pvkyjc_oKjTVBcfb0KTMRh_VnHXZicdToNe7k6FOrQ.eD670ZSzBJDlRERlFathMUrrwK5pwERuj5I4TBioHQM&dib_tag=se&keywords=heatsink+pad&qid=1747175032&sprefix=heatsink+p%2Caps%2C202&sr=8-5)             |
| Aluminum Extrusions | For housing all the components | [Buy on Amazon](https://www.amazon.com/Aluminum-Extrusion-European-Standard-15-75inch/dp/B08Y8KL79L/ref=sr_1_3?crid=21AXSCVJG02NQ&dib=eyJ2IjoiMSJ9.QyOECFPgVQVIJLjAoNrzLaH-8VL_FiokMhVRW42y_YDU47wQ2_ITQSjK_M5ZpxU0BB5oSbFM56MOpK23WwkRGYzwoV25J_1qww-b1NeQmsXWByDdlVoYQPB5057bQo_Jnl7tQ3BUugr_uDzkrbbxB_SwhRf8iKZEg57xLgJ-4VpKsecK0CIA2XYrLk20BeAM26bdaIq1QPVjqETS4cZTMepMWG6EEd1-v3bSs2wMtzM.YuzykN2blma0ZeqIPkFTLGmjWuwa-Z6bU7SXRGb-1aI&dib_tag=se&keywords=aluminum%2Bprofiles&qid=1747175435&sprefix=aluminum%2Bprofile%2Caps%2C250&sr=8-3&th=1)             |
| Aluminum Extrusions Connectors | For connecting the aluminum extrusions | [Buy on Amazon](https://www.amazon.com/Aluminum-Profile-Connector-Bracket-Accessories/dp/B0855CRFWQ/ref=sr_1_3?crid=1M4JIDNFN66P6&dib=eyJ2IjoiMSJ9.fqBDxpk7OAag-vtNHC7naDkUbDRoS9lBbP7xwE0-TMRlmkIhBVhTWhPVQkVMG2HyFmPyqNAlooweTM8IdqsL7J8hOZURrQvBxELa1G_oh5F8OQEzjlqLT_Lk5HLpBQDJjKtlMKqdrjNCG8ussepXgAclAwH1Us2JIZtoyj8XnTG4XftueJ0DJW305XIcW0Ef1ojPiEIX_9eETCqaUmAuzoepfSGINhT_x4sRmnCoD-o.QOXEORLndaplrsAdSpyIc_aVAQAeE8M5eDzAyv_rO2I&dib_tag=se&keywords=aluminum%2Bprofiles%2Bconnectors&qid=1747175501&sprefix=aluminum%2Bprofiles%2Bconnecto%2Caps%2C247&sr=8-3&th=1)             |
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

