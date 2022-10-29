import africastalking as at
api_key = "aaedd80febe6e60d009ea18c8eae0561619c2058bd6bf0ce24d86f12b2c9b4e1"
username = "diabetesproj"
# Initialize the Africas Talking client with the required credentials
at.initialize(username, api_key)
def sendtestmsg():
    number="+254727617870"
    message = "Hello there first test sms"    
    # assign the sms functionality to a variable
    sms = at.SMS
    response=" "
    try:
        response = sms.send(message, [number])
    except:
        print("Message sending failed")
    if response:
        issent = True
    return response
def sendcustomizedsms(recipient,message,issent):
    # assign the sms functionality to a variable
    sms = at.SMS
    response=" "
    try:
        response = sms.send(message, [recipient])
    except:
        print("Message sending failed")
    if response:
        issent = True
    return response,issent
