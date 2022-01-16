from lib.util.sql_table import *
from lib.model.booru.image import *
from lib.model.booru.tag import *
from lib.model.booru.filter import *
from lib.model.booru.feed import *
from lib.model.booru.album import *

BooruImage._reference = {
    'sizes': SQLRefMany('id', BooruImageSize, 'image_id'),
    'histories': SQLRefMany('id', BooruImageHistory, 'image_id'),
    'tags': SQLRefPivot('id', BooruImageTag, 'image_id', 'tag'),
    'albums': SQLRefPivot('id', BooruAlbumImage, 'image_id', 'album')
}
BooruImageSize._reference = {
    'image': SQLRefOne('image_id', BooruImage, 'id')
}
BooruImageHistory._reference = {
    'image': SQLRefOne('image_id', BooruImage, 'id')
}

BooruTag._reference = {
    'images':SQLRefPivot('id', BooruImageTag, 'tag_id', 'image')
}
BooruImageTag._reference = {
    'image': SQLRefOne('image_id', BooruImage, 'id'),
    'tag': SQLRefOne('tag_id', BooruTag, 'id')
}

BooruAlbum._reference = {
    'images': SQLRefPivot('id', BooruAlbumImage, 'album_id', 'image'),
}
BooruAlbumImage._reference = {
    'album': SQLRefOne('album_id', BooruAlbum, 'id'),
    'image': SQLRefOne('image_id', BooruImage, 'id')
}


