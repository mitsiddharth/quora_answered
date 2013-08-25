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

