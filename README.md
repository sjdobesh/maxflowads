# Max Flow Advertisements

Maximize the disperal of advertisements to targeted demographics without showing any users more than one add.
If the maxflow out does not equal the flow in, not all contracts can be fulfilled.

### Usage:
```
chmod +x ./maxflow.py
./maxflow.py [-h] n m k a g
```
positional arguments:
  n           The number of users (int)
  m           The number of adverstisers (int)
  k           The number of demographic groups (int)
  a           Config for adverstisers (string) 
              r_i + X_i 
              eg: 10g1g3g5,5g2 : r_0 = 10, X_0 = {G1, G3, G5}, r_1 = 5, X_1 = {G2}
  g           Config for groups (string) 
              user+g+user seperated by commas 
              eg: 1g2g3,1g2g4 : G1 = {j_1, j_2, j_3}, G2 = {j_1, j_2, j_4}

optional arguments:
  -h, --help  show this help message and exit
