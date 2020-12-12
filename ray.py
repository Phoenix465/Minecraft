from vector import Vector3
#from world import World


def getCloseChunks(startPos: Vector3, lookVector: Vector3, world):
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

def raycast(startPoint: Vector3, lookVector: Vector3, maxDist: int, world):
    pass