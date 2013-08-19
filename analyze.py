import json
import random

def GetAllTopics(training_data):
  topics_list = set()
  for training_sample in training_data:
    if training_sample['context_topic']:
      topics_list.add(training_sample['context_topic']['name'])
    for topic in training_sample['topics']:
      topics_list.add(topic['name'])
  return list(topics_list)

N = int(raw_input())

training_data = []

topic_stats = {}

for i in xrange(N):
  training_sample = json.loads(raw_input())
  topics_list = GetAllTopics([training_sample])
  is_answered = training_sample['__ans__']
  for topic in topics_list:
    if topic not in topic_stats:
      topic_stats[topic] = {'count': 0.0, 'answered': 0.0}
    topic_stats[topic]['count'] += 1
    if is_answered:
      topic_stats[topic]['answered'] += 1
