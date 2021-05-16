from src import open_cv as cv

def _save_new_image(prefix, boards_paths, image_index, cutout):
    new_image_name = 'result/' + prefix + '%s' % boards_paths[image_index].replace('images/boards/', '-')
    cv.saves_image(new_image_name, cutout)
    return new_image_name

def print_simple_progress():
    print ('.', end="", flush=True)