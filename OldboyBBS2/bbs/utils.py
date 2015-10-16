#_*_coding:utf-8_*_
__author__ = 'jieli'
import os
from OldboyBBS2 import settings


def handle_upload_file(request,file_obj):
    upload_dir = '%s/%s' %(settings.BASE_DIR,settings.FileUploadDir)
    #if not os.path.isdir(upload_dir):
    #    os.mkdir(upload_dir)
    print '-->',dir(file_obj)
    with open('%s/%s' %(upload_dir,file_obj.name),'wb') as destination :
        for chunk in file_obj.chunks():
            destination.write(chunk)


    return   file_obj.name


def insert_comment_node(com_tree,comment):

    for parent, v in com_tree.items():

        if parent == comment.parent_comment: #find parent
            print "find %s's parent %s" %(comment.comment,parent)
            com_tree[parent][comment] = {}
        else: #
            print "haven't found %s 's parent,start looking into further layer..." % comment
            insert_comment_node(com_tree[parent],comment)

def build_comment_tree(request,article_obj):

    all_comments = article_obj.comment_set.select_related().order_by('date')
    comment_tree = {}

    for comment in all_comments:
        if comment.parent_comment is None: #no parent
            comment_tree[comment] = {}
        else:
            insert_comment_node(comment_tree,comment)


    for k,v in comment_tree.items():
        print k,v

    return  comment_tree

def find_parent_comment(com_tree,comment_obj):

    for p,v in com_tree.items():
        if p == comment_obj.parent_comment: #find farther
            com_tree[p][comment_obj] = {}
        else:
            find_parent_comment(com_tree[p], comment_obj)

def create_comment_tree(request,article_obj):

    all_comments = article_obj.comment_set.select_related().order_by('date')
    comment_tree = {}

    for comment in all_comments:
        if comment.parent_comment is None:
            comment_tree[comment] = {}
        else:
            find_parent_comment(comment_tree,comment)

    return  comment_tree
    for k,v in comment_tree.items():
        print k,v