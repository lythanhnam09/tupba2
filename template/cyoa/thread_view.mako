<%inherit file="../base.mako"/>
<%block name="title">
    ${cyoa['name']} #${thread_num + 1} - ${thread['title'] if thread['title'] not in ['', None] else '#%d' % thread['id']}
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/cyoa.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/cyoa.js"></script>
    <script src="/static/js/cyoathread.js"></script>
</%block>
<%block name="bodyprop">
    class="bg-darkblue"
</%block>

<div class="bg-darkblue">
    <div class="container-lg bg-d25-darkblue py-2">
        % for post in thread['posts']:
            <%
                lsimg = post.get_ref('images', save_result=True)
                lewd_post = 0
                if (len(lsimg) >= 1):
                    for img in lsimg:
                        if (img['alt_id'] >= 1):
                            lewd_post = img['alt_id']
                            break
                    if (lsimg[0]['alt_id'] >= 1):
                        lsimg.insert(0, {'alt_id':0, 'link':'/static/img/lewd.png', 'alt_name':'Spoiler', 'filename':lsimg[0]['filename']})
            %>
            <div class="px-1 pb-1" id="p${post['id']}">
                <div data-id="${post['id']}" class="post card-inline bg-dark${' border-warning border-2 op' if post['is_qm'] == 1 else ''}${' border-success border-2 op-maybe' if post['is_qm'] != 1 and post['username'] == thread['op_name'] and thread['op_name'] != 'Anonymous' else ''} ${f'lewd-{lewd_post}' if (lewd_post > 0) else ''}">
                    <div class="card-header bg-d10-darkblue">
                        <div class="info">
                            <span class="username">${post['username']}</span>
                            % if post['tripcode'] != None:
                                <span class="trip">${post['tripcode']}</span> 
                            % endif
                            % if post['title'] != None:
                                <span class="title">${post['title']}</span> 
                            % endif
                            <span class="id">No.<a href="#p${post['id']}">${post['id']}</a></span> 
                            <span class="date">${post['post_date_str']}</span>
                        </div>
                        <div class="reply-by">
                            % for rep in post['reply_by']:
                                <div class="control-group-round btn-reply">
                                    <button class="btn btn-${'warning' if rep['reply']['is_qm'] == 1 else 'primary'}" onclick="showPostReply(this, ${rep['reply']['id']})">&gt;&gt;${rep['reply_id']}</button>
                                    <a class="btn btn-${'warning' if rep['reply']['is_qm'] == 1 else 'primary'}" href="#p${rep['reply_id']}">#</a>
                                </div>
                            % endfor
                        </div>
                    </div>
                    <div class="card-content bg-dark">
                        % if len(lsimg) > 0:
                            <div class="card-image" data-id="${post['id']}">
                                <div class="img-container" data-id="${post['id']}" onclick="toggleExpandImage(${post['id']}, this)">
                                    % for img in lsimg:
                                        <img src="${img['link']}" data-altid="${img['alt_id']}" alt="${post['images'][0]['filename']} (${img['alt_name']})" title="${post['images'][0]['filename']}" style="display:${'block' if loop.index == 0 else 'none'}">
                                    % endfor
                                </div>
                                % if len(lsimg) > 1:
                                    <div class="image-alt">
                                        % for img in lsimg:
                                            <div class="alt-button" data-altid="${img['alt_id']}" onclick="changeAltImg(${post['id']}, ${img['alt_id']})">
                                                ${img['alt_name']}
                                            </div>
                                        % endfor
                                    </div>
                                % endif
                                % if lsimg[0]['filename'] != None:
                                    <div class="image-filename">
                                        ${lsimg[0]['filename']}
                                    </div>
                                % endif
                            </div>
                        % endif
                        <div class="card-text">
                            ${post['comment_html']}
                        </div>
                    </div>
                </div>
            </div>
        % endfor

        <hr id="hr-bottom" class="my-2">
    </div>
</div>

