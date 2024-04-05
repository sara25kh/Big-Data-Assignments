import csv
from collections import defaultdict

# Function for the Mapper
def mapper(line):
    # data = line.split(',')
    product_category = line[1] #key
    price = float(line[2]) #value
    return product_category, price

def mapper_b(line):
    customer_id = line[0]
    price = float(line[2]) #value
    return customer_id, price

# Function for the Reducer
def reducer(data):
    revenue_by_category = defaultdict(float)
    for category, price in data:
        for i in price:
            revenue_by_category[category] += i
                
    return revenue_by_category.items()
def reducer_b(data):
    purchase_volume_by_customer =defaultdict(float)
    for customer_id,price in data:
        for i in price:
            purchase_volume_by_customer[customer_id] += i
    return purchase_volume_by_customer
        
# Function to read data from the CSV file
def read_data(file_name):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)

# Function to perform MapReduce
def map_reduce(data):
    # mapped_data = [mapper(line) for line in data]
    mapped_data = []
    for line in data:   
        mapped_data.append(mapper(line))
    mapped_data.sort(key=lambda x: x[0])  # Sort by product category
    grouped_data = defaultdict(list)
    
    for category, price in mapped_data:
        price_list = grouped_data.get(category ,[])
        price_list.append(price)
        grouped_data[category]=price_list
            

    # print(grouped_data)
    reduced_data = reducer(grouped_data.items())
    return reduced_data

def map_reduce_b(data):
    mapped_data = []
    for line in data:   
        mapped_data.append(mapper_b(line))
    mapped_data.sort(key=lambda x: x[0])  # Sort by product category
    grouped_data = defaultdict(list)
  
    for id, price in mapped_data:
        price_list = grouped_data.get(id ,[])
        price_list.append(price)
        grouped_data[id]=price_list

    reduced_data = reducer_b(grouped_data.items())
    return reduced_data

# Function to print the total revenue by product category
def print_revenue_by_category(reduced_data):
    print("Total revenue by product category:")
    # print(reduced_data)
    for category, revenue in reduced_data:
        print(f"{category}: ${revenue:.2f}")

def print_purchase_volume_by_customer(reduced_data):
    sorted_data = sorted(reduced_data.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 customers by purchase volume:")
    for i, (customer_id, purchase) in enumerate(sorted_data[:10], 1):
        print(f"{i}. {customer_id}: ${purchase:.2f}")
        
# Main function
if __name__ == "__main__":
    # File name
    file_name = "purchase_records.csv"
    
    # Read data from CSV file
    data = read_data(file_name)
    data_b = read_data(file_name)
    
    # Perform MapReduce
    reduced_data = map_reduce(data)
    reduced_data_b = map_reduce_b(data_b)
    
    # Print the total revenue by product category
    print_revenue_by_category(reduced_data)
    print_purchase_volume_by_customer(reduced_data_b)