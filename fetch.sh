#! /bin/bash

# what I need to do
# 1. pull the image from the docker -for all the tags-
# 2. parse the layers for each image
# 3. tar the layers for each image
# 4. prune all the images

# 0. preliminary step 
image="$1"
work_dir=.
target_dir="$work_dir/output"

cd "$work_dir"

# 1. pull the image from the docker -for all the tag-
sudo docker pull $image --all-tags

# 2. I need to parse and find the layors for each image

# 1st the images
mkdir -p tmp
imagefile=tmp/images.txt
sudo docker images --format "{{.ID}} {{.Repository}} {{.Tag}}" > $imagefile
# parse the docker images



sudo docker system prune -a

