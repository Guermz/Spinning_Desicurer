# Spinning Desicurer Controller - Help & Guide

These scripts were developed to control an upgraded version of the Spinning Desicurer, originally described in the publication:
"Spinning Desicurer: A Cost-Effective and Generalizable Post-Processing Method for Enhanced Optical Quality in 3D-Printed Microfluidics"
Published in MRS Communications, 2024. (https://link.springer.com/article/10.1557/s43579-024-00594-9)

The hardware has since been enhanced with a brushless DC motor to enable smoother and more consistent layer formation.

This GUI application is designed to control your own Spinning Desicurer for timed motor and UV LED operations using an Arduino. It allows for automated curing sequences useful in microfabrication, polymerization, or lab prototyping tasks.

---

## 🚀 Features

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

## 🧾 How to Use

1. Connect your Arduino and open the app.
2. Select or modify your desired durations and motor speed.
3. Click **Step 1** or **Step 2** to run an automated curing sequence.
4. Use **STOP** to cancel at any time.
5. Use the **Custom Command** box for manual control.

---

## 🧰 Required Hardware

| Component         | Description                             | Link                            |
|------------------|-----------------------------------------|---------------------------------|
| Arduino Uno      | Central Microcontroller | [Buy on Amazon](https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6/ref=sr_1_5?crid=28YRPWR3AXFE0&dib=eyJ2IjoiMSJ9.VZl_WiFg-4H_p0-BXr9pa0HoKSbb-SFea21hVZZ6cALU8pwAELbygBcjFL03D8MMjRtwqyz59Jvp4YYmEdUap3MpKeozJvDxvwig6L2iVhVXsriMFErl9ETMgpmSO-ahf6IrtGsRTevHpcYVJShXXmi6A4qOGW9q3ZWwIVUPviCdzaYyR0JX0N8edYo_liEQlyRgPFWuNkwM-dGEaxXo5pxmemN8F0KNog--RsqUtbQ.78hK3veeR6hJv7zEipbFKVC3KxY1hRzStcLQebcx2tk&dib_tag=se&keywords=arduino&qid=1747169415&sprefix=arduino+uno%2Caps%2C302&sr=8-5)             |
| UV LED           | For photopolymerization curing         | [Buy on Amazon](https://www.amazon.com/Chanzon-Ultraviolet-Emitter-Components-Lighting/dp/B01DBZK2C6?th=1)             |
| ESC (Electronic Speed Controller) | Controls brushless motor       | [Buy on Amazon](https://www.amazon.com/RC-Brushless-Electric-Controller-bullet/dp/B0754H7XZZ/ref=sr_1_8?crid=SARKJWAQ9XVZ&dib=eyJ2IjoiMSJ9.Li96wegYvrs7mtYR8L0iICDO5JP0YEMfBC20ueTgDGn5Qrbxqm6M3NYRAWXMZ7RAxehmZUTbfJPNKaybZGmtcuZZMuyrPsp-jooFE6lO_KpIxnGU746vGZOUvcpUFtdvLnPFL8sPsnn4v_wlzPVZ8Lj0Wkw31rlliG9idndn_2Tv2U1lEZHWM7mKWnQaJAYzrcA0ggcBsFUJEwWAF-HaOT1KvIBdl0tcmGClWsdZunQPzXG-JwI3hx2nDh8bAK3BOFgXRIU3A-T38pGOojfXVwb6Ves7_Xmidp3QFoy6Nh236NjvJM8YcC1ITFq3mgmoX6kwZ9-Y3d1SQ8rNIw77MoeEyxRsRlFKrVLDOhSpqR9l1VU3-xh6yZrqh4UrIE9T2Z43BU4pJrhLyuzsTapYe46jBRmzlmEmfTHf7n7sbr3ueRxS2_qkdtw-5l4xDQ4f.4uH1uNzvZOuYMWVUr1DTc2slQ4TrFTgDHD-G8wAtcjo&dib_tag=se&keywords=electronic%2Bspeed%2Bcontroller%2Bbrushless%2Bmotor&qid=1743444372&sprefix=electronic%2Bspeed%2Bcontroller%2Bbrushless%2Bmotor%2Caps%2C300&sr=8-8&th=1)             |
| Brushless DC Motor | Drives the spinning platform           | [Buy on Amazon](https://www.amazon.com/dp/B0841TWF7N/?coliid=I2BD8XCIV34OAP&colid=YT4QZJ7KA01P&ref_=list_c_wl_lv_ov_lig_dp_it&th=1)             |
| Power Supply (12V) | Powers motor and LED          | [Buy on Amazon](https://www.amazon.com/BOSYTRO-Converter-Switching-Electronic-Instruments/dp/B0DJQT5MB9/ref=sr_1_3?crid=3V6433N3CGGV1&dib=eyJ2IjoiMSJ9.F6tb4Ttf-JNKrwLe6btLkkMSQUbBT9c53bL0_n0sO7vq2H3s5pXDK-74I7mqGaDuXrkVkF63cWDoAOVT6HfqjkeMXf5gkYa81xUP1NvWcfJtq5scpF2zMcXKFp7elfdrmcqr2xDyKh-UrBllPcrNqtzQwzMvTyTfV4MoZkjPcPPXu8-LRt-oimWB_Am9KdwGCuMU9NTpEYEwUlzRKo_vgbtRMrl37xs33PMB86j7_Rg.L-_cWpO140QQmVQbqeRlRVcUewc-qIbbFJX7WW1IMt8&dib_tag=se&keywords=power%2Bsupply%2B40A&qid=1743186990&sprefix=power%2Bsupply%2B40a%2Caps%2C147&sr=8-3&th=1)             |
| LED Controller     | Microntroller to control LED           |[Buy on Amazon](https://www.amazon.com/dp/B08T9JJW6Y?ref=ppx_yo2ov_dt_b_fed_asin_title)             |
| Dessicator | For housing UV led and motor | [Buy on Amazon](https://www.amazon.com/Bel-Art-Polycarbonate-Desiccator-Polypropylene-F42020-0000/dp/B002VBW9RS/ref=sr_1_5?crid=PBMCREC7RRU8&dib=eyJ2IjoiMSJ9.iqb1nQx9tdvalGNQpwYILNzb5Se0UqYZvOLdoLveOnJDIfeqIIz7GMO1oah5vCMVf8f88eUK7MeuNWVyFJJB1GnIJDdjem78BFcvYw_psaucFqk0lm6GOWIssqhsJIhSt8CDqBMb0VLihxMxqyGVqnuHSAFF0Et4ko0nVVSg0C8imnI6AoKkOOTjnzoP-zG7r4BxRi9h35wCe84qOLvk_8vh81RhMCrjRWO7pq9Rc24.q8-ptPEVycTNPJxpRL0HcImCTo7V7SFc3eOKkl2u6dg&dib_tag=se&keywords=dessicator&qid=1747169595&sprefix=dessicat%2Caps%2C230&sr=8-5&ufe=app_do%3Aamzn1.fos.9fe8cbfa-bf43-43d1-a707-3f4e65a4b666&th=1)             |

---

## 📜 License

This project is licensed under the MIT License.

---

## 🧑‍💻 Maintained By

**Guillermo Ramirez-Alvarado**  
GitHub: [github.com/Guermz](https://github.com/Guermz)  
Email: guillermo.ramirez@utsa.edu

Feel free to reach out! We also have 3D-printable parts for the desicurer that are not included in this repository, but we’re happy to share them and help you build your own.

Don’t hesitate to contact us with any questions or suggestions for future improvements. We’d love to hear your ideas!

