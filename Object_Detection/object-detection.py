import cv2
import torch
from ultralytics import YOLO

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def main():

    # Load YOLOv9 model
    model = YOLO('yolov9c.pt')
    model.to(device)
    
    # Initialize video capture (0 for default camera)
    cap = cv2.VideoCapture(0)
    
    # Check if the video capture device is opened
    if not cap.isOpened():
        print("Error: Could not open video capture device")
        return
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Use YOLOv9 model to make predictions
        results = model(frame)
        
        # Process the results
        for result in results:
            # Loop through each detected object
            for box in result.boxes:
                # Get coordinates and class label
                x1, y1, x2, y2 = box.xyxy[0]
                label_id = int(box.cls[0].item())
                confidence = box.conf[0].item()
                
                # Get the class label from YOLO model
                class_label = model.names[label_id]
                
                # Create the label text
                label_text = f"{class_label}: {confidence:.2f}"
                
                # Draw bounding box on the frame
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Draw the label text on the frame above the bounding box
                cv2.putText(frame, label_text, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Display the frame with bounding boxes and labels
        cv2.imshow('Real-Time Object Detection', frame)
        
        # Exit the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
