import spidev
import MFRC522

# Create an instance of the MFRC522 class
MIFAREReader = MFRC522.MFRC522()

# Loop continuously to read from the RFID RC522 module
while True:
    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected!")

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If the UID is read successfully
        if status == MIFAREReader.MI_OK:
            # Print the UID in hexadecimal format
            print("Card UID: " + ":".join([format(x, "02x") for x in uid]))

            # Halt the card to stop further operations
            MIFAREReader.MFRC522_Halt()

