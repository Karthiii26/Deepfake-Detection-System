import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from hybrid_predict import predict_hybrid

DATASET_DIR = "dataset2"  
# Assuming folder structure:
# dataset_folder/REAL/*.jpg
# dataset_folder/FAKE/*.jpg

image_paths = []
true_labels = []

for label in ["REAL", "FAKE"]:
    folder = os.path.join(DATASET_DIR, label)
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_paths.append(os.path.join(folder, filename))
            true_labels.append(label)

pred_labels = []
for path in image_paths:
    pred_label, conf = predict_hybrid(path)
    pred_labels.append(pred_label)

accuracy = accuracy_score(true_labels, pred_labels)
precision = precision_score(true_labels, pred_labels, pos_label="REAL")
recall = recall_score(true_labels, pred_labels, pos_label="REAL")
f1 = f1_score(true_labels, pred_labels, pos_label="REAL")
cm = confusion_matrix(true_labels, pred_labels)

print("\nEvaluation Results (Hybrid Ensemble Model):")
print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-Score : {f1:.4f}\n")

print("Confusion Matrix (rows=True, cols=Predicted):")
print(cm)

print("\nClassification Report:")
print(classification_report(true_labels, pred_labels))
