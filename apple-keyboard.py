import urllib
import json
import smtplib


def sendemail(from_addr, to_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header = 'From: Christopher Lee\n'
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Subject: %s\n\n' % ','.join(subject)
    message = header + message

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems


def find_keyboard():
    zipcode = '94103'
    keyboard_url = 'http://store.apple.com/us/retail/availabilitySearch?parts.0=MJYR2LL/A&zip='
    pencil_url = 'http://store.apple.com/us/retail/availabilitySearch?parts.0=MK0C2AM/A&zip='

    keyboard_request = urllib.urlopen(keyboard_url + zipcode)
    pencil_request = urllib.urlopen(pencil_url + zipcode)

    keyboard_data = json.loads(keyboard_request.read())
    pencil_data = json.loads(pencil_request.read())

    keyboard_stores = keyboard_data['body']['stores']
    pencil_stores = pencil_data['body']['stores']

    availability = {
        'Keyboard': {},
        'Pencil': {}
    }
    for store in keyboard_stores:
        is_available = store['partsAvailability']['MJYR2LL/A']['pickupDisplay']
        if is_available != 'unavailable':
            availability['Keyboard'][store['address']['address']] = is_available

    for store in pencil_stores:
        is_available = store['partsAvailability']['MK0C2AM/A']['pickupDisplay']
        if is_available != 'unavailable':
            availability['Pencil'][store['address']['address']] = is_available

    try:
        if availability['Keyboard'] or availability['Pencil']:
            to_addr = ['christopherd.lee@gmail.com']
            from_addr = ['christopherd.lee@gmail.com']
            subject = ['Keyboard Pencil Availability']
            login = 'christopherd.lee@gmail.com'
            password = 'lymzdvjkvkxmubfw'
            message = json.dumps(availability)
            sendemail(to_addr, from_addr, subject, message, login, password)
            print "Email sent!"
    except Exception:
        print 'Failed to send email: ', Exception.message

if __name__ == '__main__':
    find_keyboard()
