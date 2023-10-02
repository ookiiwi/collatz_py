from .util import Point
import cv2
import numpy as np

START_ANGLE             = 180
INITIAL_ANGLE           = 8
INITIAL_VALUE           = 1000
DEFAULT_HEIGHT          = 800
DEFAULT_WIDTH           = 600
COLORS_NUMBER           = 3
BOTTOM_PADDING          = 10
ADJUSTMENT_THRESHOLD    = 200

n = INITIAL_VALUE
angle = INITIAL_ANGLE
halfAngle = angle/2

img = np.zeros((DEFAULT_HEIGHT, DEFAULT_WIDTH, COLORS_NUMBER), np.uint8)
center = Point(DEFAULT_WIDTH // 2, DEFAULT_HEIGHT - BOTTOM_PADDING)

class Stroke():
    '''
    Draw continuous line
    '''

    def __init__(self):
        self._unitVec = Point(1, 0) # used to keep track of rotation
        self.pos = Point()

    def rotate(self, a):
        self._unitVec = self._unitVec.rotate(a)

    def translate(self, amount):
        global img

        color = (255,255,255)
        endPos = self.pos + (amount * self._unitVec)

        def computePoints():
            start = self.pos + center
            end   = endPos   + center

            return start, end
        
        start, end = computePoints()

        # adjust image if needed
        img, hasBeenAdjusted = adjustImageToFitPoint(img, end)

        # recompute points if adjustement done
        if hasBeenAdjusted:
            start, end = computePoints()

        img = cv2.line(img, 
                       (int(start.x), int(start.y)),
                       (int(end.x), int(end.y)), color, 2)

        self.pos = endPos

def adjustImageToFitPoint(img, point):
    global center
    height, width = img.shape[:2]
    hasBeenAdjusted = False

    # use lambda to avoid computing array on every call
    adjustmentImageCol = lambda : np.zeros((height, ADJUSTMENT_THRESHOLD, COLORS_NUMBER), np.uint8)
    adjustmentImageRow = lambda : np.zeros((ADJUSTMENT_THRESHOLD, width, COLORS_NUMBER),  np.uint8)

    if point.x <= 0:
        img = cv2.hconcat([adjustmentImageCol(), img])
        hasBeenAdjusted = True
    elif point.x >= width:
        img = cv2.hconcat([img, adjustmentImageCol()])
        hasBeenAdjusted = True

    if point.y <= 0:
        img = cv2.vconcat([adjustmentImageRow(), img])
        hasBeenAdjusted = True
    elif point.y >= height:
        img = cv2.vconcat([img, adjustmentImageRow()])
        hasBeenAdjusted = True

    if hasBeenAdjusted:
        height, width = img.shape[:2]
        center = Point(center.x, height-BOTTOM_PADDING) # x should always stay the same

    return img, hasBeenAdjusted

def collatz(val):
    return val / 2 if val % 2 == 0 else (val * 3 + 1) / 2

def computeBranch(val):
    '''
    Apply collatz rules to values from [val] to 1

    Return a list of values
    '''

    branch = []

    while val > 1:
        branch.append(val)
        val = collatz(val)

    branch.append(1)

    return branch

def drawBranch(values):
    stroke = Stroke()
    stroke.rotate(START_ANGLE)

    for i in range(0, len(values)-1):
        if values[i]*2 == values[i+1]:
            stroke.rotate(angle) # rotate clockwise
        else:
            stroke.rotate(-halfAngle)

        stroke.translate(10) # really slow

def main():
    # draw branches
    for i in range(2, n+1):
        branch = computeBranch(i)
        branch.reverse()

        drawBranch(branch)
        del branch

    imgName= f"Collatz_{n}"
    
    cv2.imshow(imgName.replace('_', ' '), img)
    cv2.waitKey(0)
    cv2.imwrite(f'{imgName.lower()}.png', img)
