import lib.util.util as util
import lib.model.cyoa.cyoa as cyoa
import lib.model.cyoa.cyoa_tag as tag


def image_link(filename:str) -> str:
    return f'https://img.anonpone.com/image/{filename[:2]}/{filename}'

def refresh_cyoa_list():
    link = 'https://www.anonpone.com/api/cyoa'
    js = util.get_json_api(link)
    result = []

    for k in js:
        cy = cyoa.Cyoa.from_json(js[k])
        lst = tag.Tag.save_from_name_list(js[k]['_tags'])
        lsct = [tag.CyoaTag(row=(cy['id'], t['id'])) for t in lst]
        tag.CyoaTag.insert(lsct, or_ignore=True)
        result.append(cy)
    cyoa.Cyoa.insert(result, update_conflict=True, set_col=cyoa.Cyoa.get_props_name(no_id=True, blacklist=['image_path']))
    return result

def parse_query(query) -> list:
    pass

def get_cyoa_list(q:str = '', page = 1, per_page = 20, order_by:list = ['last_post_time', 'desc'], refresh = False) -> list:
    if (refresh):
        refresh_cyoa_list()
    if (order_by[0] == 'ratio'):
        result = cyoa.Cyoa.filter_tags(q, page, per_page, order_by=[['(cast(total_image as real) / total_post)', order_by[1]], ['total_image', order_by[1]]])
    else:
        result = cyoa.Cyoa.filter_tags(q, page, per_page, order_by=order_by)
    return result
