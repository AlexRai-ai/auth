import requests

def send_sms_otp(mobile_number, otp):
  # Configuration details
  api_uri = 'https://www.smsidea.co.in/smsstatuswithid.aspx'
  registered_mobile = 'your mobile'
  password = 'Qyour password'
  sender_id = 'your sender id'
  template_id = 'your template id'  # Template ID for OTP message

  # Validate mobile number format
  if not mobile_number.isdigit() or len(mobile_number) != 10:
      print("Invalid mobile number format")
      return False

  # Construct the message
  message = f"Your OTP to register is {otp}. Enter within 5 mins to verify your account with The Secretariat."

  # Prepare the payload for the API request
  payload = {
      'mobile': registered_mobile,  # Your registered mobile number with the SMS service
      'pass': password,
      'senderid': sender_id,
      'to': mobile_number,
      'msg': message,
      'template_id': template_id,
  }

  try:
      # Send the request to the SMS API
      response = requests.get(api_uri, params=payload)
      print(f"Request URL: {response.url}")  # Log the request URL
      print(f"Response Status Code: {response.status_code}")  # Log the status code
      print(f"Response Text: {response.text}")  # Log the response text
      return response.status_code == 200 and "error" not in response.text.lower()
  except requests.exceptions.RequestException as e:
      print(f"Error sending SMS: {e}")
      return False

# Example usage
otp = 123456  # Example OTP
mobile_number = "9876543210"  # Example mobile number

if send_sms_otp(mobile_number, otp):
  print("OTP sent successfully")
else:
  print("Failed to send OTP")
