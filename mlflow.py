import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")  # Change if using a remote server
mlflow.set_experiment("Serial Number OCR")

with mlflow.start_run():
    mlflow.log_param("preprocessing", "Threshold + GaussianBlur")
    mlflow.log_param("OCR Engine", "Tesseract")
    mlflow.log_metric("accuracy", 0.85)  # Replace with actual accuracy
    mlflow.log_artifact("sample_image.jpg")  # Log a sample input image
