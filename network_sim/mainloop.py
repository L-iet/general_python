import classes as C

net = C.RandomNetwork(10,20)
n = net.nodes[0]
#net.nodes[1].ip = "192.168.99.99"; net.nodes[1].device_name = "dummy"
g = {"cwd":["base"],
		"current_device":n,
		"whole_network":net,
		"username":"root",
		"BASE_DEVICE":n
	}
'''n.exec_comm("pwd","",g)
n.exec_comm("ls",[],g)
n.exec_comm("cd",["F2"],g)
n.exec_comm("ifconfig","",g)
n.exec_comm("sudo",["arp-scan","-l"],g)
n.exec_comm("sudo",["ssh","192.168.99.99"],g)
n.exec_comm("ifconfig","",g)'''

while True:
	inp = input("\n/" + ("/".join(g["cwd"])) + "/\n"+C.beautify_user(g) + "|>>").strip()
	if inp == "quit_game":
		break
	else:
		comm_l = inp.split()
		if len(comm_l) == 1:
			g["current_device"].exec_comm(comm_l[0], [], g)
		else:
			g["current_device"].exec_comm(comm_l[0],comm_l[1:],g)
