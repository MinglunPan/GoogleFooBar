from itertools import combinations

def solution(num_buns, num_required):
    num_duplicated = num_buns - num_required + 1
    bunnies_list = [[] for i in range(num_buns)]

    for key, bunnies in enumerate(combinations(range(num_buns), num_duplicated)):
        for no_b in bunnies:
            bunnies_list[no_b].append(key)
    return bunnies_list

if __name__ == "__main__":
    print(solution(3,2))