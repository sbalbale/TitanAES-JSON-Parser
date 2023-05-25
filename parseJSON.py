# importing the module
import json
import matplotlib.pyplot as plt
import gzip



# while True:
#     try:
#         fileName = input("Enter the location of the file: ")
#         with open(fileName) as json_file: # type: ignore
#             data = json.load(json_file)
#         break
#     except (FileNotFoundError):
#         print("The file you are looking for doesn't exist. Please try again.")
#         continue
    
def decompress(infile, tofile):
    with open(infile, 'rb') as inf, open(tofile, 'w', encoding='utf8') as tof:
        decom_str = gzip.decompress(inf.read()).decode('utf-8')
        tof.write(decom_str)
        
while True:
    try:
        fileName = input("Enter the location of the file: ")
        decompress(fileName, "temp.json")
        break
    except (FileNotFoundError):
        print("The file you are looking for doesn't exist. Please try again.")
        continue



# fileName = "TitanAES/LGBD01C1000003_row68_capture278_2023-04-18T17_02_29.json"

# Opening JSON file
with open('temp.json') as json_file: # type: ignore
    data = json.load(json_file)
    
excitationData = data["ExperimentParameters"]["scan_params"]["excitation"]["SignalRaw"]
transmissionData = data["SignalRaw"]["echoesOutput"]["transmission"][0]
reflectionData = data["SignalRaw"]["echoesOutput"]["reflection"][0]
totalTime = data["ExperimentParameters"]["time_window"]

graphData = {
    "excitationData": excitationData,
    "transmissionData": transmissionData,
    "reflectionData": reflectionData
}

#Single Graph
# def createGraph(totalTime, data: list, title, xLabel, yLabel):
#     timeDifference = totalTime / len(data)
#     time = [0]
#     while len(time) < len(data):
#         currentTime = time[-1] + timeDifference
#         time.append(currentTime)
        
#     x = time
#     y = data
#     print (time)
    
#     plt.plot(x,y)
#     plt.title(title)
#     plt.xlabel(xLabel)
#     plt.ylabel(yLabel)
#     plt.show()



# createGraph(totalTime, excitationData, "Excitation Data", "Time", "Amplitude")
# createGraph(totalTime, transmissionData, "Transmission", "Time", "Amplitude")
# createGraph(totalTime, reflectionData, "Reflection", "Time", "Amplitude")

def createTimes(totalTime, data):
    timeDifference = totalTime / len(data)
    time = [0]
    while len(time) < len(data):
        currentTime = time[-1] + timeDifference
        time.append(currentTime)
    return time

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
    
    
createGraph(totalTime, graphData)