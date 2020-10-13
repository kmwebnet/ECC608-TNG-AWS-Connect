# ECC608-TNG-AWS-Connect

This communicates ATECC608A-TNGTLS secure chip from ESP32 and connects to AWS IOT configured for "Multi-Account-Registration"    

for Multi-Account-Registration, check the [AWS website](https://pages.awscloud.com/iot-core-early-registration.html)  

# Requirements

Platformio(PIO Core:5.0.1 PLATFORM: Espressif 32 1.12.4) with VS Code environment.  
install "Espressif 32" platform definition on Platformio  

you need to buy ATECC608A-TNGTLS and prepare downloaded manifest file from Microchip Direct.    
And register them to your AWS Account by using Multi-Account-Registration-enabled AWS CLI prior to use this code.       




# Environment reference
  
  Espressif ESP32-DevkitC  
  this project initialize I2C 1 port   
  pin assined as below:  

      I2C 1 SDA GPIO_NUM_16  
      I2C 1 SCL GPIO_NUM_17  
       
  ATECC608A-TNGTLS(on I2C port 1)   

# Usage  

"git clone --recursive " on your target directory. and you need to change a serial port number which actually connected to ESP32 in platformio.ini.    

move to target directory (where you cloned this project)     

extract device cert from manifest file by using "manifestdecoder.py" python script.
before you use this script, execute pip install python-jose[cryptography] .    
You will find certificate PEM file in "certs" subdirectory.   

Create policy by AWS CLI. Run this only once.      

aws iot create-policy --policy-name wildcardpolicy --policy-document file://wildcardpolicy"   
{
    "policyName": "wildcardpolicy",
    "policyArn": "arn:aws:iot:ap-northeast-1:XXXXXXXXXXXX:policy/wildcardpolicy",
    "policyDocument": "{\n    \"Version\": \"2012-10-17\",\n    \"Statement\": [\n        {\n            \"Effect\": \"Allow\",\n            \"Action\": [\n                \"iot:Connect\",\n                \"iot:Publish\",\n                \"iot:Receive\",\n                \"iot:Subscribe\"\n            ],\n            \"Resource\": [\n                \"*\"\n            ]\n        }\n    ]\n}\n",
    "policyVersionId": "1"
}

Register certificate by AWS CLI.Run for each device.    

aws iot register-certificate-without-ca --certificate-pem file://certs/0123XXXXXXXXXXXX01 --status ACTIVE    
{
    "certificateArn": "arn:aws:iot:ap-northeast-1:XXXXXXXXXXXX:cert/56366869fd...96b05161",
    "certificateId": "56366869fd8....096b05161"
}

aws iot attach-policy --target "arn:aws:iot:ap-northeast-1:XXXXXXXXXXXX:cert/56366869....96b05161" --policy-name wildcardpolicy

Get AWS IoT access endpoint

aws iot describe-endpoint --endpoint-type iot:Data-ATS
{
    "endpointAddress": "XXXXXXXXXX-ats.iot.ap-northeast-1.amazonaws.com"
}

The above authority and role settings are for testing purposes, so please check and change them yourself in the production environment.

replace definitions to your own in main.c    

#define EXAMPLE_WIFI_SSID ""  
#define EXAMPLE_WIFI_PASS ""  

replace definitions to your own in sdkconfig.defaults

CONFIG_AWS_IOT_MQTT_HOST="XXXXXXXXXXXX-ats.iot.ap-northeast-1.amazonaws.com"       

# Run this project

just execute "Upload" on Platformio.   

# License

This software is released under the MIT License, see LICENSE.  
