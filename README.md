# NTFS-Timestamp-Visualizer
NTFS Timestamp Visualizer takes the input from [NTFS Timestamp Analyser](https://github.com/JelleBouma/TimestampAnalyser), which analyses NTFS timestamps and reconstructs the possible histories in terms of operations on files, and creates a tree-based visualization of these histories.

## Installation
Follow the steps below to install NTFS Timestamp Visualizer:
1. Install [Python 3.6](https://www.python.org/downloads/) or higher
    - On Windows, it's recommended to add Python to your path
2. Install [Graphviz](https://www.graphviz.org/download/) for your platform
    - On Windows, place the contents of the zip somewhere, and add this location to your path
    - On Linux, use your distributions' package manager to install Graphviz
3. OPTIONAL: Create a virtual environment
4. Install the packages in the requirements.txt (`pip install -r requirements.txt` by default)

NTFS Timestamp Visualizer should now be installed.

## Usage
The default usage format is:
```bash
python timestamp_visualizer.py sample-input.txt
```

The full usage format is:
```bash
python timestamp_visualizer.py [-h] [-o OUTPUT] [-f FILTER] [-d DPI] [-s] [-O ORIGIN_STATES] [-F FORGERY_STATES] [-H HORIZONTAL_SEP] [-V VERTICAL_SEP] input
```

Additionally, there are a number of options:
<table>
    <tr>
        <th>Option</th>
        <th>Form</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Help</td>
        <td><code>-h</code>, <code>--help</code></td>
        <td>Shows the help menu</td>
    </tr>
    <tr>
        <td>Output</td>
        <td><code>-o OUTPUT</code>, <code>--output OUTPUT</code></td>
        <td>Set the output path for the visualisation</td>
    </tr>
    <tr>
        <td>Filter</td>
        <td><code>-f FILTER</code>, <code>--filter FILTER</code></td>
        <td>Filter lines based on exact match (only matched results will be included</td>
    </tr>
    <tr>
        <td>DPI</td>
        <td><code>-d DPI</code>, <code>--dpi DPI</code></td>
        <td>Set the output DPI for the image to generate (type: integer)(default: 100)</td>
    </tr>
    <tr>
        <td>SVG output format</td>
        <td><code>-s</code>, <code>--svg</code></td>
        <td>Set output to SVG format</td>
    </tr>
    <tr>
        <td>Origin states file</td>
        <td><code>-O</code>, <code>--origin-states</code></td>
        <td>Set the origin-states configuration file</td>
    </tr>    
    <tr>
        <td>Forgery states file</td>
        <td><code>-F</code>, <code>--forgery-states</code></td>
        <td>Set the forgery-states configuration file</td>
    </tr>
    <tr>
        <td>Horizontal seperation</td>
        <td><code>-H</code>, <code>--horizontal-sep</code></td>
        <td>Specify the horizontal seperation between columns (type: float)(default: 2.0)</td>
    </tr>
    <tr>
        <td>Vertical seperation</td>
        <td><code>-V</code>, <code>--vertical-sep</code></td>
        <td>Specify the vertical seperation between rows (type: float)(default: 0.5)</td>
    </tr>
</table>

### Examples
Default run:
```bash
python timestamp_visualizer.py sample-input.txt
```

With filter:
```bash
python timestamp_visualizer.py -f ".\Folder\test2.odt" sample-input.txt
```

## Publication
This tool is a part of the following publication:

* Jelle Bouma, Hugo Jonker, Vincent van der Meer, and Eddy Van Den Aker. 2023. Reconstructing Timelines: From NTFS Timestamps to File Histories. In _The 18th International Conference on Availability, Reliability and Security (ARES 2023), August 29--September 01, 2023, Benevento, Italy._ ACM, New York, NY, USA 9 Pages. https://doi.org/10.1145/3600160.3605027
