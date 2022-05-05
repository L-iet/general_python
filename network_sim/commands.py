commands = {"cat","echo","ls","sudo","pwd","cd","chdir","whoami","logout","ifconfig"}
commands_opts = {"ls":{"-la","-l"}, "sudo":{"su","ssh", "login","arp-scan"}}
def parse_input(inp):
	inp = inp.split()
	if inp[0] not in commands:
		print(f"Command '{inp[0]}' not found.")
	else:
		pass
		#execute commands






