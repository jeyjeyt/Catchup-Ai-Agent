import random 

def get_empty_cells(state):
	empty_cells = []
	for cell in state:
		if state[cell] is None:
			empty_cells.append(cell)
	return empty_cells

def random_moves(state,max_stones):
	empty_cells = get_empty_cells(state)
	if not empty_cells or max_stones < 1:
		return []
	how_many = random.randint(1, min(max_stones, len(empty_cells)))
	chosen = random.sample(empty_cells, how_many)
	return chosen
