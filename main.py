import cv2
import numpy as np
import os
import keyboard

clear = lambda: os.system('cls')
density = '@#$8B9AYC301!=+-_,.    '
density2 = '9876543210 '


def get_brightness(pixel):
    return sum(pixel) / 3


def density_char(brightness):
    vals = np.linspace(0, 255, len(density) + 1)
    for i in range(1, len(density) + 1):
        if brightness <= vals[i]:
            return density[-i]


def compare_pixels(pixel1, pixel2, max_diff, tracking=False):
    for i in range(3):
        if abs(max(pixel1[i], pixel2[i]) - min(pixel1[i],
                                               pixel2[i])) > max_diff:  # ZMIANA W ABS MIN MAX !!!!!!!!!!!!!!!!!!!!
            if tracking:
                print(f'comparing {pixel1} =/= {[pixel2]}')
            return False

    if tracking:
        print(f'comparing {pixel1} = {pixel2}')
    return True


def to_ascii(frame, frame_prev):
    image_ascii = ''
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            image_ascii += density_char(get_brightness(frame[i][j])) \
                if not compare_pixels(frame[i][j], frame_prev[i][j], 20) else ' '
        image_ascii += '\n'
    clear()
    print(image_ascii)
    # print(len(frame), 'x', len(frame[0]), frame.shape)


def remember_background(cap, n=1):
    frames = []
    for i in range(n):
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.1, fy=0.07, interpolation=cv2.INTER_LINEAR)
        frames.append(frame)

    return np.float32(np.mean(frames, 0))


def update_background(cap, background):
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.1, fy=0.07, interpolation=cv2.INTER_LINEAR)

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    if frame is None:
        return background

    cv2.accumulateWeighted(frame, background, 0.005)
    result = cv2.convertScaleAbs(background)
    cv2.imshow('result', result)
    return background

if __name__ == '__main__':
    remove_background = False
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    if remove_background:
        background = remember_background(cap)

    frame_prev = np.zeros([34, 64, 3])
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.1, fy=0.07, interpolation=cv2.INTER_LINEAR)
        to_ascii(frame, background) if remove_background else to_ascii(frame, frame_prev)

        frame = cv2.resize(frame, None, fx=1/0.1, fy=1/0.07, interpolation=cv2.INTER_LINEAR)
        cv2.imshow('Input', frame)
        # cv2.imshow('Input', frame)
        # frame_prev = frame

        if remove_background:
            if keyboard.is_pressed(' '):
                background = remember_background(cap)
            background = update_background(cap, background)

        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
