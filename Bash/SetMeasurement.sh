#!/bin/bash
if [ -z "$1" ]; then
	printf "Add measurement name.\nType eg:\n. SetMeasurement.sh Neurons01\n"
else
	manip="/home/pi/Desktop/Manip/"
	acqui_file="acquisition_2cams.py"
	example_file="/home/pi/Desktop/Manip/Example/$acqui_file"
	readme_file="/home/pi/Desktop/Manip/Example/readme.txt"
	manip_dir="$(date +%Y-%m-%d)"
	path_tmp="$manip$manip_dir"
	mkdir -p $path_tmp
	path_full="$path_tmp/$1"
	mkdir -p $path_full
	cp $example_file $path_full
	cp $readme_file $path_full

	cd $path_full
	printf "Measurement sucessfully created in $path_full\n"
	printf "1) Adjust the acquisition file '$acqui_file'\n"
	printf "2) Fill in the 'readme.txt'\n"
	printf "3) Start the measurement by calling:\npython acquisiton_2cams.py\n"
	
fi
