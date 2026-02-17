import tensorflow as tf
print(f"TensorFlow Version: {tf.__version__}")
try:
    gpus = tf.config.list_physical_devices('GPU')
    print(f"GPUs: {gpus}")
except AttributeError as e:
    print(f"Error accessing list_physical_devices: {e}")
    try:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        print(f"Experimental GPUs: {gpus}")
    except AttributeError as e2:
        print(f"Error accessing experimental.list_physical_devices: {e2}")

