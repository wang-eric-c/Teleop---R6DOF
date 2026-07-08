import time
import cv2

import config
from tracking import HandTracker
from mapping import hand_to_pose, detect_pinch, is_engaged
from filters import OneEuroFilter
from sim_backend import SimBackend
# from serial_backend import SerialBackend


def main():
    tracker = HandTracker()
    arm = SimBackend(gui=True)          # <- swap to SerialBackend() later
    pose_filter = OneEuroFilter()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            landmarks = tracker.detect(frame)

            if landmarks is not None:
                tracker.draw(frame, landmarks)

                target = hand_to_pose(landmarks)
                pinch = detect_pinch(landmarks)
                engaged = is_engaged(landmarks)

                target = pose_filter(target, time.time())

                if engaged:
                    arm.move_to_pose(target)
                    arm.set_gripper(pinch)

                status = "ENGAGED" if engaged else "clutch"
                cv2.putText(frame, f"{status}  pinch={pinch}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0, 255, 0) if engaged else (0, 0, 255), 2)
            

            arm.step()

            cv2.imshow("teleop (q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        arm.close()


if __name__ == "__main__":
    main()