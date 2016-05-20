# -*- coding: utf-8 -*-
import cv2 
import numpy as np
import sys
import functools
from numba import double
from numba.decorators import jit

class Images:

    def __init__(self,imgPath):
        cv2.namedWindow('GA')
        self.img = cv2.imread(imgPath)
        self.circle_mask = np.zeros(self.img.shape, dtype=np.uint8)
        self.mizugi_mask = np.zeros(self.img.shape, dtype=np.bool)
        self.skin_mask = np.zeros(self.img.shape, dtype=np.bool)
        self.circle_mask_bool = np.zeros(self.img.shape, dtype=np.bool)
        self.circle_score = 0
        self.skinPic = []
    def makeMizugiMask(self):
        dst = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        for i in range (dst.shape[0]):
            for j in range (dst.shape[1]):
                # print "%d\t%d\t%d"%(dst[i][j][0],dst[i][j][1],dst[i][j][2]
                # 白のサークルマスク作成
                self.circle_mask[i][j][0] = 255
                self.circle_mask[i][j][1] = 255
                self.circle_mask[i][j][2] = 255
                # 水着マスク作成 特典加算でtrue 隠れている部分で特典
                #if ((dst[i][j][0] < 30 or dst[i][j][0] > 130) and dst[i][j][1] > 160 and dst[i][j][2] >130): 赤水着
                if dst[i][j][1] > 50*(255/100) and dst[i][j][2] > 18*(255/100):
                    self.mizugi_mask[i][j][0]= True
                    #debugcode
                    #self.circle_mask[i][j][0] = 0
                    #self.circle_mask[i][j][1] = 255
                    #self.circle_mask[i][j][2] = 255

                # スキンマスク作成 特典加算でfalse 隠れていない部分で特典
                if dst[i][j][0] < 50 and dst[i][j][1]>5:
                    self.skin_mask[i][j][0] = True
                    self.mizugi_mask[i][j][0]= False
                    self.skinPic.append([i,j])
                    #debugcode
                    #self.circle_mask[i][j][0] = 255
                    #self.circle_mask[i][j][1] = 0
                    #self.circle_mask[i][j][2] = 255

        #cv2.imshow('GA',self.circle_mask)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    def drawCircles(self,nodes):#座標インスタンスも引数
        self.circle_mask = np.zeros(self.img.shape, dtype=np.uint8)
        self.tmp_circle_mask = np.zeros(self.img.shape, dtype=np.uint8)
        self.tmp_circle_mask_bool = np.zeros(self.img.shape, dtype=np.uint8)
        self.circle_score = 0
        for node in nodes:
            cv2.circle(self.circle_mask,(node.x,node.y),node.r,(255,255,255),-1)
            #cv2.circle(self.tmp_circle_mask,(node.x,node.y),node.r,(255,255,255),-1)
            #b = self.circle_mask == 255
            #a = self.tmp_circle_mask_bool == 255
            #self.tmp_circle_mask_bool = np.logical_and(b,a)
            #self.circle_score += np.count_nonzero(self.tmp_circle_mask_bool)/3
            #self.tmp_circle_mask = np.zeros(self.img.shape, dtype=np.uint8)
        self.circle_mask_bool = self.circle_mask < 100
        self.not_circle_mask_bool = self.circle_mask ==255
        #for i in range(mask.shape[0]):
        #    for j in range(mask.shape[1]):
        #        if ((mask[i][j][0] == 255) or (self.circle_mask[i][j][0] == 0)):
        #            self.circle_mask[i][j][0] = 0
        #            self.circle_mask[i][j][1] = 0
        #            self.circle_mask[i][j][2] = 0
    def mizutama(self):
        for i in range(self.circle_mask.shape[0]):
            for j in range(self.circle_mask.shape[1]):
                if self.circle_mask[i][j][2] == 0:
                    #黒
                    self.img[i][j][0] = 0
                    self.img[i][j][1] = 0
                    self.img[i][j][2] = 0

    def output(self,gene):
        self.drawCircles(gene.nodes)
        self.mizutama()
        #cv2.imshow('GA',self.circle_mask)
        self.save()
        cv2.imshow('GA',self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def score(self):
        #点数付け
        score = 0
        mizugi_score = np.logical_and(self.circle_mask_bool,self.mizugi_mask)
        skin_score = np.logical_and(self.not_circle_mask_bool,self.skin_mask)
        score = np.count_nonzero(mizugi_score)*200 + np.count_nonzero(skin_score)*1 - self.circle_score
        #print "score:",score
        #for i in range(self.circle_mask.shape[0]):
        #    for j in range(self.circle_mask.shape[1]):
        #        inp.dotf self.circle_mask[i][j][2] == 0 and self.mizugi_mask[i][j][0] == False:
        #            #黒
        #            score += 100
        #        if self.circle_mask[i][j][2] == 255 and self.skin_mask[i][j][0] == True:
        #            score += 1
        return score

    def save(self):
        cv2.imwrite('result.jpg',self.img)








