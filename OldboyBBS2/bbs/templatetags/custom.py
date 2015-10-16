#_*_coding:utf-8_*_
__author__ = 'jieli'
from django import template

register = template.Library()


@register.filter
def upper(value):
    return  value.upper()

def recursive_build_html(html_ele,tree,indent):

    for k,v in tree.items():
        html = '''<div style="margin-left:%spx; border-left:1px solid black;border-bottom:1px dashed black;padding:5px">
                    <span class="comment-author">%s</span>
                    <span class="comment-comment">%s</span>
                    <span class="comment-date">%s</span>
                     </div>''' %(indent,
                                 k.user.name,
                                 k.comment,
                                 k.date.strftime("%Y-%m-%d %T")
                                 )
        html_ele += html
        print html
        if v:
            html_ele =  recursive_build_html(html_ele,v,indent+20)

    return   html_ele

@register.simple_tag
def build_layer_comments(comment_tree):
    comment_box = '<div class="comment_box">'
    for k,v in comment_tree.items():
        html = '''<div style="margin-left:%spx; border-left:1px solid black;border-bottom:1px dashed black;padding:5px">
                    <span class="comment-author">%s</span>
                    <span class="comment-comment">%s</span>
                    <span class="comment-date">%s</span>
                     </div>''' %(0,
                                 k.user.name,
                                 k.comment,
                                 k.date.strftime("%Y-%m-%d %T")
                                 )
        #html ='''<p>-->  %s </p>''' %(k.comment)
        print html,v
        if v: #has son
            html = recursive_build_html(html,v,10)
        comment_box  += html

    return  comment_box + "</div>"
@register.simple_tag
def abs_compare(p_num, current_p_num):

    #print '-->',p_num,current_p_num
    abs_res = abs(current_p_num - p_num)
    if abs_res <3:

       if abs_res == 0: #当前页
            page_class = 'active_page'
       else:
           page_class = ''

       html = '''<a href="?page=%s" >
            <span class="page_num %s">%s</span>
        </a>''' % (p_num,page_class,p_num)

       return  html
    else:
        return ''


def recursive_build_tree(html_ele,tree,indent) :
    for k,v in tree.items():
        row = '''<div style="margin-left:%spx;border-left:1px solid black;border-bottom:1px dashed black;padding:5px">
            <span  class="comment-author">%s</span>
            <span class="comment-comment">%s</span>
            <span class="comment-date">%s</span>
            </div>
            ''' %(indent,k.user.name,k.comment,k.date.strftime("%Y-%m-%d %T"))
        print 'row:',row
        html_ele += row
        if v:
            html_ele = recursive_build_tree(html_ele,tree[k],indent+30)
    return html_ele
@register.simple_tag
def build_comment_tree(comment_tree):

    html_ele = "<div class='comment_box'>";

    for k,v in comment_tree.items():
        row = '''<div style="margin-left:%spx; border-left:1px solid black;border-bottom:1px dashed black;padding:5px">
            <span class="comment-author" >%s</span>
            <span class="comment-comment" >%s</span>
            <span class="comment-date">%s</span>
            </div>
            ''' %(0,k.user.name,k.comment,k.date.strftime("%Y-%m-%d %T"))
        print '-->row,',row
        html_ele += row
        if v:
            html_ele = recursive_build_tree(html_ele,comment_tree[k],30)

    return  html_ele + "</div>"
