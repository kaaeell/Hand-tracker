import cv2
import mediapipe as mp

# I'm using MediaPipe's hand solution — it gives us 21 landmarks per hand,
# which is more than enough to figure out which fingers are up.
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# These are the landmark IDs for each fingertip and the joint just below it (PIP).
# If the tip is higher on screen (smaller y) than the pip, the finger is extended.
TIPS = [8, 12, 16, 20]   # index, middle, ring, pinky
PIPS = [6, 10, 14, 18]


def count_fingers(landmarks, hand_label):
    """Return the number of fingers currently held up."""
    lm = landmarks.landmark
    count = 0

    # The thumb is trickier because it moves sideways instead of up/down.
    # We compare x-coordinates and flip the logic depending on which hand it is.
    if hand_label == "Right":
        if lm[4].x < lm[3].x:
            count += 1
    else:
        if lm[4].x > lm[3].x:
            count += 1

    # For the other four fingers, just check if the tip is above the pip joint.
    for tip, pip in zip(TIPS, PIPS):
        if lm[tip].y < lm[pip].y:
            count += 1

    return count


def draw_info(frame, finger_count, hand_label, cx, cy):
    """Draw a nice label near the center of the detected hand."""
    label = f"{hand_label}: {finger_count} finger{'s' if finger_count != 1 else ''}"

    # Draw a semi-transparent background pill so the text is readable on any background.
    (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
    pad = 10
    x1, y1 = cx - text_w // 2 - pad, cy - text_h - pad
    x2, y2 = cx + text_w // 2 + pad, cy + pad

    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (30, 30, 30), -1)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    cv2.putText(
        frame, label,
        (cx - text_w // 2, cy),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
        (255, 255, 255), 2, cv2.LINE_AA
    )


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Couldn't open the camera. Make sure it's connected and not in use.")
        return

    print("Hand tracker is running — press Q to quit.")

    with mp_hands.Hands(
        model_complexity=0,       # 0 = fast, 1 = more accurate
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Lost camera feed.")
                break

            # Flip horizontally so it feels like a mirror — way more natural to use.
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            # MediaPipe wants RGB, not BGR.
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb.flags.writeable = False
            results = hands.process(rgb)
            rgb.flags.writeable = True

            total = 0

            if results.multi_hand_landmarks:
                for hand_lm, hand_info in zip(
                    results.multi_hand_landmarks,
                    results.multi_handedness
                ):
                    # Draw the skeleton on the hand.
                    mp_draw.draw_landmarks(
                        frame, hand_lm, mp_hands.HAND_CONNECTIONS,
                        mp_draw.DrawingSpec(color=(0, 200, 255), thickness=2, circle_radius=4),
                        mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2),
                    )

                    # Figure out which hand this is and count the fingers.
                    label = hand_info.classification[0].label
                    count = count_fingers(hand_lm, label)
                    total += count

                    # Find the rough center of the hand (wrist landmark) to place the label.
                    wrist = hand_lm.landmark[0]
                    cx, cy = int(wrist.x * w), int(wrist.y * h) - 40
                    draw_info(frame, count, label, cx, cy)

            # Show the total finger count in the top-left corner.
            cv2.putText(
                frame, f"Total fingers: {total}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1,
                (0, 255, 150), 3, cv2.LINE_AA
            )

            # Subtle instruction reminder at the bottom.
            cv2.putText(
                frame, "Press Q to quit",
                (20, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (180, 180, 180), 1, cv2.LINE_AA
            )

            cv2.imshow("Hand Tracker", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    print("Done.")


if __name__ == "__main__":
    main()