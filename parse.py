import os
import sys
#from myshutil import copytree

def cp_layer(src, destbase):
    tmp = src[:src.rfind("/")]
    if src[src.rfind("/"):] != "/diff" and src[src.rfind("/"):] != "/diff\n":
        print("%r"%src[src.rfind("/"):])
        assert False
    tmp = tmp[tmp.rfind("/"):]

    dest = destbase + tmp
    #copytree(src, dest, ignore_dangling_symlinks = True)
    if src.rfind("\n") != -1:
        src = src[:src.rfind("\n")]
    order = "cp -r " + src + " " + dest
    os.system("mkdir -p " + dest)
    os.system(order) 
    
def parse_layers(input_, destbase):
    count = 0
    index = input_.find(":")
    while index != -1:
        src = input_[:index]
        input_ = input_[index + 1:]
        index = input_.find(":")
        cp_layer(src, destbase)
    src = input_
    cp_layer(src, destbase)

def make_image_dir(imagename):
    os.system("mkdir -p " + imagename)

def parse_images(filename):
    with open(filename, 'r') as f:
        for line in f:
            words = line.split() 
            id_ = words[0]
            image = words[1]
            tag = words[2]
            currdir = image + "/" + tag
            make_image_dir(currdir)
            
            order = "docker inspect -f '{{.GraphDriver.Data.LowerDir}}:{{.GraphDriver.Data.UpperDir}}' " + id_
            
            result = os.popen(order).read()
            parse_layers(result, currdir)
            os.system("tar -cvf" + currdir + ".tar " + currdir)

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
