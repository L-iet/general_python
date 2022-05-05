import random
import os

sm = [chr(x) for x in range(97,123)]
upp = [chr(x) for x in range(65,91)]
digits = [str(x) for x in range(10)]
syms = ["@","#","!","$","&","*","?"]

def last_part_of_ip(ip):
	return ip.split('.')[-1]
def beautify_user(g):
	return f"~{last_part_of_ip(g['current_device'].ip)}:{g['username']}"
class Node(object):
	"""Node is a device"""
	def __init__(self, n, ip):
		self.device_name = n
		self.ip = ip
		last_ip = last_part_of_ip(self.ip)
		if last_ip in [0, 255]:
			self.device_type = "Router"
		else:
			self.device_type = random.choice(["PC","PC","PC","PC","PC","PC","PC","Server","Router","Router"])
		self.files = {"base":{"root":{"bin":{}, "bin2":{}, "bin3":{"f1":{},"F2":{"ff1.txt": "ff1 contents", "_hidden_file.txt":"hidden file contents"}}, "some_otherfile.txt":"some other file contents"}, "root_file.txt":"root file contents"}, "filename.txt":"file contents"}
		self.users = {"root":"root_password","username":"password"}
		self.basic_user = "root"
	def __eq__(self,other):
		return self.device_name == other.device_name and self.files is other.files ##Checks if they are identical in memory
	def __str__(self):
		return f"Node({self.device_name})"
	def __repr__(self):
		return f"Node({self.device_name})"

	def exec_comm(self,comm, opts, game_state):
		cwd = game_state["cwd"]
		#entering the cwd
		cwd_ = self.files
		for foldername in cwd:
			cwd_ = cwd_[foldername]

		if game_state["username"] != "root":
			if comm in {"arp-scan", "su", "ssh","login"}:
				print("Command not found.")
				return

		if comm == "cat":
			if not opts:
				print("Usage: cat filename.txt")
				return
			fname = opts[0]

			if fname:
				if fname in cwd_ and "." in fname: print( cwd_[fname] )
				elif not "." in fname: print("Not a file")
				else: print("No such file.")
			else:
				print("Filename not provided")
		elif comm == "echo":
			if not opts:
				print("Usage: echo > filename.txt; echo >> filename.txt; echo some_text > filename.txt; echo some_text")
				return
			if opts[0] == ">":
				fname = opts[1]
				if not '.' in fname: fname += '.txt'
				cwd_[fname] = "ECHO by Joshua Mark"
			elif opts[0] == ">>":
				fname = opts[1]
				if not '.' in fname: fname += '.txt'
				cwd_[fname] = cwd_.get(fname,"") + "\nECHO by Joshua Mark"
			else:
				if len(opts) == 1:
					print(opts[0])
				elif ">" in opts:
					ind = opts.index(">")
					fname = opts[ind+1]
					if not '.' in fname: fname += '.txt'
					cwd_[fname] = ' '.join(opts[:ind])
				elif ">>" in opts:
					ind = opts.index(">>")
					fname = opts[ind+1]
					if not '.' in fname: fname += '.txt'
					cwd_[fname] = cwd_.get(fname,"") + "\n" + " ".join(opts[:ind])
		elif comm == "ls":
			if (not opts) or opts[0] == "":
				print(*([x for x in cwd_ if not x.startswith("_")]),sep="\n")
			elif opts[0] == "-l":
				vis_files = [x for x in cwd_ if not x.startswith("_")]
				l_to_print = list(zip(vis_files, [( str(len(cwd_[x])) +"B" if '.' in x else '') for x in vis_files]))
				l_to_print = [(".",""),("..","")]+ l_to_print
				for x in l_to_print:
					print(*x)
			elif opts[0] == "-la":
				l_to_print = list(zip(list(cwd_), [(str(len(cwd_[x])) +"B" if '.' in x else '') for x in cwd_]))
				l_to_print = [(".",""),("..","")]+ l_to_print
				for x in l_to_print:
					print(*x)

		elif comm == "sudo":
			username = game_state["username"]
			passw = input("Enter root password: ") #get_pass() #need get_pass here
			hash_root_passw = self.users["root"] #I'll actually be storing the hashes here
			if passw == hash_root_passw: #hash(passw) instead of passw
				#success
				c = opts[0]
				if c == "su":
					if username != "root": 
						game_state["username"] = "root"
				elif c == "ssh":
					node_id = opts[1]
					nodes_by_ip = game_state["whole_network"].nodes_by_ip
					nodes_by_name = game_state["whole_network"].nodes_by_name
					if node_id.isalnum():
						for node_name in nodes_by_name:
							if node_name == node_id:
								game_state["current_device"] = nodes_by_name[node_name]
								game_state["username"] = nodes_by_name[node_name].basic_user
								return nodes_by_name[node_name] #return the node we are now at
					elif [int(x) for x in node_id.split(".")]: #shitty way to check if it is in ip format
						for node_ip in nodes_by_ip:
							if node_ip == node_id:
								game_state["current_device"] = nodes_by_ip[node_ip]
								game_state["username"] = nodes_by_ip[node_ip].basic_user
								return nodes_by_ip[node_ip] #return the node we are now at


				elif c == "login":
					new_user = opts[1]
					u_pass = self.users[new_user]
					passw = input(f"Enter password for {new_user}: ") #get_pass()
					if passw == u_pass:
						#success
						game_state["username"] = new_user
						#we are now the new user
					else:
						print("Incorrect Password.")
						#maybe modify here to count how many times and lockout
				elif c == "arp-scan":
					net = game_state["whole_network"]
					#for now, just print all devices
					if len(opts) == 1:
						for dev in net.nodes_by_name:
							print(dev)
					elif opts[1] == "-l":
						print("Device Name     IP Address")
						l1 = [n.rjust(11) for n in net.nodes_by_name]
						l2 = [n.rjust(14) for n in net.nodes_by_ip]
						for dev in zip(l1, l2):
							print(*dev)
					elif opts[1] == "-la":
						print("Device Name|     IP Address| Device Type|")
						l1 = [n.rjust(11)+"|" for n in net.nodes_by_name]
						l2 = [n.rjust(14)+"|" for n in net.nodes_by_ip]
						l3 = [(net.nodes_by_name[n].device_type).rjust(11)+"|" for n in net.nodes_by_name]
						for dev in zip(l1, l2, l3):
							print(*dev)
		elif comm == "pwd":
			print("/"+ ("/".join(game_state["cwd"]) + "/"))
		elif comm == "cd" or comm == "chdir":
			
			if not opts:
				print("Usage: cd foldername")
				return
			fname = opts[0]

			if fname not in {"",".."}:
				if fname in cwd_ and "." not in fname:
					game_state["cwd"].append(fname)
					return
				else:
					print("Not a valid directory.")
			elif fname:
				game_state["cwd"] = game_state["cwd"][:-1]
				return
		elif comm == "whoami":
			print(game_state["username"])
			return
		elif comm == "logout":
			game_state["username"] = "root"
			game_state["current_device"] = game_state["BASE_DEVICE"]
			return
		elif comm == "ifconfig":
			print("....",game_state["current_device"].ip,".....")
			return

		elif comm == "clear":
			os.system("cls") if os.name == "nt" else os.system("clear")



		else:
			print("Command not found.")
			return




class Edge(object):
	"""Edge joins 2 nodes"""
	def __init__(self, node1, node2,weight=1):
		self.nodes = [node1,node2]
		self.weight = weight
	def __eq__(self,other):
		return self.nodes[0] == other.nodes[0] and self.nodes[1] == other.nodes[1]
	def __str__(self):
		return f"Edge({self.nodes[0].device_name}, {self.nodes[1].device_name})"
	def __repr__(self):
		return f"Edge({self.nodes[0].device_name}, {self.nodes[1].device_name})"

class RandomNetwork(object):
	"""Network of devices"""
	def __init__(self,N_NODES,N_EDGES,directed=False):
		ipx = ["192.168.10."+str(x) for x in range(256)]
		self.ips = random.sample(ipx,k=N_NODES)
		self.nodes_by_name = {}; self.nodes_by_ip = {}
		if (not directed and N_EDGES > (N_NODES*(N_NODES-1)/2)) or (directed and N_EDGES > (N_NODES * (N_NODES-1))):
				raise ValueError("Required edges above maximum possible edges")
		
		self.nodes = []
		for i in range(N_NODES):
			dev_name = create_random_str()
			if i == 1:
				node1 = Node("dummy","192.168.99.99")
				self.nodes_by_name["dummy"] = node1
				self.nodes_by_ip["192.168.99.99"] = node1
			else:
				node1 = Node(dev_name,self.ips[i])
				self.nodes_by_name[dev_name] = node1
				self.nodes_by_ip[self.ips[i]] = node1
			self.nodes.append(node1)
			

		self.edges = []
		for i in range(N_EDGES):
			if not self.edges:
				n1 = random.choice(self.nodes)
				n2 = random.choice(self.nodes)
				while n1 == n2:
					n2 = random.choice(self.nodes)
				edge = Edge(n1,n2)
				self.edges.append(edge)
				continue
			while (edge in self.edges or (Edge(*(edge.nodes[::-1])) in self.edges) if not directed else False):
				n1 = random.choice(self.nodes)
				n2 = random.choice(self.nodes)
				while n1 == n2:
					n2 = random.choice(self.nodes)
				edge = Edge(n1,n2)
			self.edges.append(edge)


def create_random_str(length=10,passw=False):
	if not passw:
		return ''.join(random.choices(sm+upp+digits,k=length))


if __name__ == '__main__':
	pass
