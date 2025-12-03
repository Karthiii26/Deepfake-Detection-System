@echo off
echo Starting Deepfake Detection System...
call tf_env\Scripts\activate
python hybrid_main.py
pause
