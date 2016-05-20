#must be same dir with GA imageGA
# -*- coding: utf-8 -*-
import GA
#IMAGE_PATH = 'kasumi.jpeg' 
#IMAGE_PATH = 'mizu.jpeg' 
if __name__ == '__main__':
    print "please write image path"
    path = st = str(raw_input())
    #1世代作成
    genelation = GA.Genelation(path)
    for i in range(0,100):
        genelation.nextGenelation()

    genelation.imgOutput()


