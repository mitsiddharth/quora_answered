import json
import random
import sys
import math
import re

def GetAllTopics(training_data):
  topics_dict = {}
  for training_sample in training_data:
    for topic in training_sample['topics']:
      topics_dict[topic['name']] = topic['followers']
  return topics_dict

def CreateFeatureMapping(topics_list):
  fmap = {}
  cnt = 0
  for topic in topics_list:
    fmap[topic] = cnt
    cnt += 1
  return fmap

def CreateVectorFromSample(sample, feature_map):
  bit_vector = [0] * len(feature_map)
  topics = GetAllTopics([sample])
  for topic in topics.keys():
    if topic in feature_map:
      bit_vector[feature_map[topic]] = 1
  return bit_vector

def dot(a, b):
  ret = 0.0
  for i in xrange(len(a)):
    ret += a[i] * b[i]
  return ret

def sigmoid(x):
  try:
    return 1. / (1 + math.exp(-x))
  except OverflowError:
    return 0

def magnitude(a):
  ret = 0
  for i in xrange(len(a)):
    ret += a[i] * a[i]
  return ret ** .5

def norm(a, b):
  ret = 0
  for i in xrange(len(a)):
    ret += (a[i]-b[i])*(a[i]-b[i])
  ret = ret ** .5
  ret /= (magnitude(a) * magnitude(b))
  return ret

def LogisticRegression(X, Y):
  """returns weight vector W."""
  n = len(X)
  m = len(X[0])
  tolerance = 0.001
  step_size = 0.001
  W_old = [1] * m
  W_diff = 100
  iteration_cnt = 0
  while W_diff > tolerance:
    iteration_cnt += 1
    if iteration_cnt == 100:
      break
    W_prev = list(W_old)
    for i in xrange(n):
      for j in xrange(m):
        W_old[j] = W_old[j] + step_size * X[i][j] * (Y[i] - sigmoid(dot(W_old, X[i])))
    W_diff = norm(W_old, W_prev)
  
  return W_old

def predict(X, W):
  return sigmoid(dot(X, W)) >= 0.5

def SplitSentence(sentence):
  words = re.split("\W+", sentence)
  filtered_words = [w for w in words if len(w) > 4]
  return filtered_words

def StartsWithQuestionWord(sentence):
  match = re.match("^(what|how|where|why|who)", sentence.lower())
  return match is not None

def GetFeatures(data, topic_stats, max_follower_count):
  s = 0.0
  num_topics = 0.01
  topics_list = GetAllTopics([data])
  max_topic_prob = 0.
  follower_count_local_max = 0
  for topic in topics_list:
    if topic in topic_stats:
      follower_count_local_max = max(follower_count_local_max, topics_list[topic])
      prob = topic_stats[topic]['answered'] / topic_stats[topic]['count'] 
      s += prob
      max_topic_prob = max(max_topic_prob, prob)
      num_topics += 1
  words = SplitSentence(data['question_text'])
  X = [1, max_topic_prob, int(training_sample['anonymous']), len(topics_list), len(words), int(StartsWithQuestionWord(data['question_text']))]
  return X

def PrintFeaturesToFile(file_name, X, Y):
  f = open(file_name, 'w')
  for i in xrange(len(X)):
    s = ''
    s += (str(2*Y[i] - 1) + ' ')
    for j in xrange(len(X[i])):
      s += (str(j+1) + ':' + str(X[i][j]) + ' ')
    print >>f, s
  f.close()


N = int(raw_input())

training_data = []

topic_stats = {}

for i in xrange(N):
  training_sample = json.loads(raw_input())
  training_data.append(training_sample)
  topics_list = GetAllTopics([training_sample])
  is_answered = training_sample['__ans__']
  max_follower_count = 0
  for topic in topics_list.keys():
    max_follower_count = max(topics_list[topic], max_follower_count)
    if topic not in topic_stats:
      topic_stats[topic] = {'count': 0.0, 'answered': 0.0}
    topic_stats[topic]['count'] += 1
    if is_answered:
      topic_stats[topic]['answered'] += 1

X = []
Y = []

for training_sample in training_data:
  X.append(GetFeatures(training_sample, topic_stats, max_follower_count))
  Y.append(int(training_sample['__ans__']))

#PrintFeaturesToFile('feature_file', X, Y)

W = LogisticRegression(X, Y)

right_cnt = 0
wrong_cnt = 0

test_data = []
test_labels = []
T = int(raw_input())
for i in xrange(T):
    test_input = json.loads(raw_input())
    question_key = test_input['question_key']
    X = GetFeatures(test_input, topic_stats, max_follower_count)
    #test_data.append(X)
    #test_labels.append(test_input['__ans__'])
    __ans__ = predict(X, W)
    #if __ans__ == test_input['__ans__']:
    #  right_cnt += 1
    #else:
    #  wrong_cnt += 1
    print json.dumps({'question_key': question_key, '__ans__': __ans__})
#PrintFeaturesToFile('test_file', test_data, test_labels)
#print 'right_cnt = %d , wrong_cnt = %d' % (right_cnt, wrong_cnt)
