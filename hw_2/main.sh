#!/usr/bin/env

# run 'sh main.sh' from command line 
# check this script and dockerfile are in PythonCourse/hw_2 now

docker build -t hw2pdf $(pwd)  && docker run --mount src="$(pwd)/artifacts",target=/PythonCourse/hw_2/artifacts,type=bind -it hw2pdf
