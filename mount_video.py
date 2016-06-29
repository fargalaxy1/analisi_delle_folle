import os

commandString = "ffmpeg -f image2 -r 4 -i output/timestep_%01d.png -vcodec mpeg4 -y output/movie_script.mp4"
os.system(commandString)

# commandString_launch = "/Applications/VLC.app/Contents/MacOS/include/vlc movie_script.mp4"
# os.system(commandString_launch)
