def ParseNetDev(file):
    lines = open(file, "r").readlines()
    columnLine = lines[1]
    _, receiveCols , transmitCols = columnLine.split("|")
    receiveCols = map(lambda a:"recv_"+a, receiveCols.split())
    transmitCols = map(lambda a:"trans_"+a, transmitCols.split())

    cols = receiveCols+transmitCols

    faces = {}
    for line in lines[2:]:
        if line.find(":") < 0: continue
        face, data = line.split(":")
        faceData = dict(zip(cols, data.split()))
        faces[face] = faceData

    return faces

def GetNetData(data_dir, snet_file, enet_file):
    netfile = data_dir + "/" + snet_file 
    sfaces = ParseNetDev(netfile)
    netfile = data_dir + "/" + enet_file 
    efaces = ParseNetDev(netfile)

    recv_bytes = 0
    transmit_bytes = 0
    #print efaces.keys()
    for key in efaces.keys():
        #print("recv_bytes", efaces[key]["recv_bytes"])
        #print("recv_bytes", sfaces[key]["recv_bytes"])
        recv_bytes+=(float(efaces[key]["recv_bytes"])-float(sfaces[key]["recv_bytes"]))
    for key in efaces.keys():
        transmit_bytes+=(float(efaces[key]["trans_bytes"])-float(sfaces[key]["trans_bytes"]))
        
    print("Recv Megabytes, transmit Megabytes", recv_bytes/(1024 * 1024), transmit_bytes/(1024 * 1024))
    return (recv_bytes/(1024 * 1024), transmit_bytes/(1024 * 1024))



## Use like
  #      net_data = GetNetData(data_dir, snet_file, enet_file)
