import cmd

class FestivalCommand(cmd.Cmd, object):
	"""Command interpreter for python festival-client"""

	def __init__(self, festival_client):
		super(FestivalCommand, self).__init__()

		self.prompt = "festival> "
		self.festival_client = festival_client

	def do_EOF(self, line):
		print("")
		return True

	def do_quit(self, line):
		return True

	def do_exit(self, line):
		return self.do_quit(line)

	def emptyline(self):
		pass

	def default(self, line):
		# Ignoring audio responses for now
		scheme_responses, audio_responses = self.festival_client.send_message(line)
		for scheme_response in scheme_responses:
			print(scheme_response)
