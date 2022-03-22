The current code consists of 5 files:
Main.py: sets up the shared memory and initializes all threads
Data_generator.py: repeatedly pings an IP address, and records the results
Sentinel.py: reads the data stream and determines if the mu or sigma value has changed significantly
Proof.py: uses the mu and sigma from the sentinel to determine the probability that each of the given theorems hold
Model.py: given the probabilities, determines the most relevant one


More Info:
https://docs.google.com/document/d/1jI9saYA9w_TSPjx0xVIkZqPf8i9IN1A6laPkFalznFM/edit?usp=sharing