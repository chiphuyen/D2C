from bs4 import BeautifulSoup
from collections import Counter
from tqdm import tqdm 
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("openai-community/gpt2")

def count_unique_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = [tag.name for tag in soup.find_all()]
    unique_tags = set(tags)
    return len(unique_tags)

def calculate_dom_depth(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    def get_max_depth(element, depth):
        children = element.find_all(recursive=False)
        if not children:
            return depth
        return max(get_max_depth(child, depth + 1) for child in children)

    return get_max_depth(soup, 0)

def count_total_nodes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return len(soup.find_all())

def compute_stats_and_bucketize(numbers, k):
    if not numbers or k <= 0:
        return "Invalid input"

    average = sum(numbers) / len(numbers)
    minimum = min(numbers)
    maximum = max(numbers)

    # Calculate the range for each bucket
    range_size = (maximum - minimum) / k
    buckets = [[] for _ in range(k)]

    # Function to determine the bucket index for a number
    def get_bucket_index(num):
        if num == maximum:
            return k - 1
        return int((num - minimum) / range_size)

    # Assign numbers to buckets
    for num in numbers:
        bucket_index = get_bucket_index(num)
        buckets[bucket_index].append(num)

    return average, minimum, maximum, buckets

def interval_buckets(min_value, max_value, k):
    """
    Split the range [min_value, max_value] into k equal-interval buckets.

    :param min_value: The minimum value of the range.
    :param max_value: The maximum value of the range.
    :param k: Number of buckets.
    :return: A list of tuples, each representing the min and max values of a bucket.
    """
    if k <= 0:
        raise ValueError("Number of buckets (k) must be positive.")

    interval = (max_value - min_value) / k
    buckets = []

    for i in range(k):
        bucket_min = min_value + i * interval
        # To ensure the last bucket ends exactly at max_value
        bucket_max = min_value + (i + 1) * interval if i < k - 1 else max_value
        buckets.append((bucket_min, bucket_max))

    return buckets

def size_buckets(data, k):
    """
    Split the data into k buckets such that each bucket has approximately the same number of items.

    :param data: List of numbers to be bucketed.
    :param k: Number of buckets.
    :return: A list of tuples, each representing the min and max values of a bucket.
    """
    if k <= 0:
        raise ValueError("Number of buckets (k) must be positive.")

    # Convert data to a pandas Series for ease of computation
    series = pd.Series(data)
    # Calculate quantiles
    quantiles = np.linspace(0, 1, k+1)
    quantile_ranges = series.quantile(quantiles).tolist()

    # Create buckets
    buckets = [(quantile_ranges[i], quantile_ranges[i+1]) for i in range(len(quantile_ranges)-1)]

    return buckets

if __name__ == "__main__":
    all_counts = []
    for filename in tqdm(os.listdir("../../testset_final")):
        if ".html" in filename:
            full_path = os.path.join("../../testset_final", filename)
            with open(full_path, "r") as f:
                html_content = f.read() 
                
                # length = tokenizer(html_content)["input_ids"]
                # all_counts.append(len(length))

                # total_tags = count_total_nodes(html_content)
                # all_counts.append(total_tags)

                # dom_depth = calculate_dom_depth(html_content)
                # all_counts.append(dom_depth)

                unique_tags = count_unique_tags(html_content)
                all_counts.append(unique_tags)

    print (len(all_counts))
    print (np.mean(all_counts))
    print (min(all_counts), max(all_counts))
    print (np.std(all_counts))
    



