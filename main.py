import pyautogui
import time
import math
import pyscreeze


def filter_points(points, threshold=5):
    selected_points = []
    for point in points:
        x, y, _, _ = point  # Unpack the (left, top, width, height) tuple
        # Check if this point is far enough from all previously selected points
        if all(abs(x - px) > threshold or abs(y - py) > threshold for px, py, _, _ in selected_points):
            selected_points.append(point)
    return selected_points


def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def move_character(character_position, target_point):
    # Calculate the direction towards the target point
    dx = target_point[0] - character_position[0]
    dy = target_point[1] - character_position[1]

    # Calculate distance between character and target point
    dist = distance(character_position, target_point)

    # Adjust character position based on direction and distance
    duration = min(1, dist / 1500)  # Use longer duration for longer distances, max duration is 1 second

    if dx > 0:
        # Move right
        pyautogui.keyDown('d')
        time.sleep(duration)
        pyautogui.keyUp('d')
    elif dx < 0:
        # Move left
        pyautogui.keyDown('a')
        time.sleep(duration)
        pyautogui.keyUp('a')

    if dy > 0:
        # Move down
        pyautogui.keyDown('s')
        time.sleep(duration)
        pyautogui.keyUp('s')
    elif dy < 0:
        # Move up
        pyautogui.keyDown('w')
        time.sleep(duration)
        pyautogui.keyUp('w')


def click_cotton():
    character_position = (952, 600)

    stuck_counter = 0

    out_of_bounds_counter = 0

    current_distance = 0

    time.sleep(3)

    while True:
        try:
            if stuck_counter >= 3 or out_of_bounds_counter >= 350:
                pyautogui.press('t')
                time.sleep(5)

                pyautogui.keyDown('s')
                time.sleep(5.5)
                pyautogui.keyUp('s')

                pyautogui.keyDown('a')
                time.sleep(2.2)
                pyautogui.keyUp('a')

                pyautogui.keyDown('s')
                time.sleep(3)
                pyautogui.keyUp('s')

                pyautogui.keyDown('d')
                time.sleep(0.8)
                pyautogui.keyUp('d')

                pyautogui.keyDown('s')
                time.sleep(0.9)
                pyautogui.keyUp('s')

                pyautogui.keyDown('d')
                time.sleep(1.5)
                pyautogui.keyUp('d')
                print("YOU WERE STUCK!")
                print("Resetting counter to zero ...")
                stuck_counter = 0

            filtered_locations = filter_points(pyautogui.locateAllOnScreen(
                'cotton.png', confidence=0.6, grayscale=False))
            time.sleep(1)
            # Find the closest cotton point to the character
            closest_point = min(filtered_locations, key=lambda point: distance(character_position, point))

            # Move the character towards the closest cotton point
            move_character(character_position, closest_point)

            time.sleep(1)
            if current_distance == distance(character_position, closest_point):
                print("Adding to stuck counter")
                stuck_counter = stuck_counter + 1
            current_distance = distance(character_position, closest_point)
            if distance(character_position, closest_point) < 150:
                # Move the mouse cursor to the cotton location and click
                pyautogui.moveTo(character_position[0], character_position[1], duration=0.5)
                pyautogui.click()

                # Wait for 3 seconds
                time.sleep(3)
        except pyautogui.ImageNotFoundException:
            print("Exception triggered")
            filtered_locations.remove(closest_point)
            time.sleep(3)
        except pyscreeze.ImageNotFoundException:
            print("NO COTTON FOUND! WAITING!")
            out_of_bounds_counter = out_of_bounds_counter + 1
            time.sleep(3)
    exit()


click_cotton()
