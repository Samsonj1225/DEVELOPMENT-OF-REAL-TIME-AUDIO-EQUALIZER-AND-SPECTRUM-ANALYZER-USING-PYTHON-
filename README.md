## DEVELOPMENT OF REAL-TIME AUDIO EQUALIZER AND SPECTRUM ANALYZER USING PYTHON

This project is a real-time audio equalizer and spectrum analyzer with a graphical user interface built using Python. It records audio input, applies frequency-based equalization using FIR filters, displays the equalized audio spectrum, and plays back the processed sound with boosted volume.

### 1. Set Up the Python Environment

- Ensure Python is installed on your system.
- Install the required Python libraries:
  ```
  pip install numpy sounddevice scipy matplotlib
  ```
- Save the provided Python script (e.g., `main.py`).

### 2. Features of the Application

- Records real-time audio input.
- Applies a 5-band FIR filter equalizer to adjust frequency response.
- Displays a log-scaled spectrum analyzer plot.
- Plays back the equalized audio with volume boost.
- Interactive GUI built using `tkinter`.

### 3. Running the Application

- Open a terminal or IDE.
- Run the script:
  ```
  main.py
  ```
- A GUI window will open with the following buttons:
  - **Start Speaking**: Begins audio recording.
  - **Stop Speaking**: Ends the recording session.
  - **Show Equalized Audio Spectrum**: Displays the spectrum plot of the filtered audio.
  - **Play Equalized Audio**: Plays the enhanced audio through your speakers.

