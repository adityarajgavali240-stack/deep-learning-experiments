#!/bin/bash

echo "Starting all 12 Deep Learning Experiments..."

# Array of experiment folders
folders=(
    "Experiment_01_ANN_Basics"
    "Experiment_02_MLP_Classification"
    "Experiment_03_CNN_Image_Classification"
    "Experiment_04_CNN_Facial_Emotion"
    "Experiment_05_Transfer_Learning_Emotion"
    "Experiment_06_RNN_Sentiment_Analysis"
    "Experiment_07_Image_Captioning"
    "Experiment_08_POS_Tagging"
    "Experiment_09_LSTM_Text_Generation"
    "Experiment_10_GRU_Sentiment"
    "Experiment_11_Attention_Case_Study"
    "Experiment_12_Transformers_Case_Study"
)

# Start each app in the background
for folder in "${folders[@]}"; do
    if [ -d "$folder" ]; then
        cd "$folder"
        echo "Starting $folder..."
        python app.py > /dev/null 2>&1 &
        cd ..
    fi
done

echo "All experiments have been started!"
echo "Access them at:"
echo "Experiment 01: http://localhost:5001"
echo "Experiment 02: http://localhost:5002"
echo "Experiment 03: http://localhost:5003"
echo "Experiment 04: http://localhost:5004"
echo "Experiment 05: http://localhost:5005"
echo "Experiment 06: http://localhost:5006"
echo "Experiment 07: http://localhost:5007"
echo "Experiment 08: http://localhost:5008"
echo "Experiment 09: http://localhost:5009"
echo "Experiment 10: http://localhost:5010"
echo "Experiment 11: http://localhost:5011"
echo "Experiment 12: http://localhost:5012"
