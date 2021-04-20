import json
http = ( "put","options", "connect", "get", "head", "post", "delete"
         , "patch", "trace")
logging = ("debug", "info", "error", "warning", "error", "critical")





def create():
      webserverName=input("Please enter file name")
      httpName=input("Please enter the name of the http request method")
      while httpName.lower() not in http:
            print(f"Incorrect value. Values available: {http}")
            httpName = input("Please correct the name of the http request method")
      logLevel=input("Please enter logging level")
      while logLevel.lower() not in logging:
            print(f"Incorrect value. Values available: {logging}")
            logLevel = input("Please correct the logging level")
      numOfLines=int(input("Please enter number of log lines to display"))
      while numOfLines <=0 :
            print(f"Incorrect value, must be bigger than 0")
            numOfLines = input("Please correct the number of lines")
      additional=input("Please enter website adress you are looking for")



      data={"webserverName":webserverName,
      "httpName":httpName,
      "logLevel":logLevel,
      "numOfLines":numOfLines,
      "ownParameter": additional}

      with open('configFile.json', 'w') as file:
            json.dump(data, file)

if __name__ == '__main__':
      create()