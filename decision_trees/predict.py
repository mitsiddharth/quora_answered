import utils
import json

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

def PrintStats(tree):
  def UniqueFeatures(tree):
    ret = set([])
    if tree is None:
      return ret
    if not 'split_feature' in tree:
      return ret
    ret.add(tree['split_feature'])
    ret = ret.union(UniqueFeatures(tree['left']))
    ret = ret.union(UniqueFeatures(tree['right']))
    return ret
  print 'Unique features = %s' % (str(list(UniqueFeatures(tree))))

def main():
  
  f = open('/Users/siddharths/quora_answered/week1/trained.1500.model')
  tree = json.load(f)
  f.close()

  print 'loaded the model. max depth = %d' % (MaxDepth(tree))
  PrintStats(tree)

  X_test, Y_test = utils.LoadData('/Users/siddharths/quora_answered/week1/alldata.test')

  correct_predictions = 0
  for i in xrange(len(X_test)):
    result = predict(tree, X_test[i])
    result = int(result >= 0.5)
    if result == int(Y_test[i]):
      correct_predictions += 1
  print 'predictions result: %d/%d' % (correct_predictions, len(X_test))


if __name__ == '__main__':
  main()
