from flask import Flask, request, jsonify
import pywhatkit as kit
import time

app = Flask(__name__)

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    data = request.get_json()
    message_body = data.get('message')
    to_phone_number = data.get('to')

    if not message_body or not to_phone_number:
        return jsonify({'error': 'Message and destination phone number are required'}), 400

    try:
        now = time.localtime()
        send_hour = now.tm_hour
        send_minute = now.tm_min + 1
        if send_minute >= 60:
            send_minute -= 60
            send_hour += 1

        if send_minute == now.tm_min:
            send_minute += 1

        kit.sendwhatmsg(to_phone_number, message_body, send_hour, send_minute, 15)

        return jsonify({'status': 'Message scheduled', 'to': to_phone_number, 'message': message_body}), 200

    except Exception as e:
        return jsonify({'status': 'Failed to send message', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
