class Deserialization():

    """
     this class does data deserializing
    """

    def deserialize(self, input_str):
        encoded_message_front = input_str.find("02")
        encoded_message_back = input_str.find("03")
        final_message = input_str[encoded_message_front +
                                  2:encoded_message_back]
            
        
        return bytes.fromhex(final_message).decode('utf-8')
