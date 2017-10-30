import RPi.GPIO as GPIO
import dht11
import time
import datetime as datetime
import os

def decide():
    reply = input("Do you want to do a breath test (y/n):")
    str.lower(reply)

    if(reply=='y'):
        return True
    else:
        return False

def breath_test(initial_humid,initial_temp,heat_sensor):
    print("Please provide breath sample")
    time.sleep(5)
    value = heat_sensor.read()

    while(value.is_valid()==False):
        print("Please provide breath sample")
        time.sleep(5)
        value = heat_sensor.read()

    final_humid = value.humidity - initial_humid
    final_temp = value.temperature - initial_temp

    if(final_humid<=0):
        breath_test(initial_humid,initial_temp,heat_sensor)
    else:
        print("Humidity of breath : ", final_humid)
        print("Temperature Change due to breath : ", final_temp)
    return

def HI_condition(HI):

    if (HI<80):
        print("GOOD # Room is comfortable")
    elif(HI>=80 and HI<90):
        print("CAUTION # Fatigue with prolonged exposure to this index")
    elif (HI >= 90 and HI < 103):
        print("DANGER # Heat cramps or heat exhaustion likely. Prolonged exposure results heat stroke")
    else:
        print("EXTREME DANGER # Heat Stroke imminent")
    return


def sensor_data(dict_item):

    led = 7
    heat_switch = 11
    value = 0

    # operating temperature in fahrenheit
    #general
    lowLimit_gen = 32
    upLimit_gen = (70*9/5)+32

    # phone
    lowLimit_phone = 32
    upLimit_phone = 95

    # computer
    lowLimit_computer = 25
    upLimit_computer = 100

    #tv
    lowLimit_tv = 25
    upLimit_tv = 100

    #humidity
    lowLimit_humid = 30
    upLimit_humid = 50

    GPIO.setmode(GPIO.BOARD)  # GPIO.BCM

    GPIO.setup(heat_switch, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # last parameter is activating the pull up resistors inside the switch
    GPIO.setup(led, GPIO.OUT)

    # initialize sensor
    heat_sensor = dht11.DHT11(pin=heat_switch)


    try:
        value = heat_sensor.read()

        while(value.is_valid() == False):
            value = heat_sensor.read()


        if value.is_valid():
            f_temp = (value.temperature * 9 / 5) + 32
            t = datetime.datetime.today()
            initial_humid = value.humidity
            initial_temp = value.temperature

            GPIO.output(led, 1)

            print("************************")
            if(decide()):
                breath_test(initial_humid,initial_temp,heat_sensor)
            else:
                print("Breathe test rejected")
            print("************************")

            print("************************")
            print("Recorded time : ", datetime.datetime.now())
            print("Temperature(C) : ", value.temperature, "C")
            print("Temperature(F) : ", f_temp, "F")
            print("Humidity : ", initial_humid)
            print("************************")

            with open("temp&humidity.txt", mode="a+", encoding="utf-8") as file_obj:
                file_obj.write(
                    "Date : " + t.strftime('%m/%d/%Y') + ",Temperature(C) : " + str(value.temperature) + ",Humidity : " + str(value.humidity) + "\n")

            time.sleep(1)

            # temperature comparisons
            # phone
            print("************************")
            if(dict_item['phone']==0 and dict_item['computer']==0 and dict_item['tv']==0 and dict_item['other']==0):
                print("There are no devices in the room")
            if(dict_item['phone']>0):

                if (f_temp >= lowLimit_phone and f_temp <= upLimit_phone):
                    print("Room suitable for mobile phone")
                else:
                    print("Room NOT suitable for mobile phone")

            # computer
            if (dict_item['computer'] > 0):

                if (f_temp >= lowLimit_computer and f_temp  <= upLimit_computer):
                    print("Room suitable for computer")
                else:
                    print("Room NOT suitable for computer")

            #tv
            if (dict_item['tv'] > 0):

                if (f_temp  >= lowLimit_tv and f_temp <= upLimit_tv):
                    print("Room suitable for tv")
                else:
                    print("Room NOT suitable for tv")
            if (dict_item['other'] > 0):

                if (f_temp  >= lowLimit_gen and f_temp <= upLimit_gen):
                    print("Room suitable for other appliances")
                else:
                    print("Room NOT suitable for other appliances")
            print("************************")

            #heat index
            if(f_temp<80):
                HI = 0.5 * (f_temp + 61.0 + ((f_temp - 68.0) * 1.2) + (value.humidity * 0.094))
            else:
                HI = -42.379 + 2.04901523 * f_temp + 10.14333127 * value.humidity - .22475541 * f_temp * value.humidity- .00683783 * f_temp* f_temp- .05481717 * value.humidity* value.humidity+ .00122874 * f_temp* f_temp* value.humidity+ .00085282 * f_temp* value.humidity* value.humidity- .00000199 * f_temp* f_temp* value.humidity* value.humidity

            print("************************")
            print("Heat Index : {:.2f} ".format(HI))

            HI_condition(HI)

            if (initial_humid >= lowLimit_humid and initial_humid<= upLimit_humid):
                print("Room has comfortable humidity")
            elif(initial_humid<lowLimit_humid):
                print("Room has LESS humidity")
            else:
                print("Room has HIGH humidity")

            print("************************")

        else:
            GPIO.output(led, 0)

    except Exception as error:
        print("There were some technical difficulties : ",error)
    finally:
        print("Ending program")
        GPIO.cleanup()
        return


def u_interf():
    print("Welcome to Device health")

    phone = int(input("Please specify the number of phones in location : "))
    computer = int(input("Please specify the number of computers in location : "))
    tv = int(input("Please specify the number of tvs in location : "))
    other = int(input("Please specify the number of other devices in location : "))

    myDict = {}
    myDict["phone"] = phone
    myDict["computer"] = computer
    myDict["tv"] = tv
    myDict["other"] = other

    return myDict



def main():
    dev_dict = u_interf()

    sensor_data(dev_dict)


'''
    print("Phone : ",dev_list.pop())
    print("Computer : ", dev_list.pop())
    print("TV : ", dev_list.pop())
    print("Other_Appliance : ", dev_list.pop())
'''


main()


