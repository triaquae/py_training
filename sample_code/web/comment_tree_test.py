#_*_coding:utf-8_*_
__author__ = 'Alex Li'


data = [
    ('a',None),
    ('b', 'a'),
    ('c', None),
    ('d', 'a'),
    ('e', 'a'),
    ('g', 'b'),
    ('h', 'g'),
    ('j', None),
    ('f', 'j'),
]


'''
a -> b -> g ->h
a -> d
a -> e
{
    a : {b:{g:}}
}
'''
{
    'a':{
        'b':{
            'g':{
                'h':{}
            }
        },
        'd':{},
        'e':{}
    },
    'j':{
        'f':{}
    }
 }

def tree_search(d_dic, s,p):
    for k,v_dic in d_dic.items():
        if k == p: #find farther
            print("find [%s] 's farther [%s]" %(s,p ))
            d_dic[k][s]= {}
        else: #might in deeper layer of this branch
            print("going to deeper layer...")
            tree_search(d_dic[k], s,p)
tree_dic = {}
for son,parent in data:
    if parent is None:#no parent
        tree_dic[son]  =  {}
    else: # looking for where it's farther is
        tree_search(tree_dic, son,parent)

for k,v in tree_dic.items():
    print(k,v)