import math

def LoadData(file_name, num_lines=None):
  X = []
  Y = []
  f = open(file_name)
  cnt = 0
  for line in f.readlines():
    cnt += 1
    if num_lines is not None and cnt > num_lines:
      break
    line = line.replace('\n', '')
    arr = line.split(',')
    Y.append(float(arr[0]))
    X.append(map(float, arr[1:]))
  f.close()
  return X, Y

def Combine(Y, X):
  data = []
  for i in xrange(len(Y)):
    data.append([Y[i]] + X[i])
  return data

def Entropy(P, N):
  eps = 0.001
  den = P + N + eps
  return -P * math.log((P+eps) / den, 2) - N * math.log((N+eps) / den, 2)


