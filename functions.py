


import cv2
import numpy


class STI:
    def __init__(self, path):
        self.frameCounter = 0
        self.video = cv2.VideoCapture(path)


        self.videoWidth  = 64
        self.videoHeight  = 64
        self.threshold = 0.3

        # Uncomment below for slower processing
        # self.videoWidth  = int(self.video.get((cv2.CAP_PROP_FRAME_WIDTH)))
        # self.videoHeight  = int(self.video.get((cv2.CAP_PROP_FRAME_HEIGHT)))

        self.totalFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.bins = numpy.floor(1 + numpy.log2(self.videoHeight)).astype(int)


    def columnSTI(self):
        self.video.set(1, 0)
        columnSTI = numpy.zeros((self.videoHeight, self.totalFrames, 3), dtype=numpy.uint8)
        middleCol = round(self.videoWidth/2)
        while (self.frameCounter < self.totalFrames):
            self.frameCounter += 1
            hasFrames, image = self.video.read()
            if hasFrames:
                for i in range(self.videoHeight):
                    bluePixel, greenPixel, redPixel = image[i][middleCol]
                    columnSTI[i][self.frameCounter-1] = [bluePixel, greenPixel, redPixel]
        cv2.imwrite('middlecolumn.jpg', columnSTI)
        self.frameCounter = 0
        return True

    def rowSTI(self):
        self.video.set(1, 0)
        rowSTI = numpy.zeros( (self.videoWidth, self.totalFrames, 3), dtype=numpy.uint8)
        middleRow = round(self.videoHeight/2)
        while (self.frameCounter < self.totalFrames):
            self.frameCounter += 1
            hasFrames, image = self.video.read()
            if hasFrames:
                for i in range(self.videoWidth):
                    bluePixel, greenPixel, redPixel = image[middleRow][i]
                    rowSTI[i][self.frameCounter-1] = [bluePixel, greenPixel, redPixel]
        cv2.imwrite('middlerow.jpg', rowSTI)
        self.frameCounter = 0
        return True




    def histogramSTI(self):
        self.video.set(1, 0)
        histSTI = numpy.zeros( (self.videoWidth, self.totalFrames, 3), dtype=numpy.uint8)
        newPastFrameHist = []
        rg =  numpy.zeros( (self.videoWidth + 1, self.videoHeight + 1, 3), dtype=numpy.uint8)
        while (self.frameCounter < self.totalFrames):
            self.frameCounter += 1
            hasFrames, image = self.video.read()
            if hasFrames:
                pastFrameHist = newPastFrameHist
                newPastFrameHist = []
                rg =  numpy.zeros( (self.videoWidth + 1, self.videoHeight + 1, 3), dtype=numpy.uint8)

                for j in range(self.videoWidth):

                    currentColHist = numpy.zeros((self.bins.astype(int), self.bins.astype(int)))
                    redChormaArr = []
                    greenChormaArr = []

                    for i in range(self.videoHeight):
                        redChroma = 0
                        greenChroma = 0
                        bluePixel, greenPixel, redPixel = image[i][j]
                        sum = bluePixel * 1.0 + greenPixel * 1.0 + redPixel * 1.0 +  + 0.00000000001
                        if (sum > 0):
                            redChroma = ((redPixel / sum))
                            greenChroma = ((greenPixel / sum))
                        if (redChroma < 0):
                            redChroma = 0
                        if (greenChroma < 0):
                            greenChroma = 0

                        rg[j][i] = [redChroma*255, greenChroma*255, 0]
                        # cv2.imwrite("./debug/rg_image"+ str(self.frameCounter) +".jpg", rg)

                        redChormaArr.append(redChroma)
                        greenChormaArr.append(greenChroma)

                    redChormaArr = numpy.array(redChormaArr)
                    greenChormaArr = numpy.array(greenChormaArr)

                    # Normalize
                    if (numpy.any(redChormaArr)):
                        redChormaArr = (self.bins - 1)*((redChormaArr - numpy.min(redChormaArr))/(numpy.ptp(redChormaArr)))
                    if (numpy.any(greenChormaArr)):
                        greenChormaArr = (self.bins - 1)*((greenChormaArr - numpy.min(greenChormaArr))/(numpy.ptp(greenChormaArr)))

                    for z in range(redChormaArr.size):
                        currentColHist[numpy.round(redChormaArr[z]).astype(int)][numpy.round(greenChormaArr[z]).astype(int)] += 1/self.videoHeight

                    sum = 0
                    histSTI[j][self.frameCounter-1] = [255, 255, 255]
                    if (self.frameCounter != 1):
                        for x in range(self.bins):
                            for y in range(self.bins):
                                sum += min(currentColHist[x][y], pastFrameHist[j][x][y])
                        if (sum < self.threshold):
                            histSTI[j][self.frameCounter-1] = [255*sum, 255*sum, 255*sum]

                    newPastFrameHist.append(currentColHist)
                print ("Frame " + str(self.frameCounter) + " processed")
        cv2.imwrite('histogramdifference.jpg', histSTI)
        print ("All frames processed. \n")
        self.frameCounter = 0
        return True