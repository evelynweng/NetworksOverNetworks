import codecs
import random


class Serialization():
    """
    All of the codes are directly taken from professor's son, all credits to
    his son. I just make some restructure.
    """
    _STX = "02"
    _ETX = "03"
    _SOH = "01"
    _EOT = "04"
    _NULL = "00"
    # Function get_userascii that converts a string to hexadecimal.

    def get_userascii(self, user_input):
        format_string = ""
        for element in user_input:
            hex(ord(element))
            character_string = format(ord(element), "x")
            format_string = format_string + character_string
        return format_string

    def make_message(self, transmitted_string):
        frontnum_NULL = random.randint(1, 6)
        backnum_NULL = random.randint(1, 6)
        final_string = (frontnum_NULL * self._NULL) + \
            transmitted_string + (backnum_NULL * self._NULL)
        return final_string

    def serialize(self, input_str):
        format_string = self.get_userascii(input_str)
        framed_string = self._STX + format_string + self._ETX
        transmitted_string = 3*self._SOH + self._STX + format_string + self._ETX
        + 3*self._EOT
        message_string = self.make_message(transmitted_string)

        return message_string
