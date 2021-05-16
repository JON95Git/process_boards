import cv2

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def loades_image(image_path, flag):
    return cv2.imread(image_path, flag)

def show_image(message, image):
    cv2.imshow(message, image)

def saves_image(image, params):
    cv2.imwrite(image, params)

def wai_time(time):
    cv2.waitKey(time)
    cv2.destroyAllWindows()

def threshold(image):
    return cv2.threshold(image, 230, 255, cv2.THRESH_BINARY)

def circle(origin, dot):
    return cv2.circle(origin, (dot), 2, (0, 0, 255), -1)

def get_rotation_matrix_2d(dot, angle, value):
    return cv2.getRotationMatrix2D(dot, angle, value)

def warp_affine(image, matrix, size):
    return cv2.warpAffine(image, matrix, (size))

def split(difference):
    return cv2.split(difference)

def count_non_zero(a):
    cv2.countNonZero(a)
