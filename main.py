import platform

from ultralytics import YOLO

model_path = "./models/detect-element.pt"
model = YOLO(model_path).to("cpu")

try:
    print("Exporting model for Android (TFLite)...")
    model.export(
        model=model_path,
        format="tflite",
        imgsz=320,
        int8=True,
        half=True,
    )
    print("Android export completed.")

    # Export for iOS (Core ML)
    if platform.system() != "Darwin":
        print(
            "Skipping Core ML export: requires macOS host (not supported inside Linux Docker)."
        )
    else:
        print("Exporting model for iOS (Core ML)...")
        model.export(
            format="coreml",
            imgsz=320,
            half=True,  # Half precision
            nms=True,  # Non-maximum suppression
        )
        print("iOS export completed.")
    # Visualize results
    # model.plot()
except Exception as e:
    print("Error during export:", e)
