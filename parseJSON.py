# importing the module
import json
import matplotlib.pyplot as plt
import gzip

    # """
    # This function decompresses a gzip file and writes the decompressed content to a new file.
    # :param infile: The path to the input file that needs to be decompressed. It should be a binary file
    # that has been compressed using gzip compression
    # :param tofile: The parameter "tofile" is a string representing the name of the file that the
    # decompressed data will be written to
    # """
def decompress(infile, tofile):
   
    with open(infile, 'rb') as inf, open(tofile, 'w', encoding='utf8') as tof:
        decom_str = gzip.decompress(inf.read()).decode('utf-8')
        tof.write(decom_str)
        
# This code block is prompting the user to enter the location of a file. It then attempts to
# decompress the file using the `decompress` function defined earlier in the code. If the file is not
# found, it prints an error message and prompts the user to try again. This process continues until a
# valid file location is entered and successfully decompressed.
while True:
    try:
        fileName = input("Enter the location of the file: ")
        decompress(fileName, "temp.json")
        break
    except (FileNotFoundError):
        print("The file you are looking for doesn't exist. Please try again.")
        continue

# Opening JSON file
# This code block is opening a JSON file named "temp.json" and loading its contents into a Python
# dictionary named `data`. The `with` statement is used to ensure that the file is properly closed
# after its contents have been read. The `json.load()` method is used to parse the JSON data from the
# file and convert it into a Python dictionary. The `# type: ignore` comment is used to suppress a
# type checking warning that may be raised by some Python linters.
with open('temp.json') as json_file: # type: ignore
    data = json.load(json_file)
    
# These lines of code are extracting specific data from a JSON file and storing it in variables.
excitationData = data["ExperimentParameters"]["scan_params"]["excitation"]["SignalRaw"]
transmissionData = data["SignalRaw"]["echoesOutput"]["transmission"][0]
reflectionData = data["SignalRaw"]["echoesOutput"]["reflection"][0]
totalTime = data["ExperimentParameters"]["time_window"]

# `graphData` is a dictionary that stores the different types of data needed to create the graphs. The
# keys of the dictionary are the names of the data types, and the values are the actual data arrays.
# In this case, the three types of data are "excitationData", "transmissionData", and
# "reflectionData", and their corresponding values are the arrays `excitationData`,
# `transmissionData`, and `reflectionData` that were extracted from the JSON file.
graphData = {
    "excitationData": excitationData,
    "transmissionData": transmissionData,
    "reflectionData": reflectionData
}

# """
# The function creates a list of evenly spaced time intervals based on the total time and the number
# of data points.

# :param totalTime: The total time available for the data to be spread across
# :param data: The data parameter is a list of values for which we want to create corresponding time
# values. These values could represent anything, such as measurements taken at different times or
# events occurring at different intervals
# :return: a list of time values that are evenly spaced based on the total time and the number of data
# points provided.
# """
def createTimes(totalTime, data):
    
    timeDifference = totalTime / len(data)
    time = [0]
    while len(time) < len(data):
        currentTime = time[-1] + timeDifference
        time.append(currentTime)
    return time

# """
# This function creates a graph with three subplots for excitation, transmission, and reflection data.

# :param totalTime: The total time of the data being plotted, in microseconds (μs)
# :param data: The data parameter is a dictionary containing three keys: "excitationData",
# "transmissionData", and "reflectionData". The values for each key are lists of amplitude values for
# the corresponding data type. The totalTime parameter is the total time duration for the data
# :type data: dict
# """
#Multiple Graphs
def createGraph(totalTime, data: dict):
    
    # Placing the plots in the plane
    
    plot1 = plt.subplot2grid((3, 3), (0, 0),colspan=3)
    plot2 = plt.subplot2grid((3, 3), (1, 0),colspan=3)
    plot3 = plt.subplot2grid((3, 3), (2, 0),colspan=3)
    
    # Make x values
    xexcitationData = createTimes(totalTime, data["excitationData"])
        
    xTransmissionData = createTimes(totalTime, data["transmissionData"])
    
    xReflectionData = createTimes(totalTime, data["reflectionData"])
    
    # Plot for Excitation Data
    plot1.plot(xexcitationData, data["excitationData"])
    plot1.set_title("Excitation Data")
    plot1.set_xlabel("Time (μs)")
    plot1.set_ylabel("Amplitude (V)")
    
    # Plot for transmission data
    plot2.plot(xTransmissionData, data["transmissionData"])
    plot2.set_title("Transmission Data")
    plot2.set_xlabel("Time (μs)")
    plot2.set_ylabel("Amplitude (mV)")
    
    # Plot for reflection data
    plot3.plot(xReflectionData, data["reflectionData"])
    plot3.set_title("Reflection Data")
    plot3.set_xlabel("Time (μs)")
    plot3.set_ylabel("Amplitude (mV)")
    
    # Packing all the plots and displaying them
    plt.tight_layout()
    plt.show()
    
    
# The `createGraph(totalTime, graphData)` function is creating a graph with three subplots for
# excitation, transmission, and reflection data. It takes in two parameters: `totalTime`, which is the
# total time of the data being plotted in microseconds, and `graphData`, which is a dictionary
# containing three keys: "excitationData", "transmissionData", and "reflectionData". The values for
# each key are lists of amplitude values for the corresponding data type. The function uses the
# `createTimes()` function to create a list of evenly spaced time intervals based on the total time
# and the number of data points, and then plots the data on three subplots using Matplotlib.
createGraph(totalTime, graphData)