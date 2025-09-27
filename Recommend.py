import math

#finds the cosine simularity between two vectors (represented as lists)
def cosineSimularity(a, b):
    dotProduct = 0
    aLength = 0
    bLength = 0
    for i in range(len(a)):
        dotProduct += a[i] * b[i]
        aLength += a[i] ** 2
        bLength += b[i] ** 2
    dot = math.acos(dotProduct / ((aLength ** 0.5) * (bLength ** 0.5)))
    return round(math.degrees(dot), 2)

#opens the file and reads the amount of entries
history = open("history.txt", "r")
details = history.readline()
itemNum = int(details.split(" ")[1])

#Creates a dictionary with the item ID as a key and the value as a list, the index of which corresponds to a customer ID.
#The value at each index is 1 if the customer has bought the item, 0 otherwise.
customerItemTable = {}
for line in history.readlines():
    line = line.strip().split(" ")
    customerItemTable.setdefault(int(line[1]), [0] * itemNum)
    customerItemTable[int(line[1])][int(line[0])-1] = 1
history.close()

#Counts the number of positive entries (1) in the table
count = 0
for item, value in customerItemTable.items():
    for x in value:
        if x == 1:
            count += 1
print(f"Positive entries: {count}")

#using list comprehension to instantiate a 2D array with default values of 0
ItemToItem = [[0 for _ in range(itemNum)] for _ in range(itemNum)]

#Calculates the cosine simularity between each pair of items and stores it in the 2D array
for i in range(len(ItemToItem)):
    for j in range(len(ItemToItem)):
        if i != j:
            ItemToItem[i][j] = cosineSimularity(customerItemTable[i+1], customerItemTable[j+1])
          
#Calculates the average angle between all pairs of items, taking into account the symmetry of the matrix to avoid double counting              
total_angle = 0
count = 0
for i in range(len(ItemToItem)):
    for j in range(i + 1, len(ItemToItem)):
        total_angle += ItemToItem[i][j]
        count += 1

average_angle = total_angle / count if count > 0 else 0
print(f"Average angle: {average_angle}")

queries = open("queries.txt", "r")

for line in queries.readlines():
    # Print out the items in the shopping cart
    shopping_cart = []
    if len(line):
        line = line.strip().split(" ")
        for item in line:
            shopping_cart.append(int(item))
        print(f"Shopping cart: {' '.join(map(str, shopping_cart))}")

        # Find the item with the lowest cosine similarity that is not already in the shopping cart...
        recommendations = []
        for item in shopping_cart:
            min_similarity = float('inf')
            recommended_item = None
            for i in range(itemNum):
                if (i + 1) not in shopping_cart and ItemToItem[item - 1][i] < min_similarity:
                    min_similarity = ItemToItem[item - 1][i]
                    recommended_item = i + 1

            # ...and print it out
            if recommended_item != None and min_similarity < 90:
                print(f"Item: {item}; match: {recommended_item}; angle: {min_similarity}")
                recommendations.append((recommended_item, min_similarity))
            else:
                print(f"Item: {item} no match")

        # Sort the recommendations by cosine similarity and remove duplicates for the recommended list
        recommendations.sort(key=lambda x: x[1])
        recommended_list = []
        for item in recommendations:
            if item[0] not in recommended_list:
                recommended_list.append(item[0])
                
        print(f"Recommend: {' '.join(map(str, recommended_list))}")

queries.close()