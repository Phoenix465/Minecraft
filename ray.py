"""
Handles Raycasting

Functions
-----
getCloseChunks - Gets two closest Chunks based on lookVector

raycast - Performs a Raycast.
"""

from vector import Vector3


def getCloseChunks(startPos: Vector3, lookVector: Vector3, world):
    """


    Parameters
    ----------
    startPos : Vector3
        The Start Position of the Range Check

    lookVector : Vector3
        The Direction of the Range Ray

    world : World
        The world that the chunks are used from.

    Returns
    -------
    chunkCheck : list
        A list containing Chunks which are to be checked in the Raycasting.

    """

    addVector = lookVector * Vector3(1, 0, 1) * 0.1
    updateCurrentCameraPos = startPos - addVector

    checkChunks = list(world.adjacentCurrentChunk.values()) + list(world.cornerCurrentChunks.values())

    filterCheckChunks = []

    for chunk in checkChunks:
        if not chunk:
            continue

        chunkCentre = chunk.bottomCentre.copy()
        chunkCentre.Y = startPos.Y

        chunkOrigDist = (startPos - chunkCentre).magnitude
        chunkNewDist = (updateCurrentCameraPos - chunkCentre).magnitude

        if chunkNewDist < chunkOrigDist:
            filterCheckChunks.append(chunk)

    filterCheckChunks = [chunk for chunk in filterCheckChunks if chunk]
    filterScoreChunk = {chunk: 0 for chunk in filterCheckChunks}
    currentRayPos = startPos

    for _ in range(10):
        bestChunk = None
        bestDist = 500

        currentRayPos += addVector

        for chunk in filterCheckChunks:
            dist = (chunk.bottomCentre - currentRayPos).magnitude

            if dist < bestDist:
                bestChunk = chunk
                bestDist = dist

        if bestChunk:
            filterScoreChunk[bestChunk] += 1

    closestChunkTarget = None
    highestScore = 0

    for chunk, score in filterScoreChunk.items():
        if score > highestScore:
            highestScore = score
            closestChunkTarget = chunk

    chunkCheck = [world.currentChunk]
    if closestChunkTarget:
        chunkCheck.append(closestChunkTarget)

    chunkCheck = list(filter(None, chunkCheck))

    return chunkCheck


def raycast(startPoint: Vector3, lookVector: Vector3, maxDist: int, chunkCheckList: list):
    """
    Raycasts to find the block hit.

    Parameters
    ----------
    startPoint : Vector3
        Starting Position of the Ray

    lookVector : Vector3
        Direction of the Ray

    maxDist : int
        Max Distance of the Ray

    chunkCheckList : list
        Chunks that the blocks are to be checked from

    Returns
    -------
    list
        Either None list or a list containing about the block hit.
    """

    def convert(num):
        if num < 0:
            return num + 16

        if num >= 16:
            return num % 16

        return num

    distDiff = 0
    currentRayPosition = startPoint
    lookMag = lookVector.magnitude

    if len(chunkCheckList) == 0:
        return

    lastPos = None

    while distDiff < maxDist:
        closestBlockPos = Vector3(*[round(posP) for posP in currentRayPosition.tuple])

        if closestBlockPos != lastPos:
            targetChunk = None

            for chunk in chunkCheckList:
                if chunk.isPointInChunk(closestBlockPos):
                    targetChunk = chunk

            if targetChunk:
                posChunk = closestBlockPos.copy()

                posChunk.X = convert(posChunk.X)
                posChunk.Z = convert(posChunk.Z)

                targetBlock = targetChunk.blocks[posChunk.Y][posChunk.X][posChunk.Z]

                if any(targetBlock.surfacesShow):
                    closestSurfaceI = targetBlock.closestSurfaceIndex(currentRayPosition)

                    return [targetChunk, targetBlock, closestSurfaceI]

        lastPos = closestBlockPos
        currentRayPosition -= lookVector
        distDiff += lookMag

    return [None, None, None]
