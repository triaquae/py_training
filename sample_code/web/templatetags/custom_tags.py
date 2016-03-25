#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from django import template
register = template.Library()
from django.utils.safestring import mark_safe


def build_comment_tree_html(branch,margin_pos):
    branch_html = ""
    for k,v_dic in branch.items():
        branch_html += "<div class='comment-node' style='margin-left:%spx' >" %margin_pos + \
                       k.comment + \
                       "<span class='pull-right'>" + k.user.name + "&nbsp;&nbsp;" +\
                       k.date.strftime('%Y-%m-%d %H:%M') + "<span>"\
                       "</div>"
        if v_dic:#has child
            branch_html += build_comment_tree_html(v_dic,margin_pos+20)
    return  branch_html

def tree_search(t_dic, comment_obj):
    for k,v_dic in t_dic.items():
        if k.id == comment_obj.parent_comment_id:#find parent
            print("find [%s]'s parent [%s]" %(comment_obj,k))
            t_dic[k][comment_obj] ={}
        else:#might in this branch's deeper layer
            print("going to further layer ... ")
            tree_search(t_dic[k], comment_obj)
@register.simple_tag
def build_comment_tree(comments):
    '''
    build comment tree according to it's layers
    :param comments:
    :return:
    '''
    comments = sorted(comments,key=lambda x:x.id)
    print("comment tags:",comments)
    tree_dic = {}
    for comment in comments:
        if comment.parent_comment is None:#has no parent
            tree_dic[comment] = {}
        else:#do further search
            tree_search(tree_dic, comment)
    for k,v in tree_dic.items():
        print(k,v)

    comment_list_in_layer = sorted(tree_dic.items(),key=lambda x:x[0].id)
    print(comment_list_in_layer)
    html = "<div>"
    for key,branch_dic in comment_list_in_layer:
        margin_pos = 0
        top_branch_comment = "<div class='top-branch-comment'>"  + \
                             "<div class='comment-node' style='margin-left:%spx' >" % margin_pos + \
                              key.comment +  "</div>"
        html += top_branch_comment
        if branch_dic:
            html += build_comment_tree_html(branch_dic,margin_pos+20)
        html +="</div>"  #for end of the top-branch-comment
    html += "</div>"
    print(html )
    return mark_safe(html)