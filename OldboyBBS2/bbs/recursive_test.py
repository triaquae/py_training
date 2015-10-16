#_*_coding:utf-8_*_
__author__ = 'jieli'



data = [
    (None,'A'),
    ('A','A1'),
    ('A','A1-1'),
    ('A1','A2'),
    ('A1-1','A2-3'),
    ('A2-3','A3-4'),
    ('A1','A2-2'),
    ('A2','A3'),
    ('A2-2','A3-3'),
    ('A3','A4'),
    (None,'B'),
    ('B','B1'),
    ('B1','B2'),
    ('B1','B2-2'),
    ('B2','B3'),
    (None,'C'),
    ('C','C1'),

]


data_dic = {
    'A': {
        'A1': {
            'A2':{
                'A3':{
                    'A4':{}
                }
            },
            'A2-2':{
                'A3-3':{}
            }
        }
    },
    'B':{
        'B1':{
            'B2':{
                'B3':{}
            },
            'B2-2':{}
        }
    },
    'C':{
        'C1':{}
    }

}

comment_tree = {}

def recursive(data_tree,parent,son):
    for p,v in data_tree.items():
        if p == parent: # find it's farther
            print "\033[32;1mfound %s's parent %s\033[0m" %(son,parent)
            data_tree[p][son] = {}
        else:
            print "not find %s's parent node %s yet, going to further layer" %(son,parent)
            recursive(data_tree[p],parent,son) #data_tree['A']

for parent,son in data:
    if parent is None: #no parent
        comment_tree[son] = {}
    else:
        recursive(comment_tree,parent,son)


for k,v in comment_tree.items():
    print k,v