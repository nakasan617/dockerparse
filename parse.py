import os
import sys
import shutil

def parse_layers(input_):
    input_ = input_[input_.find("[") + 1:]
    input_ = input_[:input_.rfind("]")]
    shas = input_.split()
    for i in range(len(shas)):
        shas[i] = shas[i][shas[i].find(":") + 1:]
    print(shas)
        
    return shas 

def locate_layers(layers):
    base = "/var/lib/docker/image/overlay2/layerdb/sha256/"
    for layer in layers:
        dir_ = base + layer + "/diff"
        print("one layer")
        print(dir_)
        os.system("cat " + dir_)

def locate_layer(layer):
    base = "/var/lib/docker/image/overlay2/layerdb/sha256/"
    dir_ = base + layer + "/cache-id"
    os.system("cat " + dir_)
    
def tar_layers(layers, currdir):
    base = "/var/lib/docker/overlay2/"
    count = 0
    for layer in layers:
        #if count > 0:
        #    break
        src = base + layer + "/diff/"
        if os.path.isdir(src):
            os.system("ls " + src)
            #shutil.copytree(src, currdir)
        else:
            locate_layer(layer)

        #count += 1 

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
            make_image_dir(currdir)
            order = "docker inspect -f '{{.GraphDriver.Data.LowerDir}}:{{.GraphDriver.Data.UpperDir}}' " + id_
            
            result = os.popen(order).read()
            #print(image + " " + tag)
            #layers = parse_layers(result)
            #tar_layers(layers, currdir)
            #locate_layer(layers)
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
