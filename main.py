from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Replace these with your Twilio account details
ACCOUNT_SID = 'ACe8af6e2da44c8303a2255a903d88b532'
AUTH_TOKEN = '9b3de29a7d1737f4ce948491a0fd2d1a'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # This is the Twilio sandbox number

# Initialize the Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    # Get JSON data from the request
    data = request.get_json()

    # Get 'message' and 'to' from the request data
    message_body = data.get('message')
    to_phone_number = data.get('to')

    if not message_body or not to_phone_number:
        return jsonify({'error': 'Message and destination phone number are required'}), 400

    try:
        # Send the WhatsApp message using Twilio
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_phone_number}'
        )

        # Build response_details dynamically
        response_details = {
          'status': 'Message sent',
          'message_sid': getattr(message, 'sid', None),
          'date_created': getattr(message, 'date_created', None),
          'date_sent': getattr(message, 'date_sent', None),
          'date_updated': getattr(message, 'date_updated', None),
          'to': getattr(message, 'to', None),
          'from': getattr(message, 'from_', None),
          'body': getattr(message, 'body', None),
          'status': getattr(message, 'status', None),
          'direction': getattr(message, 'direction', None)
        }

        # Remove keys with None values
        response_details = {k: v for k, v in response_details.items() if v is not None}

        # Return the detailed response
        return jsonify(response_details), 200

    except Exception as e:
        # Return an error response
        return jsonify({'status': 'Failed to send message', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
