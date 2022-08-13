import imageio as iio
import matplotlib.pyplot as plt
import time


# Will need to add audio capture to script as well
camera = iio.get_reader("<video0>")
meta = camera.get_meta_data()
num_frames = 5 * int(meta["fps"])
delay = 1/meta["fps"]

buffer = list()
for frame_counter in range(num_frames):
    frame = camera.get_next_data()
    buffer.append(frame)
    time.sleep(delay)

camera.close()

iio.mimwrite("frames.mp4", buffer, macro_block_size=8, fps=meta["fps"])