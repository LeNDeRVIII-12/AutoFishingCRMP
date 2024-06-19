import numpy as np
import cv2
import pyautogui
from PIL import ImageGrab
import keyboard
import time
import tkinter as tk

# Константы и настройки
THRESHOLD = 0.8
PEREBOR = False

# Словари изображений и действий
images_and_actions = {
    'assets/S.png': 'S',
    'assets/SHIFT.png': 'shift',
    'assets/V.png': 'V',
    'assets/W.png': 'W',
    'assets/D.png': 'D',
    'assets/CTRL.png': 'ctrl',
    'assets/C.png': 'C',
    'assets/SPACE.png': 'space',
}

fish = {
    'assets/RedFish1.png': 'red',
    'assets/WhiteFish1.png': 'white',
}

# Получение размеров экрана
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# Параметры областей захвата экрана
correct_width_fish1 = width // 2.0966
correct_width_fish2 = width // 1.9277
correct_height_fish1 = height // 1.176
correct_height_fish2 = height // 1.0746

correct_width_key1 = width // 2.0628
correct_width_key2 = width // 1.90902
correct_height_key1 = height // 1.23393
correct_height_key2 = height // 1.2050209


def take_screenshot(bbox):
    screenshot = np.array(ImageGrab.grab(bbox=bbox))
    return cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)


def find_template(screenshot, template_path, threshold=THRESHOLD):
    template = cv2.imread(template_path, 0)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc, template.shape if max_val >= threshold else None


def execute_action(action):
    actions = {
        'S': lambda: pyautogui.press('s'),
        'shift': lambda: keyboard.press_and_release('shift'),
        'V': lambda: pyautogui.press('v'),
        'W': lambda: pyautogui.press('w'),
        'D': lambda: pyautogui.press('d'),
        'ctrl': lambda: keyboard.press_and_release('ctrl'),
        'C': lambda: pyautogui.press('c'),
        'space': lambda: pyautogui.press('space')
    }
    actions.get(action, lambda: None)()


def process_key_templates(screenshot):
    for template_path, action in images_and_actions.items():
        max_val, max_loc, shape = find_template(screenshot, template_path)
        if shape:
            h, w = shape
            cv2.rectangle(screenshot, max_loc, (max_loc[0] + w, max_loc[1] + h), 255, 5)
            execute_action(action)
            print(f"Found {template_path}: {action}")


def process_fish_templates(screenshot):
    for template_path, action in fish.items():
        max_val, max_loc, shape = find_template(screenshot, template_path)
        if shape:
            h, w = shape
            cv2.rectangle(screenshot, max_loc, (max_loc[0] + w, max_loc[1] + h), 255, 5)
            print(f"Found {template_path}: {action}")
            process_key_templates(screenshot_key)


# Основной цикл
while True:
    screenshot_fish = take_screenshot(
        (correct_width_fish1, correct_height_fish1, correct_width_fish2, correct_height_fish2))
    screenshot_key = take_screenshot((correct_width_key1, correct_height_key1, correct_width_key2, correct_height_key2))

    process_fish_templates(screenshot_fish)

    screenshot = take_screenshot((956, 1271, 1616, 1324))
    max_val, max_loc, shape = find_template(screenshot, 'assets/OVER.png', threshold=0.6)
    if shape:
        h, w = shape
        cv2.rectangle(screenshot, max_loc, (max_loc[0] + w, max_loc[1] + h), 255, 5)
        print("Found OVER")
        pyautogui.press('e')

        # Обработка инвентаря и перемещение предметов
        # (далее следует аналогичный код для работы с инвентарем и перемещением предметов)

        # Завершение текущей рыбалки и начало новой
        pyautogui.press('esc')
        pyautogui.press('t')
        pyautogui.write('/fish')
        pyautogui.press('enter')
        pyautogui.press('enter')

    cv2.imshow('Fish Capture', screenshot_fish)
    cv2.imshow('Key Capture', screenshot_key)
    cv2.imshow('Over Check', screenshot)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
