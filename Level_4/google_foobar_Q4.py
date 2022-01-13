from collections import defaultdict

def findNegativePath(adj_matrix):
	node_length = len(adj_matrix)

	dist_mat = [
		[v for v in adj_matrix[i]]
		for i in range(node_length)]

	for k in range(node_length):
		if dist_mat[k][k] < 0:
			return [True, []]
		for i in range(node_length):
			for j in range(node_length):
				new_dist = dist_mat[i][k] + dist_mat[k][j]
				if dist_mat[i][j] > new_dist:
					dist_mat[i][j] = new_dist

	return [False, dist_mat]

def solution(times, time_limit):

	def getRoute(start, remained_time, passed_list):
		if remained_time < min_time_thres_dict.get(start): return 
		
		new_passed_list = passed_list + [start]
		new_passed_set = set(new_passed_list)
		if new_passed_set in result_dict[start][remained_time]: return

		result_dict[start][remained_time].append(new_passed_set)
		# BFS
		for next_loc in range(time_length):
			new_remained_time = remained_time - dist_mat[start][next_loc]
			if next_loc == final_dest and \
				new_remained_time >= 0 and \
				len(new_passed_list) == time_length:
				continue
			getRoute(next_loc, new_remained_time , new_passed_list)

	time_length = len(times)
	if time_length == 2: return []

	has_add_time_cycle, dist_mat = findNegativePath(times)
	# Detect whether exist negative cycle:
	if has_add_time_cycle: return list(range(0, time_length - 2))
	
	# Initialization
	final_dest = time_length - 1
	result_dict = {loc:defaultdict(list) for loc in range(final_dest+1)}
	min_time_thres_dict = {i:min(0, row[-1]) for i,row in enumerate(dist_mat)}

	getRoute(0, time_limit, [])

	# Extract Result
	result_list = [[]]
	for remained_time, passed_bunnies_list in result_dict[final_dest].items():
		if remained_time < 0:
			continue
		result_list += passed_bunnies_list
	max_length = max([0] + [len(x) for x in result_list])
	result = [row for row in result_list if len(row) == max_length]
	result.sort()
	result = [x-1 for x in list(result[0])[1:-1]] 
	return result