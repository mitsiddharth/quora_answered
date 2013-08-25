import math
import utils
from sklearn import tree


def Entropy(P, N):
  eps = 0.001
  den = P + N + eps
  return -P * math.log((P+eps) / den, 2) - N * math.log((N+eps) / den, 2)

def Split(data, start, end, minGain=0):
  # first column of "data" are the labels.

  data_subset = data[start:end]

  P = sum([x[0] for x in data_subset])
  N = end - start - P


  initial_entropy = Entropy(P, N)
  ig_max = -1e9

  split_feature, split_index = 0, 0

  # starting from 1 because 1st column contains labels
  for i in range(1, len(data_subset[0])):
    data_subset.sort(key=lambda row: row[i])
    P1 = 0
    N1 = 0
    for j in xrange(len(data_subset) - 1):
      if data_subset[j][i] != data_subset[j+1][i]:
        if data_subset[j][0] == 1:
          P1 += 1
        else:
          N1 += 1
        IG = initial_entropy - Entropy(P1, N1) - Entropy(P - P1, N - N1)
        if IG > ig_max:
          ig_max = IG
          split_feature = i
          split_index = j
  
  tree = {}
  tree["probability"] = P/(P+N+0.)
  print 'ig_max = %f' % (ig_max)
  if ig_max > minGain:
    data_subset.sort(key=lambda row: row[split_feature])
    # First column in the "data" and "data_subset" matrices are
    # labels. So, we should not account for that column while storing it.
    tree["split_feature"] = split_feature - 1
    tree["split_value"] = data_subset[split_index][split_feature]
    tree["left"] = Split(data_subset, 0, split_index + 1, minGain)
    tree["right"] = Split(data_subset, split_index + 1, len(data_subset), minGain)
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
  X, Y = utils.LoadData('/Users/siddharths/quora_answered/week1/alldata.train', 15000)
  print 'loaded data. X has %d entries, Y has %d entries' % (len(X), len(Y))

  data = utils.Combine(Y, X)
  print 'starting Split'
  tree = Split(data, 0, len(data), 1)
  print 'Ended Split!!'

  f = open('/Users/siddharths/quora_answered/week1/trained.15000.model', 'w');
  print >> f, str(tree).replace('\'', '"')
  f.close()

if __name__ == '__main__':
  main()
