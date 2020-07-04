import os
import sys
import shutil

def tar_layer(currdir):
    shutil.copytree(currdir, dest)
    
def parse_layers(input_):
    count = 0
    index = input_.find(":")
    while index != -1:
        portion = input_[:index]
        input_ = input_[index + 1:]
        index = input_.find(":")
        tar_layer(portion)
    portion = input_
    tar_layer(portion)

def make_image_dir(imagename):
    os.system("mkdir -p " + imagename)

def parse_images(filename):
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            if count > 0:
                break
            words = line.split() 
            id_ = words[0]
            image = words[1]
            tag = words[2]
            currdir = image + "_" + tag
            make_image_dir(currdir, image)
            order = "docker inspect -f '{{.GraphDriver.Data.LowerDir}}:{{.GraphDriver.Data.UpperDir}}' " + id_
            
            result = os.popen(order).read()
            parse_layers(result)
            count += 1

def pull_images(imagename, wd):
    os.system("cd " + wd)
    os.system("docker pull " + imagename + " --all-tags")    
    os.system("mkdir -p tmp")
    imagefile = "tmp/images.txt"
    os.system("docker images --format \"{{.ID}} {{.Repository}} {{.Tag}}\" > " + imagefile)

def main():
    assert len(sys.argv) == 3
    # pull_images(sys.argv[1], sys.argv[2])
    imagefile = "tmp/images.txt"
    parse_images(imagefile)

if __name__ == "__main__":
    main()
