import time
from random import randrange
import paho.mqtt.client as mqtt
from cryptography.fernet import Fernet


def on_connect(client, userdata, flags, r_c):
    """Check connection"""
    if r_c == 0:
        print("Connected")
    else:
        print("Not connected")


def on_message(client, userdata, message):
    """On receiving new message:
    Decrypt message, convert to integer, display to user the units and
    set msgflag to True for handling running total (without resetting to 0)
    then kick off publish function"""
    decrypted_message = cipher.decrypt(message.payload)
    msg = int(decrypted_message.decode("utf-8"))
    print("Unit Total from Server = ", str(decrypted_message.decode("utf-8")))
    pub(client, TOPIC1, msg, QOSS)


def sub(client, topic, qos):
    """Subscribe to TOPIC2"""
    client.subscribe(topic, qos)


def pub(client, topic, msg, qos):
    """Publish encrypted unit total (simulated by adding a random numer)"""
    msg = msg + randrange(10)
    message = str(msg)
    encrypted_message = cipher.encrypt(message.encode())
    out_message = encrypted_message.decode()
    client.publish(topic, out_message, qos, True)
    time.sleep(4)


QOSS = 1
BROKER = 'broker.emqx.io'
TOPIC1 = "UNITS1221"
TOPIC2 = "UNITS1222"
PORT = 1883
CIPHER_KEY = b'70JZaJg4c5F7RIOhrSXNjq0Y0iGp1QtBy2gyVMSdHHY='
cipher = Fernet(CIPHER_KEY)


client = mqtt.Client("Smart_Meter")
client.connect(BROKER, PORT)
client.on_connect = on_connect
client.on_message = on_message
sub(client, TOPIC2, QOSS)

while True:
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
