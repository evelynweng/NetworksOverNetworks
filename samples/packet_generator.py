#This is the program that generates a message and converts it into a hex string.

#Two imports, codecs and random. Codecs is needed for the conversion, and random is needed to get the amount of NULL messages before and after the message.
import codecs
import random

#Hex values for start of text, end of text, start of heading, end of transmission, and null.
STX = "02"
ETX = "03"
SOH = "01"
EOT = "04"
NULL = "00"

#Function get_userascii that converts a string to hexadecimal.
def get_userascii(user_input):
  format_string =""
  for element in user_input:
    hex(ord(element))
    character_string = format(ord(element), "x")
    format_string = format_string + character_string
  return(format_string)

#Function make_message that determines the number of NULL messages for the front and back of the message.
def make_message(transmitted_string):
  frontnum_NULL = random.randint(1,6)
  backnum_NULL = random.randint(1,6)
  final_string = (frontnum_NULL * NULL) + transmitted_string + (backnum_NULL * NULL)
  return(final_string)

#Main function that recieves the string as an input and creates the final hex string with NULL, STX, ETX, SOH, and EOT messages. The final message is written and saved on a text file called "message.txt".
def main():
  user_string = input("Please input a string to convert: ")
  format_string = get_userascii(user_string)
  framed_string = STX + format_string + ETX
  transmitted_string = (3*SOH) + STX + format_string + ETX + (3*EOT)
  message_string = make_message(transmitted_string)
  f = open("message.txt", "w+")
  f.write(message_string)
  f.close()

main()
