#_*_coding:utf-8_*_
__author__ = 'jieli'


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

def recursive(data_dic,s,p):
    for parent,v in data_dic.items():
        if parent == p: #find parent
            data_dic[parent][s]={}
        else:
            print 'not find %s, go into further layer search....' % p
            recursive(data_dic[parent],s,p)


data_tree ={}
for node in data:
    son,parent = node
    print '-->serarch:',son,parent
    if parent is None:
        data_tree[son]={}
    else:
        recursive(data_tree,son,parent)


for k,v in data_tree.items():
    print k,v

