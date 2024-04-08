# File System Simulation

This is a Python script for simulating a basic file system with functionalities for saving, deleting, and visualizing files. It includes handling space allocation and fragmentation of files within the simulated storage.

## Dependencies

To run this script, you will need Python 3 and the following packages:

- `matplotlib`: For visualizing the file system fragmentation.

You can install these packages using `pip`:

```bash
pip install matplotlib
```

## Running the Script

To run the script, use the following command in a terminal or command prompt:

```bash
python file_system_simulation.py
```

Once you start the script, it will prompt you for commands. Here are the commands you can use:

- `save`: Save a file. You will be prompted to enter a filename after this command.
- `delete`: Delete a file. You will be prompted to enter the filename of the file you wish to delete.
- `visualize`: Visualize the current state of the file system, showing files and free spaces.
- `exit`: Exit the script.

## Visualization

The visualization feature uses `matplotlib` to display a bar for each file and gray areas for the free space within the file system storage. This visual representation helps understand the current fragmentation state.

## Example Usage

```bash
Enter command (save, delete, visualize, exit): save
Enter filename: file1
Enter command (save, delete, visualize, exit): visualize
Enter command (save, delete, visualize, exit): exit
```
