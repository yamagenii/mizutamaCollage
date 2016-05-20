# -*- coding: utf-8 -*-a
from numpy.random import *
import imageGA
import operator

MAX_R = 60
NODE_NUM = 50#可変でもいいかも
GENE_NUM = 20
SELECTION_NUM = 4
CROSS_NUM = 6
MUTATION_NUM = 10
"""円ノード　タプル座標　半径"""
class CircleNode:
    def __init__(self,img):
        self.maxX = img.shape[1]
        self.maxY = img.shape[0]
        self.x = randint(int(img.shape[1]*1.1))
        self.y = randint(int(img.shape[0]*1.1))
        self.r = randint(5,MAX_R)
    """突然変異肌の上"""
    def skinMutation(self,skinpic):
        self.x = randint(skinpic[1])
        self.y = randint(skinpic[0])
        self.r = randint(5,MAX_R/2)
    """突然変異"""
    def mutation(self):
        self.x = randint(self.maxX)
        self.y = randint(self.maxY)
        self.r = randint(5,MAX_R)


class Gene:
    """遺伝子 (円ノードリスト) スコアランキングで順番を取得する"""
    num = NODE_NUM
    def __init__(self,img):
        nodes = []
        for i in range(0,NODE_NUM):
            firstNode = CircleNode(img)
            nodes.append(firstNode)
        self.nodes = nodes
        self.score = 0
        self.rank = 0#初期段階では順位付けなし

    def calcScore(self,imgGA):
        self.score = imgGA.score()


class Genelation:
    """世代(遺伝子とマスク)"""
    geneNum = GENE_NUM
    count = 0
    def __init__(self,imgPath):
        self.imgGA = imageGA.Images(imgPath)
        self.imgGA.makeMizugiMask()
        genes = []
        for i in range(0,GENE_NUM):
            firstGene = Gene(self.imgGA.img)
            genes.append(firstGene)
        self.genes = genes
        self.mask = self.imgGA.circle_mask
        self.skinpic = self.imgGA.skinPic
        print self.mask.shape
    def nextGenelation(self):
        self.calcScores()
        self.cross()
        self.mutation()
        self.count = self.count + 1

    def cross(self):
        selection_genes = self.genes[-SELECTION_NUM:]
        for i in range(0,GENE_NUM-1):
            for node in self.genes[i].nodes:
                node = selection_genes[randint(SELECTION_NUM-1)].nodes[randint(NODE_NUM)]
        


    def calcScores(self):
        self.drawCircles()
        #スコアでソート
        self.genes.sort(key=operator.attrgetter('score'))
        #print 'genelation'
        print self.count

    
    def imgOutput(self):
        self.imgGA.output(self.genes[GENE_NUM-1])
    
    def drawCircles(self):
        for gene in self.genes:
            self.imgGA.drawCircles(gene.nodes)
            gene.calcScore(self.imgGA)
    
    def mutation(self):
        for i in range(0,MUTATION_NUM-2):
            randGeneIndex = randint(GENE_NUM-2)
            randNodeIndex = randint(NODE_NUM-1)
            self.genes[randGeneIndex].nodes[randNodeIndex].mutation()
        for i in range(0,2):
            randGeneIndex = randint(GENE_NUM-2)
            randNodeIndex = randint(NODE_NUM-1)
            self.genes[randGeneIndex].nodes[randNodeIndex].skinMutation(self.skinpic[randint(len(self.skinpic))])
            

