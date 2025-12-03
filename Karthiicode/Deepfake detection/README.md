# Deepfake Detection System

This project implements a deepfake detection system using a hybrid model (Custom CNN + ResNet50).

## Requirements

*   Python 3.x
*   See `requirements.txt` for dependencies.

## Installation

1.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, simply execute the batch file:

```bash
run_app.bat
```

Or run the Python script directly:

```bash
python hybrid_main.py
```

## Files

*   `hybrid_main.py`: Main application entry point.
*   `deepfake_model.h5`: Trained custom model.
*   `deepfake_resnet50.h5`: Trained ResNet50 model.
*   `evaluation.py`: Evaluation scripts.
*   `hybrid_preprocess.py`: Preprocessing utilities.
*   `hybrid_predict.py`: Prediction logic for the hybrid model.
