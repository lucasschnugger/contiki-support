import sys, os, json


def readSrcFile(path):
    if os.path.isfile(path):
        file = open(srcFile)
        data = json.load(file)
        return data
    return None


def saveDestFile(path, data):
    print(data, file=open(path, 'w'))


def generateSubPath(startTime, startX, startY, nodeId, stepsize, steptime, direction, steps):
    # Directions can be:
    # - R (Right)
    # - L (Left)
    # - U (Up)
    # - D (Down)
    # - S (Stay)
    subpath = ""
    currentTime = startTime
    currentX = startX
    currentY = startY
    for step in range(steps):
        currentTime += steptime
        if direction == "R":
            currentX += stepsize
        if direction == "L":
            currentX -= stepsize
        if direction == "U":
            currentY -= stepsize
        if direction == "D":
            currentY += stepsize
        subpath += f"{nodeId-1} {currentTime} {currentX} {currentY}\n"
    return currentTime, currentX, currentY, subpath


srcFile = sys.argv[1]
destFile = sys.argv[2]
data = readSrcFile(srcFile)
if data is not None:
    result = "#node time(s) x y\n\n"

    result += "#initial positions of nodes\n"
    for mobileNode in data:
        nodeId = mobileNode['Node']
        startX = mobileNode['StartX']
        startY = mobileNode['StartY']
        result += f"{nodeId-1} 0.0 {startX} {startY}\n"
    result += "\n"

    for mobileNode in data:
        nodeId = mobileNode['Node']
        stepsize = mobileNode['StepSize']
        steptime = mobileNode['StepTime']
        starttime = mobileNode['StartTime']
        currenttime = starttime
        startX = mobileNode['StartX']
        currentX = startX
        startY = mobileNode['StartY']
        currentY = startY
        path = mobileNode['Path']
        result += f"#moving node {nodeId} (0-indexed)\n"
        for subpathElem in path:
            direction = subpathElem['Direction']
            steps = subpathElem['Steps']
            currenttime, currentX, currentY, subpath = generateSubPath(currenttime, currentX, currentY, nodeId, stepsize, steptime, direction, steps)
            result += subpath
        result += "\n"

    print(result)
    saveDestFile(destFile, result)
