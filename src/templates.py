import re
import numpy
import pytesseract
from src import open_cv as cv
from matplotlib import pyplot
import math
from PIL import Image
import time
from src import utils
import os

templates_paths = [
    'images/templates/template-AB01.jpg',
    'images/templates/template-AB02.jpg',
    'images/templates/template-AC01.jpg',
    'images/templates/template-AC02.jpg'
]

template_models = [
    'AB01',
    'AB02',
    'AC01',
    'AC02'
]

rgb_value = [0, 0, 0]

coordinates_ab01 = [81, 82], [62, 58], [90, 108], [
    234, 302], [210, 401], [101, 401], [194, 503]
coordinates_ab02 = [122, 121], [148, 83], [173, 64], [
    127, 283], [151, 401], [174, 501]
coordinates_ac01 = [221, 110], [194, 84], [101, 84], [
    244, 134], [58, 454], [151, 431], [233, 406]
coordinates_ac02 = [161, 180], [125, 260], [125, 101], [
    175, 310], [55, 460], [150, 436], [245, 410]

is_inverted_ab01 = [False, False, False, True, True, True, True]
is_inverted_ab02 = [False, False, False, True, True, True]
is_inverted_ac01 = [False, False, False, False, True, True, True]
is_inverted_ac02 = [False, False, False, True, True, True, True]

error_msgs = ['missing square', 'missing rectangle', 'position error']

error_msgs_ab01 = [error_msgs[0], error_msgs[0], error_msgs[0],
                   error_msgs[1], error_msgs[1], error_msgs[2], error_msgs[1]]
error_msgs_ab02 = [error_msgs[0], error_msgs[0], error_msgs[0],
                   error_msgs[1], error_msgs[1], error_msgs[1]]
error_msgs_ac01 = [error_msgs[0], error_msgs[0], error_msgs[2],
                   error_msgs[0], error_msgs[1], error_msgs[1], error_msgs[1]]
error_msgs_ac02 = [error_msgs[0], error_msgs[0], error_msgs[2],
                   error_msgs[0], error_msgs[2], error_msgs[1], error_msgs[1]]
log_message = ''
log_system = []
tolerance = 0.1


def print_init_message():
    print()
    print('Checking templates...')


def _get_duplicate_and_model(image_path, image_model, image_index):
    duplicate = cv.loades_image(image_path[image_index], 1)
    template_model = image_model[image_index]
    return duplicate, template_model


def _verfify_template(image_model, image_index):
    if image_model[image_index] == template_models[0]:
        templates_model = templates_paths[0]
    elif image_model[image_index] == template_models[1]:
        templates_model = templates_paths[1]
    elif image_model[image_index] == template_models[2]:
        templates_model = templates_paths[2]
    elif image_model[image_index] == template_models[3]:
        templates_model = templates_paths[3]
    return templates_model


def _read_template_image(templates_model, duplicate):
    template_image = cv.loades_image(templates_model, 1)
    difference = template_image - duplicate
    return template_image, difference


def _get_rgb(split_value):
    b, g, r = cv.split(split_value)
    return r, g, b


def _check_tolerance(template_image, duplicate, rgb):
    for y in range(0, template_image.shape[0], 1):
        for x in range(0, template_image.shape[1], 1):
            if _if_tolerance(rgb, x, y):
                duplicate[y, x] = (0, 0, 255)


def _if_tolerance(rgb, x, y):
    return rgb[0][y, x] > 255 * tolerance or rgb[1][y, x] > 255 * tolerance or rgb[2][y, x] > 255 * tolerance


def _is_red(rgb):
    return rgb[0] == 255 and rgb[1] == 0 and rgb[2] == 0


def _get_rgb_value(x, y, is_inverted, duplicate):
    if is_inverted == True:
        (b, g, r) = duplicate[x, y]
    else:
        (b, g, r) = duplicate[y, x]
    return r, g, b


def _test_coordinate(coord, message, is_inverted, duplicate):
    global log_message
    rgb_value = _get_rgb_value(coord[0], coord[1], is_inverted, duplicate)
    is_red = _is_red(rgb_value)
    if is_red:
        log_message = ' ' + message
        return False                     
    else:
        return True


def _check_if_ok(coord_checks):
    if all(coord_checks) == True:
        error_msg = 'OK'
    else:
        error_msg = 'not OK: ' + log_message
    log_system.append(error_msg)


def _test_coordinates_model(template_model, duplicate):
    is_ok = [True, True, True, True, True, True, True]
    if template_model == template_models[0]:
        for i in range(len(coordinates_ab01)):
            is_ok[i] = _test_coordinate(
                (coordinates_ab01[i]), error_msgs_ab01[i], is_inverted_ab01[i], duplicate)

    elif template_model == template_models[1]:
        for i in range(len(coordinates_ab02)):
            is_ok[i] = _test_coordinate(
                (coordinates_ab02[i]), error_msgs_ab02[i], is_inverted_ab02[i], duplicate)

    elif template_model == template_models[2]:
        for i in range(len(coordinates_ac01)):
            is_ok[i] = _test_coordinate(
                (coordinates_ac01[i]), error_msgs_ac01[i], is_inverted_ac01[i], duplicate)

    elif template_model == template_models[3]:
        for i in range(len(coordinates_ac02)):
            is_ok[i] = _test_coordinate(
                (coordinates_ac02[i]), error_msgs_ac02[i], is_inverted_ac02[i], duplicate)
    _check_if_ok((is_ok))


def _is_non_zero(rgb):
    return (cv.count_non_zero(rgb[0]) != 0 or cv.count_non_zero(rgb[1]) != 0 or cv.count_non_zero(rgb[2]) != 0)


def _check_against_template(template_model, duplicate, rgb):
    if _is_non_zero(rgb):
        _test_coordinates_model(template_model, duplicate)


def print_results(boards_paths):
    print()
    print('-' * 60)
    print('Results:')
    for i in range(0, len(boards_paths)):
        print(boards_paths[i] + ' ..... ' + log_system[i])
    print('-' * 60)
    print()


def check_all_templates(image_path, image_model, boards_paths):
    for image_index in range(0, len(boards_paths)):
        utils.print_simple_progress()
        duplicate, template_model = _get_duplicate_and_model(
            image_path, image_model, image_index)
        templates_model = _verfify_template(image_model, image_index)
        template_image, difference = _read_template_image(
            templates_model, duplicate)
        rgb = _get_rgb(difference)
        _check_tolerance(template_image, duplicate, rgb)
        _check_against_template(template_model, duplicate, rgb)
        new_image_name = utils._save_new_image(
            'draw', boards_paths, image_index, duplicate)
        cv.wai_time(1)
