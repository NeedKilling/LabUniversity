clear()
change_hat(Hats.Brown_Hat)
while True:
	for i in range(get_world_size()): 
		for j in range(get_world_size()):
			
			if can_harvest():
				harvest()
			
			if i%2 == 0:
				if j%2 == 0:
					till()
					plant(Entities.Carrot)
				else:
					if can_harvest():
						harvest()
					else:
						plant(Entities.Tree)
			else: 
				if j%2 == 0:
					if can_harvest():
						harvest()
					else:
						plant(Entities.Tree)
				else:
					till()
					plant(Entities.Carrot)
			
				
			
					
					
			move(North)
			
		move(East)
		
	
