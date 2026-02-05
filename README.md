# Workout Progress Tracker

A Python-based desktop application designed to help you track your fitness journey. manage your weight, monitor weight lifting progress, and compare your cardio performance.

## Description

The Workout Progress Tracker is a user-friendly GUI application built with `tkinter`. It allows users to log various fitness activities and visualizes progress over time using `matplotlib`. Whether you are tracking your body weight, improving your lifts, or competitive cardio speeds, this tool provides the data/insights you need.

## Features

- **Personal Profile**: Simple login with your name to separate your data.
- **Weight Journey**:
  - Log your weight on a weekly basis.
  - Visualize your weight trends over time with a line graph.
- **Weight Lifting Tracker**:
  - Add custom exercises (e.g., Bench Press, Squats).
  - Log weight and repetitions for each session.
  - View progress charts displaying both weight and reps trends.
- **Cardio Tracker**:
  - Supports **Swimming**, **Running**, and **Cycling**.
  - Input distance and time to calculate your speed.
  - **Competitive Mode**: Compare your performance against simulated competitors using bar charts.
- **Data Management**:
  - All data is stored locally in an SQLite database (`workout_tracker.db`).
  - Option to clear all user data.

## Prerequisites

- **Python 3.x**
- **Tkinter**: Usually comes pre-installed with Python. On Linux, you might need to install it manually:
  ```bash
  sudo apt-get install python3-tk
  ```

## Installation

1.  **Clone the repository** (or download usage files):

    ```bash
    git clone git@github.com:athersaeed/Workout-Tracker-App.git
    cd Workout-Progress-Tracker
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Application**:

    ```bash
    python WT12_sqlite.py
    ```

2.  **Get Started**:
    - Enter your name on the welcome screen.
    - Choose an activity from the main menu:
      - **Weight Journey**: Add weekly inputs.
      - **Weight Lifting**: Create exercises and log sets.
      - **Cardio**: Select a type, enter stats, and "Compare" to see how you stack up.

## Project Structure

- `WT12_sqlite.py`: The main entry point and source code for the application.
- `requirements.txt`: List of Python libraries required (mainly `matplotlib`).
- `workout_tracker.db`: The SQLite database file (automatically created upon the first run).

## Technologies Used

- **Python**: Core programming language.
- **Tkinter**: Standard GUI framework.
- **SQLite**: Local database for data persistence.
- **Matplotlib**: Graph plotting library for visualizations.
