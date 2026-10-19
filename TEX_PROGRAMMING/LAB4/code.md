clear()
change_hat(Hats.Brown_Hat)
X_START, X_END = 1, 6
Y_START, Y_END = 1, 6

while True:
	for i in range(get_world_size()): 
		for j in range(get_world_size()):
			
			if can_harvest():
				harvest()
			
			
			if X_START <= i <= X_END and Y_START <= j <= Y_END:
				till()
				plant(Entities.Pumpkin)
			
			else:
				
				if i%2 == 0:
					if j%2 == 0:
						till()
						plant(Entities.Carrot)
						use_item(Items.Fertilizer)
					else:
						if can_harvest():
							harvest()
							till()
						else:
							plant(Entities.Tree)
				else: 
					if j%2 == 0:
						if can_harvest():
							harvest()
							till()
						else:
							plant(Entities.Tree)
					elif j%3 == 0:
						if can_harvest():
							harvest()
						else:
							till()
							plant(Entities.Sunflower)
					else:
						till()
						plant(Entities.Carrot)
			
				
			
					
					
			move(North)
			
		move(East)
		
	
		