# User Interface

class Service_send_message():
	def message_service(self, mylabel):
		to_label   = input("This message is for? (#label:)")
		to_message = input("please enter your message: ")
		return to_label+','+str(mylabel)+','+to_message


if __name__ == "__main__":
	# Do some unit test
	pass