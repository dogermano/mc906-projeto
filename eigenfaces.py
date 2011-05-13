from numpy import *
from PIL import Image

DIM = 2500
WIDTH, HEIGHT = 50, 50

def get_average_face(image_files):
  # Calculate average face:
  average = zeros((HEIGHT, WIDTH))
  for image_file in image_files:
    image = asarray(Image.open(image_file))
    average += image
  average = average / len(image_files)

  # Save picture:
  Image.fromarray(average.astype('uint8')).save("average_face.jpg")
  return average

def get_eigenfaces(average_face, image_files):
  # Initialize first line:
  diff_face = asarray(Image.open(image_files[0])) - average_face
  diffs_matrix_t = diff_face.reshape(1, DIM)

  # Complete matrix t(A):
  for image_file in image_files[1:]:
    diff_face = asarray(Image.open(image_file)) - average_face
    diffs_matrix_t = concatenate((diffs_matrix_t, diff_face.reshape(1, DIM)))

  # Calculate v, eigenvectors of t(A)*A:
  diffs_matrix = diffs_matrix_t.transpose()
  w, v = linalg.eig(dot(diffs_matrix_t, diffs_matrix))

  # Eigenface i, eigenvector of A*t(A), is A*vi:
  u = dot(diffs_matrix, v)
  for i in range(u.shape[1]):
    u[:,i] = u[:,i] / linalg.norm(u[:,i])

  return w, u

def get_image_class(average_face, eigenfaces, image_file):
  # Calculate image's class:
  image_class = []
  diff_image = asarray(Image.open(image_file)) - average_face
  diff_image = diff_image.reshape(1, DIM)
  for k in range(eigenfaces.shape[1]):
    image_class.append(sum(eigenfaces[:,k].transpose() * diff_image))

  return image_class

def get_images_classes(average_face, eigenfaces, image_files):
  # Build dict with all classes:
  classes = {}
  for image_file in image_files:
    classes[image_file[:-4]] = \
      get_image_class(average_face, eigenfaces, image_file)

  return classes

def find_image_class(average_face, eigenfaces, classes, image_file):
  # Project image in face space:
  target = get_image_class(average_face, eigenfaces, image_file)

  # Find closest class:
  min_dist = 2 ** 32
  min_class = None
  for classe in classes:
    dist = linalg.norm(array(target) - array(classes[classe]))
    if dist < min_dist:
      min_dist = dist
      min_class = classe

  return min_class