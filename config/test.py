a = ["a", "b", "c"]
b = ["1", "2", "3"]
al = tuple([d[0] for d in a])
bl = tuple([d[0] for d in b])
row = dict(zip(al,bl))
row['k'] = '4'

print al, row