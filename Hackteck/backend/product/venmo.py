from venmo_api import Client



@app.route('/venmo', methods=['POST'])
def venmoLogin():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Get your access token. You will need to complete the 2FA process
    access_token = Client.get_access_token(username=email,
                                        password=password)
    venmo = Client(access_token=access_token)


def venmoSend():
    value = request.json.get('value', None)
    note = request.json.get('note', None)
    username = request.json.get('username', None)

    # Send a payment to a user
    payment = venmo.payment.request_money(value, note, user_id)

def venmoRequest():
    value = request.json.get('value', None)
    note = request.json.get('note', None)
    username = request.json.get('username', None)
    # Request money from a user
    payment = venmo.payment.request_money(1.00, note, username)