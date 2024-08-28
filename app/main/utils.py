import africastalking as at
api_key = os.environ.get('AT_API_KEY')
username = os.environ.get('AT_USERNAME')
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