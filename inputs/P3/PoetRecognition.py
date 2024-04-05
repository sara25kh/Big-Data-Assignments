import random
import re
from collections import defaultdict
# Step a: Data Preprocessing

# Function to read poems from text files
def read_poems(poet_names):
    poems = {}
    for poet in poet_names:
        with open(f"{poet}.txt", "r", encoding="utf-8") as file:
            poems[poet] = file.read().splitlines()
    # for key, lst in poems.items():
    #     print(f"{key}: {lst[:10]}")    
    return poems

# Function to split poems into training and test datasets
def split_data(poems, split_ratio=0.8):
    train_data = {}
    test_data = {}
    for poet, poem_list in poems.items():
        random.shuffle(poem_list)  # Shuffle poems
        split_index = int(len(poem_list) * split_ratio)
        train_data[poet] = poem_list[:split_index]
        test_data[poet] = poem_list[split_index:]
    # for key, lst in test_data.items():
    #     print(f"{key}: {lst[:10]}") 
    return train_data, test_data

# Function for preprocessing steps like tokenization, removing stopwords, etc.
def preprocess(poems):
    # Implement your preprocessing steps here
    # Example: Tokenization, stopword removal, lowercasing, etc.
    preprocessed_poems = {}
    for poet, poem_list in poems.items():
        preprocessed_poems[poet] = [preprocess_poem(poem) for poem in poem_list]
    # for key, lst in poems.items():
    #     print(f"{key}: {lst[:10]}")     
    return preprocessed_poems

# Function to preprocess a single poem
def preprocess_poem(poem):
    preprocess_poem = tokenize(poem)
    for word in preprocess_poem:
        if word in ("و",'با','از','در','به','که','تا','را')  :
            preprocess_poem.remove(word)  
    # print(preprocess_poem)
    return preprocess_poem
#Function to tokenize
def tokenize(my_str):
    #print('Tokenizing...')
    result = re.split(' |\t|\n', my_str)
    result = list(filter(None, result))
    return result
# Step b: Frequent Itemset Mining

# Implement A-Priori and PCY algorithms for frequent itemset mining


# Function to generate candidate itemsets of size k
def generate_candidates(frequent_itemsets, k):
    candidate_itemsets = []
    # Join step: Generate candidate itemsets by joining frequent itemsets of size k-1
    for i in range(len(frequent_itemsets)):
        for j in range(i+1, len(frequent_itemsets)):
            itemset1, itemset2 = frequent_itemsets[i], frequent_itemsets[j]
            # Check if the first k-2 elements are equal
            if itemset1[:k-2] == itemset2[:k-2]:
                # print(itemset1)
                candidate_itemset = sorted(list(set(itemset1) | set(itemset2)))  # Union of two itemsets
                candidate_itemsets.append(candidate_itemset)
    return candidate_itemsets

# Function to prune candidate itemsets using the Apriori property
def prune_candidates(candidate_itemsets, frequent_itemsets, k):
    pruned_candidates = []
    for candidate in candidate_itemsets:
        subsets = [candidate[:k-1]]  # Initialize subsets with all (k-1)-subsets of candidate
        # Generate all (k-1)-subsets of the candidate
        for i in range(k-1):
            subset = candidate[:i] + candidate[i+1:]
            subsets.append(subset)
        # Check if all (k-1)-subsets are frequent
        if all(subset in frequent_itemsets[k-1] for subset in subsets):
            pruned_candidates.append(candidate)
    return pruned_candidates

# Function to find frequent itemsets using the A-Priori algorithm
def apriori_algorithm(data, min_support):
    frequent_itemsets = defaultdict(list)
    # Step 1: Generate frequent 1-itemsets
    single_item_counts = defaultdict(int)
    for transactions in data.values():
        for transaction in transactions:
            for item in transaction:
                single_item_counts[item] += 1
    frequent_itemsets[1] = [[item] for item, count in single_item_counts.items() if count >= min_support]

    # Step 2: Generate frequent itemsets of size > 1
    k = 2
    while frequent_itemsets:
        candidate_itemsets = generate_candidates(frequent_itemsets, k)
        frequent_itemsets = {}
        for transaction in transactions:
            for candidate in candidate_itemsets:
                if set(candidate).issubset(set(transaction)):
                    frequent_itemsets[candidate] = frequent_itemsets.get(candidate, 0) + 1
        frequent_itemsets = {itemset: support for itemset, support in frequent_itemsets.items() if support >= min_support}
        k += 1

    return frequent_itemsets


# Step c: Generating Association Rules

# Generate association rules from the frequent itemsets

# Step d: Poet Classification and Evaluation

# Implement poet classification using association rules and evaluate accuracy

# Main function
if __name__ == "__main__":
    # Step a: Data Preprocessing
    # poet_names = ['khayyam', 'ferdousi', 'hafez', 'saadi', 'rumi']
    poet_names = ['khayyam',  'hafez']
    poems = read_poems(poet_names)
    train_data, test_data = split_data(poems)
    # print(test_data)
    preprocessed_train_data = preprocess(train_data)
    preprocessed_test_data = preprocess(test_data)

    # Sample data (replace with actual preprocessed data)
    preprocessed_train_data = {
        'khayyam': [['word1', 'word2', 'word3'], ['word2', 'word4']],
        'ferdousi': [['word1', 'word3', 'word5'], ['word2', 'word5']],
        'hafez': [['word2', 'word3', 'word6'], ['word1', 'word4']],
        'saadi': [['word1', 'word2', 'word3'], ['word3', 'word5']],
        'rumi': [['word2', 'word4', 'word6'], ['word1', 'word5']]
    }

    # Minimum support threshold
    min_support = 2

    # Apply A-Priori algorithm
    frequent_itemsets = apriori_algorithm(preprocessed_train_data, min_support)

    # Print frequent itemsets
    for k, itemsets in frequent_itemsets.items():
        print(f"Frequent {k}-itemsets:")
        for itemset in itemsets:
            print(itemset)
    # Step b: Frequent Itemset Mining
    # Implement A-Priori and PCY algorithms

    # Step c: Generating Association Rules
    # Generate association rules from the frequent itemsets

    # Step d: Poet Classification and Evaluation
    # Implement poet classification using association rules and evaluate accuracy
