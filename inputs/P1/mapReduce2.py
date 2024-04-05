import csv
from collections import defaultdict


# Function to read data from the CSV file
def read_data(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)
    

def mapper(line):
    userID = line[0]
    action = line[2]   
    return userID ,action

def reducer(data):
    most_active_user= defaultdict(int)
    for userId , action in data:
        most_active_user[userId] = len(action)
    return most_active_user            


def map_reduce(data):
    mappedData = []
    for line in data:
        mappedData.append(mapper(line))
    mappedData.sort(key=lambda x: x[0])  # Sort by ID
    grouped_data = defaultdict(list)
  
    for id, action in mappedData:
        action_list = grouped_data.get(id , [])
        action_list.append(action)
        # print(action_list , 'id' , id)
        grouped_data[id] = action_list

    reduced_data =  reducer(grouped_data.items())
    return reduced_data




# Main function
if __name__ == "__main__":
    # File name
    file_name = "social_media_dataset.csv"
    
    # Read data from CSV file
    data = read_data(file_name)        

    reduced_data = map_reduce(data) 
    sorted_data = sorted(reduced_data.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 active users:")
    for i, (key, value) in enumerate(sorted_data[:10], 1):
        print(f"{i}. user_id: {key}, amount of interactions: {value}")
    