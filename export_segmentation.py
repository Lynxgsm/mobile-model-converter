"""Segmentation model export utility for mobile platforms.

Usage examples:

- Export YOLOv8 segmentation weights to TFLite (FP16) and Core ML:
  python3 export_segmentation.py --model ./models/yolov8n-seg.pt --imgsz 320

- Export INT8 TFLite (requires dataset for calibration):
  python3 export_segmentation.py --model ./models/yolov8n-seg.pt --precision int8 --data path/to/data.yaml

Notes:
- Prefer FP16 (precision=fp16) for a balance of speed and quality on mobile.
- INT8 requires a proper representative dataset via --data.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export YOLO segmentation model to mobile formats"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="./models/detect_damage.pt",
        help="Path to segmentation model weights (*.pt)",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=320,
        help="Inference image size (square). Use the same size the model was trained on.",
    )
    parser.add_argument(
        "--precision",
        type=str,
        choices=["fp32", "fp16", "int8"],
        default="fp16",
        help="Numerical precision for export (TFLite uses this; Core ML uses fp16 flag)",
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Dataset YAML for INT8 calibration (required when --precision int8)",
    )
    parser.add_argument(
        "--export-tflite",
        action="store_true",
        help="Export TFLite model",
    )
    parser.add_argument(
        "--export-coreml",
        action="store_true",
        help="Export Core ML model",
    )
    parser.add_argument(
        "--nms",
        action="store_true",
        default=True,
        help="Enable NMS during Core ML export",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Force CPU for export",
    )

    args = parser.parse_args()

    # Default to exporting both if neither explicitly requested
    if not args.export_tflite and not args.export_coreml:
        args.export_tflite = True
        args.export_coreml = True

    return args


def determine_precision_flags(precision: str) -> tuple[bool, bool]:
    is_half_precision = precision == "fp16"
    is_int8_precision = precision == "int8"
    return is_half_precision, is_int8_precision


def export_segmentation_model(
    model_path: str,
    imgsz: int,
    precision: str,
    data_yaml: Optional[str],
    export_tflite: bool,
    export_coreml: bool,
    nms: bool,
    force_cpu: bool,
) -> None:
    half, int8 = determine_precision_flags(precision)

    if int8 and not data_yaml:
        print(
            "[error] --precision int8 requires --data path to a dataset YAML for calibration."
        )
        sys.exit(1)

    if imgsz % 32 != 0:
        print(
            f"[warning] imgsz {imgsz} is not a multiple of 32. Consider using a multiple of 32 (e.g., 320, 640)."
        )

    print(f"Loading segmentation model from {model_path} ...")
    model = YOLO(model_path)
    if force_cpu:
        model = model.to("cpu")

    if export_tflite:
        print("Exporting model for Android (TFLite)...")
        export_kwargs = {
            "model": model_path,
            "format": "tflite",
            "imgsz": imgsz,
            "half": half,
            "int8": int8,
        }
        if int8 and data_yaml:
            export_kwargs["data"] = data_yaml

        model.export(**export_kwargs)
        print("TFLite export completed.")

    if export_coreml:
        print("Exporting model for iOS (Core ML)...")
        model.export(
            model=model_path,
            format="mlmodel",
            imgsz=imgsz,
            half=half,
            nms=nms,
        )
        print("Core ML export completed.")


def main() -> None:
    args = parse_args()
    export_segmentation_model(
        model_path=args.model,
        imgsz=args.imgsz,
        precision=args.precision,
        data_yaml=args.data,
        export_tflite=args.export_tflite,
        export_coreml=args.export_coreml,
        nms=args.nms,
        force_cpu=args.cpu,
    )


if __name__ == "__main__":
    main()
