#This is the program that takes the final message from the generator and converts it back to a string.

#Opens the file message.txt and expects to read the message.
encoded_file = open("message.txt", "r")
encoded_line = encoded_file.read().replace("\n", " ")

#Finds out where the actual message is within the NULL, STX, ETX, SOH, and EOT messages.
encoded_message_front = encoded_line.find("02")
encoded_message_back = encoded_line.find("03")
final_message = encoded_line[encoded_message_front + 2:encoded_message_back]

#Converts hexadecimal back into the original message.
print(bytes.fromhex(final_message).decode('utf-8'))
