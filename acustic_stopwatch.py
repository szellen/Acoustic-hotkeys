import requests
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import pyautogui 

pyautogui.FAILSAFE = False
#phyphox configuration
PP_ADDRESS = "http://192.168.0.11:8080"
PP_CHANNELS = ["tindex","tlist"]
# tlist: time in sequnse
# tindex: number of tap
# last: time when last tap happens

#global var to save timestamp
xs = []

# global array to save acceleration
i =[]
i2 =[]


def getSensorData():
    url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
    data = requests.get(url=url).json()
    i = data["buffer"][PP_CHANNELS[0]]["buffer"][0]
    i2 = data["buffer"][PP_CHANNELS[1]]["buffer"][0]
    return [i,i2]
    
    
def getData():
    [ni,ni2] = getSensorData() # get nth sample
    i.append(ni)
    i2.append(ni2)
    return [ni,ni2]
    
def main():
    index = 0
    start_time = 0.0
    ni2 = 0.0
    interval_type_list = ['N','N','N'] # with two dummy node

    while True:
      [ni,ni2] = getData()

      if ni2 is None or len(interval_type_list) > 200: # reset when clicked 'reset' buttor or when the data gets too large
          ni2 = 0.0
          ni = 0
          interval_type_list = ['N','N','N'] #reset the list

      if (ni != index): #detect new tap
          
          interval = round(ni2-start_time,3)
          interval_type = intervalDetection(interval)
          interval_type_list.append(interval_type)
        
        #   print (ni, interval, interval_type, interval_type_list)
          index = ni
          start_time = ni2
        
          commandDetection(interval_type_list)



def intervalDetection(interval):
    """Determine type of interval,
    paraeter interval: time between two acustic events in sec
    S --> short interval ranging 0.1 - 0.3 sec
    L --> long interval ranging 0.3 - 0.9 sec
    N --> interval is either too long or too short and considered as noise
    """
    if interval > 0.01 and interval < 0.25: # short gap
        return 'S'
    elif interval > 0.25 and interval < 0.6: # long gap
        return 'L'
    else: 
        return 'N' 

def commandDetection(interval_type_list):
    """Detect pattern from the given interval type list
    """
    num = len(interval_type_list)

    pattern = ""
    pattern = pattern.join(interval_type_list[num-4:num])
    # print (pattern)
    switcher = {
        "NSSS":one,
        "NLSS":two,
        "NSLS":three,
        "NSSL":four
    }
    func = switcher.get(pattern, lambda:"")
    print (func())


def one():
    pyautogui.hotkey("ctrl", "a") 
    return "- - - -"
def two():
    pyautogui.hotkey("ctrl", "c") 
    return "-    - - -"
def three():
    pyautogui.hotkey("ctrl", "z") 
    return "- -    - -"
def four():
    pyautogui.hotkey("ctrl", "v") 
    return "- - -    -"
if __name__ == '__main__':
    main()


