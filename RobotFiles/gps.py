from gps3 import gps3
def getLoc(samples):
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()


    data = []
    i = 0
    errorCount = 0
    for new_data in gps_socket:
        
        if i == samples:
            break
        if errorCount == 10:
            print("ERROR: NO FIX")
            break
        if new_data:
            data_stream.unpack(new_data)
            lat = data_stream.TPV['lat']
            lon = data_stream.TPV['lon']
            if lat == 'n/a':
                errorCount += 1
                continue
            data.append((lat,lon ))
            i+= 1
            
    return data

