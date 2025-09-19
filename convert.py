import os
from moviepy import ImageSequenceClip
from functions import log

image_folder = 'figures' # Replace with your image folder path
output_video_name = 'Simulation.mp4'
fps = 4 # Frames per second

image_files = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")]
image_files.sort() # Ensure images are in desired order

clip = ImageSequenceClip(image_files, fps=fps)
clip.write_videofile(output_video_name)
log(f"Video '{output_video_name}' created successfully.")