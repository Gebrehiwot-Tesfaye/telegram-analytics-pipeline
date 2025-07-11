import os
import json
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

def extract_message_id(img_path):
    basename = os.path.basename(img_path)
    msg_id = os.path.splitext(basename)[0]
    return msg_id

def detect_objects_in_images(media_dir, output_json, detected_dir="media/detected", max_images=20):
    results = []
    os.makedirs(detected_dir, exist_ok=True)
    detected_count = 0
    for root, _, files in os.walk(media_dir):
        for file in files:
            if detected_count >= max_images:
                break
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(root, file)
                # Skip missing/corrupt/empty files
                if not os.path.exists(img_path) or os.path.getsize(img_path) == 0:
                    continue
                try:
                    detections = model(img_path)
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")
                    continue
                for r in detections:
                    # Only save if there are detections
                    if len(r.boxes) > 0:
                        # Save annotated image with boxes, labels, and confidence scores
                        r.save(detected_dir)
                        subfolder = os.path.join(detected_dir, os.path.splitext(file)[0])
                        if os.path.exists(subfolder):
                            for f in os.listdir(subfolder):
                                src = os.path.join(subfolder, f)
                                dst = os.path.join(detected_dir, f"detected_{file}")
                                os.rename(src, dst)
                                print(f"Saved detected image: {dst}")
                            os.rmdir(subfolder)
                        detected_count += 1
                    # Collect detection metadata
                    for box in r.boxes:
                        results.append({
                            "message_id": extract_message_id(img_path),
                            "media_path": img_path,
                            "detected_object_class": model.names[int(box.cls)],
                            "confidence_score": float(box.conf)
                        })
        if detected_count >= max_images:
            break
    # Save detection results to JSON
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    detect_objects_in_images("media", "data/image_detections.json", detected_dir="media/detected", max_images=20)