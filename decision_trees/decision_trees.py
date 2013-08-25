import math
import utils
from sklearn import tree
import multiprocessing

def SplitFeature(data, feature_id, q):
  P = sum([x[0] for x in data])
  N = len(data) - P

  initial_entropy = utils.Entropy(P, N)
  ig_max = -1e9

  split_feature, split_index = 0, 0

  data.sort(key=lambda row: row[1])
  P1 = 0
  N1 = 0
  for j in xrange(len(data) - 1):
    if data[j][0] == 1:
      P1 += 1
    else:
      N1 += 1
    if data[j][1] != data[j+1][1]:
      IG = initial_entropy - utils.Entropy(P1, N1) - utils.Entropy(P - P1, N - N1)
      if IG > ig_max:
        ig_max = IG
        split_index = j
  result = [ig_max, feature_id, split_index]
  #print 'feature %d\'s result = %s' % (feature_id, str(result))
  q.put(result)
 

def ConstructDataSubset(data, start, end, feature_id):
  data_subset = []
  for i in range(start, end):
    data_subset.append([data[i][0], data[i][feature_id]])
  return data_subset

def Split(data, start, end, minGain=0, parallel=False):
  # Note: first column of "data" are the labels.

  P = sum([x[0] for x in data[start:end]])
  N = end - start - P

  q = multiprocessing.Queue()
  jobs = []

  ig_max = -1e9
  split_feature = 1
  split_index = 0

  # starting from 1 because 1st column contains labels
  for i in range(1, len(data[0])):
    data_subset = ConstructDataSubset(data, start, end, i)
    if parallel:
      p = multiprocessing.Process(target=SplitFeature, args=(data_subset, i, q,))
      jobs.append(p)
      p.start()
    else:
      SplitFeature(data_subset, i, q)

  cnt = 1
  while cnt < len(data[0]):
    result = q.get()
    cnt += 1
    if result[0] > ig_max:
      ig_max = result[0]
      split_feature = result[1]
      split_index = result[2]

  assert q.empty()

  tree = {}
  tree["probability"] = P/(P+N+0.)
  print 'ig_max = %f' % (ig_max)
  if ig_max > minGain:
    data_subset = data[start:end]
    data_subset.sort(key=lambda row: row[split_feature])
    # First column in the "data" and "data_subset" matrices are
    # labels. So, we should not account for that column while storing it.
    tree["split_feature"] = split_feature - 1
    tree["split_value"] = data_subset[split_index][split_feature]
    tree["left"] = Split(data_subset, 0, split_index + 1, minGain, parallel)
    tree["right"] = Split(data_subset, split_index + 1, len(data_subset), minGain, parallel)
  return tree

def predict(tree, X):
  if tree is None:
    return 0 #When it doesn't have a tree at all, just predict null
  if not "split_feature" in tree:
    return tree["probability"]
    
  if X[tree["split_feature"]] > tree["split_value"]:
    return predict(tree["right"], X)
  else:
    return predict(tree["left"], X)

def MaxDepth(tree):
  if tree is None:
    return 0
  h1 = 0
  h2 = 0
  if 'left' in tree:
    h1 = MaxDepth(tree['left'])
  if 'right' in tree:
    h2 = MaxDepth(tree['right'])
  return 1 + max(h1, h2)

def main():
  X, Y = utils.LoadData('/Users/siddharths/quora_answered/week1/alldata.train', 5000)
  print 'loaded data. X has %d entries, Y has %d entries' % (len(X), len(Y))

  data = utils.Combine(Y, X)
  print 'starting Split'
  tree = Split(data, 0, len(data), 1)
  print 'Ended Split!!'

  f = open('/Users/siddharths/quora_answered/week1/trained.5000.model', 'w');
  print >> f, str(tree).replace('\'', '"')
  f.close()

if __name__ == '__main__':
  main()
