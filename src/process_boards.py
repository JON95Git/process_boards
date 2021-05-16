import re
import numpy
import pytesseract
from src import open_cv as cv
from matplotlib import pyplot
import math
from PIL import Image
import time
from src import utils

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

boards_paths = [
    'images/boards/board01.jpg',
    'images/boards/board02.jpg',
    'images/boards/board03.jpg',
    'images/boards/board04.jpg',
    'images/boards/board05.jpg',
    'images/boards/board06.jpg',
    'images/boards/board07.jpg',
    'images/boards/board08.jpg',
    'images/boards/board09.jpg',
    'images/boards/board10.jpg',
]

image_path = []
image_model = []


def print_init_message():
    print('Process initialized')


def get_custom_config():
    return r'-c tessedit_char_whitelist=ABC012 --psm 3'


def _loades_images(image_index):
    original = cv.loades_image(boards_paths[image_index], 1)
    backup = cv.loades_image(boards_paths[image_index], 1)
    image = cv.loades_image(boards_paths[image_index], 0)
    return original, backup, image


def _prepare_image_analyzer(image):
    (height, width) = image.shape[:2]
    ret, image_t = cv.threshold(image)
    return height, width, image_t


def _test_in_loop(height, width, image_t):
    p1 = 0
    xi = width
    inc = 0
    for y in range(0, height, 1):
        for x in range(0, width, 1):
            color = image_t[y, x]
            if color != 255 and (p1 == 0):
                dot1 = (x, y)
                xi = x
                p1 = 1
                if x > (width/2):
                    inc = 1
            if (p1 == 1) and (inc == 1) and (color != 255) and (x < xi):
                dot2 = (x, y)
                xi = x
            if (p1 == 1) and (inc == 0) and (color != 255) and (x > xi):
                dot2 = (x, y)
                xi = x
    return inc, dot1, dot2


def _circle_images(original, dot1, dot2):
    cv.circle(original, dot1)
    cv.circle(original, dot2)


def _apply_math(inc, dot1, dot2):
    angle = math.atan2(dot1[1] - dot2[1], dot1[0] - dot2[0])
    if inc == 1:
        angle = math.degrees(angle)
    if inc == 0:
        angle = math.degrees(angle)+180
        aux = dot1
        dot1 = dot2
        dot2 = aux
    return angle, dot1, dot2


def _get_matrix(dot1, angle):
    return cv.get_rotation_matrix_2d(dot1, angle, 1.0)


def _affine_transformation(matrix, original, backup, image_t, width, height):
    image_rotate = cv.warp_affine(image_t, matrix, (width, height))
    original_rotate = cv.warp_affine(original, matrix, (width, height))
    backup_rotate = cv.warp_affine(backup, matrix, (width, height))
    return backup_rotate


def _cutout_shape(dot1, backup_rotate):
    init_dot = dot1
    board_width = 602
    board_height = 295
    xi = init_dot[0] - board_width + 1
    xf = init_dot[0] + 1
    yi = init_dot[1]
    yf = init_dot[1] + board_height
    cutout = backup_rotate[yi : yf, xi : xf]
    if cutout.shape[0] != 295:
        cutout = backup_rotate[yi - 4 : yf, xi : xf]
    return cutout


def _image_to_string(new_image_name, custom_config, image_index):
    return pytesseract.image_to_string(new_image_name, config=custom_config).replace(' ', '').replace('\n', '')


def _append_path_and_model(new_image_name, board_text, image_index):
    image_path.append(new_image_name)
    image_model.append(board_text[:4])
    return image_path, image_model


def analyze_all_boards():
    for image_index in range(0, len(boards_paths)):
        utils.print_simple_progress()
        original, backup, image = _loades_images(image_index)
        height, width, image_t = _prepare_image_analyzer(image)
        inc, dot1, dot2 = _test_in_loop(height, width, image_t)
        _circle_images(original, dot1, dot2)
        angle, dot1, dot2 = _apply_math(inc, dot1, dot2)
        matrix = _get_matrix(dot1, angle)
        backup_rotate = _affine_transformation(
            matrix, original, backup, image_t, width, height)
        cutout = _cutout_shape(dot1, backup_rotate)
        new_image_name = utils._save_new_image(
            'new', boards_paths, image_index, cutout)
        custom_config = get_custom_config()
        board_text = _image_to_string(
            new_image_name, custom_config, image_index)
        image_path, image_model = _append_path_and_model(
            new_image_name, board_text, image_index)
    return image_path, image_model
