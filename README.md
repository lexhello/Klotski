# Klotski Slide Puzzle Solver (Build18 Hackathon Project)

## Overview
This project implements a xyz gantry-style mechanical system capable of autonomously solving a 4×4 Taquin/Klotski sliding block puzzle after we put in the initial state. Designed and built for the Build18 Hackathon, the system uses stepper-motor motion control paired with Raspberry Pi-based logic and host-side coordination.

## Hardware Specifications
* Stepper Motors: NEMA17
* Motor Drivers: A4988
* Compute: Raspberry Pi 4
* Mechanical System: XY gantry for precise tile manipulation

## Software Stack
* Python control scripts
* Gantry control + puzzle-solving logic
* Laptop interface for commands/logging

## How to Run
* main.py runs on pi
* laptop_main.py runs on laptop
