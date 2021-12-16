from lib.util.sql_table import *
from lib.model.cyoa.cyoa import *
from lib.model.cyoa.cyoa_tag import *
from lib.model.cyoa.cyoa_thread import *
from lib.model.cyoa.fanart import *
from lib.model.cyoa.post import *

Cyoa._reference = {
    'tags': SQLRefPivot('id', CyoaTag, 'cyoa_id', 'tag'),
    'threads': SQLRefPivot('id', CyoaThread, 'cyoa_id', 'thread'),
    'fanarts': SQLRefMany('id', Fanart, 'cyoa_id')
}

Tag._reference = {
    'cyoas': SQLRefPivot('id', CyoaTag, 'tag_id', 'cyoa')
}
CyoaTag._reference = {
    'tag': SQLRefOne('tag_id', Tag, 'id'),
    'cyoa': SQLRefOne('cyoa_id', Cyoa, 'id')
}

Thread._reference = {
    'cyoas': SQLRefPivot('id', CyoaThread, 'thread_id', 'cyoa'),
    'posts': SQLRefMany('id', Post, 'thread_id')
}
CyoaThread._reference = {
    'thread': SQLRefOne('thread_id', Thread, 'id'),
    'cyoa': SQLRefOne('cyoa_id', Cyoa, 'id')
}

Fanart._reference = {
    'cyoa': SQLRefOne('cyoa_id', Cyoa, 'id')
}

Post._reference = {
    'thread': SQLRefOne('thread_id', Thread, 'id'),
    'images': SQLRefMany('id', PostImage, 'post_id')
}
PostImage._reference = {
    'post': SQLRefOne('post_id', Post, 'id')
}

#print('cyoa table db referenced')
