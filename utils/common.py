def mean(arr):
    if len(arr) == 0: 
        return 0.5
    else: 
        total = 0
        for i in arr:
            total+=i
        return total/len(arr)

def getWinLose(p1_id, p2_id, result):
    if result == 1 or result == "1":
        return p1_id, p2_id
    return p2_id, p1_id


