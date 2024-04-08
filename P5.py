#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wednesday Mar 6 15:10:27 2024

@author: jamesmiller
@packages: matplotlib, random
"""

import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class FileSystem:
    def __init__(self, storageSize, systemSlowThreshold):
        self.storageSize = storageSize
        self.freeSpace = storageSize
        self.files = {}
        self.systemSlowThreshold = systemSlowThreshold
        self.freeSpaces = [{'start': 0, 'size': self.storageSize}]

    def saveFile(self, filename, filesize):
        print("Saving file:", filename, filesize)  # Temporary check
        if filesize > self.freeSpace:
            print("Not enough space")
            return False

        if not self._findContiguousSpace(filesize):
            self._fragmentFile(filename, filesize)

        self.freeSpace -= filesize
        print("New free space:", self.freeSpace)  # Check if this updates
        return True

    def deleteFile(self, filename):
        fileData = self.files.pop(filename, None)
        if fileData:
            self.freeSpace += sum(frag['size'] for frag in fileData['fragments'])

    def loadFile(self, filename):
        fileData = self.files.get(filename)
        if not fileData:
            return

        loadTime = self._calculateBaseLoadTime(fileData['size'])

        if len(fileData['fragments']) > 1:
            loadTime += self._calculateAssemblyTime(fileData['fragments'])

        return loadTime

    def _allocateFromSpace(self, index, space, file_size):
        start = space['start']
        newSpaceStart = start + file_size

        if file_size < space['size']:
            self.freeSpaces[index]['size'] -= file_size
            self.freeSpaces[index]['start'] = newSpaceStart
        else:
            del self.freeSpaces[index]

    def _findContiguousSpace(self, fileSize):
        for i, space in enumerate(self.freeSpaces):
            if space['size'] >= fileSize:
                self._allocateFromSpace(i, space, fileSize)
                return True
        return False

    def _fragmentFile(self, filename, fileSize):
        fragments = []
        remainingSize = fileSize

        for i, space in enumerate(self.freeSpaces):
            if space['size'] >= remainingSize:
                fragments.append({'start': space['start'], 'size': remainingSize})
                self.updateFreeSpaces(i, space, remainingSize)
                break
            else:
                fragments.append({'start': space['start'], 'size': space['size']})
                remainingSize -= space['size']
                self.updateFreeSpaces(i, space, space['size'])

        self.files[filename] = {'fragments': fragments}

    def updateFreeSpaces(self, index, space, usedSize):
        if usedSize < space['size']:
            self.freeSpaces[index]['size'] -= usedSize
            self.freeSpaces[index]['start'] += usedSize
        else:
            del self.freeSpaces[index]

    def visualize(self):
        plt.figure(figsize=(10, 2))
        plt.xlim(0, self.storageSize)
        plt.ylim(0, 1)

        # Check and visualize each file fragment
        for fileName, fileData in self.files.items():
            for fragment in fileData['fragments']:
                if fragment['size'] > 0:  # Ensuring the fragment size is greater than zero
                    plt.gca().add_patch(mpatches.Rectangle(
                        (fragment['start'], 0), fragment['size'], 1,
                        edgecolor='black', facecolor=self._getFragmentColor(fileName)
                    ))
                else:
                    print(f"Fragment size error for file {fileName}")

        # Visualize free spaces
        for space in self.freeSpaces:
            if space['size'] > 0:
                plt.gca().add_patch(mpatches.Rectangle(
                    (space['start'], 0), space['size'], 1,
                    edgecolor='black', facecolor='gray'
                ))
            else:
                print("Free space size error")

        plt.xlabel("Storage")
        plt.title("File System Fragmentation")
        plt.legend(handles=[
            mpatches.Patch(color='green', label='Files'),
            mpatches.Patch(color='gray', label='Free Space')
        ])
        plt.show()

    def _getFragmentColor(self, filename):
        return 'green'

    def _calculateBaseLoadTime(self, fileSize):
        baseLoadFactor = 0.01
        return fileSize * baseLoadFactor

    def _calculateAssemblyTime(self, fragments):
        assemblyOverhead = 5
        for fragment in fragments:
            assemblyOverhead += fragment['size'] * 0.005
        return assemblyOverhead


criticalityMetrics = []
fileSystem = FileSystem(100, 0.8)

while True:
    command = input("Enter command (save, delete, visualize, exit): ")

    if command == "save":
        filename = input("Enter filename: ")
        filesize = random.randint(1, 50)
        success = fileSystem.saveFile(filename, filesize)
        if not success:
            print("Not enough space.")

    elif command == "delete":
        filename = input("Enter filename to delete: ")
        fileSystem.deleteFile(filename)

    elif command == "visualize":
        fileSystem.visualize()

    elif command == "exit":
        break

    else:
        print("Invalid command.")

    # Metric Collection
    fragmentedFiles = sum(len(file['fragments']) > 1 for file in fileSystem.files.values())
    fragmentationPercentage = 0
    if len(fileSystem.files) > 0:
        fragmentationPercentage = fragmentedFiles / len(fileSystem.files)

    criticalityMetrics.append(fragmentationPercentage)

    # Critical Condition
    if fragmentationPercentage >= fileSystem.systemSlowThreshold:
        print("System too slow!")
        break
