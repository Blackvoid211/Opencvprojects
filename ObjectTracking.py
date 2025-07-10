import cv2
import sys
import os

def select_tracker(tracker_type):
    if tracker_type == 'BOOSTING':
        return cv2.legacy.TrackerBoosting_create()
    elif tracker_type == 'MIL':
        return cv2.legacy.TrackerMIL_create()
    elif tracker_type == 'KCF':
        return cv2.legacy.TrackerKCF_create()
    elif tracker_type == 'TLD':
        return cv2.legacy.TrackerTLD_create()
    elif tracker_type == 'MEDIANFLOW':
        return cv2.legacy.TrackerMedianFlow_create()
    elif tracker_type == 'MOSSE':
        return cv2.legacy.TrackerMOSSE_create()
    elif tracker_type == 'CSRT':
        return cv2.legacy.TrackerCSRT_create()
    else:
        raise ValueError('Unknown tracker type')

def main():
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
    print('Select tracker')
    for i, tracker_type in enumerate(tracker_types, start=1):
        print(f'{i}) {tracker_type}')

    tracker_choice = int(input('Enter tracker choice: ')) - 1
    if tracker_choice < 0 or tracker_choice >= len(tracker_types):
        print('Invalid tracker choice')
        sys.exit()

    tracker_type = tracker_types[tracker_choice]
    tracker = select_tracker(tracker_type)

    video_path = input('Enter video path (leave blank for webcam): ')

    if not video_path:
        video = cv2.VideoCapture(0)
    else:
        if not os.path.isfile(video_path):
            print(f'File not found: {video_path}')
            sys.exit()

        video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print(f'Could not open video file: {video_path}')
        sys.exit()

    ok, frame = video.read()
    if not ok or frame is None:
        print('Could not read video file')
        sys.exit()

    bbox = cv2.selectROI(frame, False)
    ok = tracker.init(frame, bbox)

    while True:
        ok, frame = video.read()
        if not ok or frame is None:
            print('Failed to read frame')
            break

        ok, bbox = tracker.update(frame)

        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.putText(frame, "ESC to quit", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        cv2.imshow('Tracking', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()




