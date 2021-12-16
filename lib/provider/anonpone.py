import lib.util.util as util
import lib.model.cyoa.cyoa as cyoa
import lib.model.cyoa.cyoa_tag as tag


def image_link(filename:str) -> str:
    return f'https://img.anonpone.com/image/{filename[:2]}/{filename}'

def get_cyoa_list(refresh = False) -> list:
    if (refresh):
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
    result = cyoa.Cyoa.select(order_by=['last_post_time', 'desc'], limit=20)
    return result
