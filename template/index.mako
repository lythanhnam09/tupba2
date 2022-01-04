<%inherit file="base.mako"/>
<%block name="title">
    TUPBA II - Homepage
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/main.css">
</%block>
    <div class="bg-darkblue">

        <div class="container-lg bg-d10-darkblue">
            <div class="row vflex-center">
                <%
                    ls = [
                        ('Rewatch stream', '/rewatch', '/static/img/booru.png'),
                        ('CYOA browser', '/cyoa', '/static/img/booru.png'),
                        ('Booru browser', '/booru', '/static/img/rewatch.png'),
                        ('Logger', '/logger', '/static/img/logger.png'),
                        ('Other', '/other', '/static/img/other.png'),
                        ('Setting', '/setting', '/static/img/setting.png'),
                    ]
                %>
                % for item in ls:
                    <div class="col-sm-6 p-1">
                        <a href="${item[1]}">
                            <div class="card m-0 pos-relative">
                                <img src="${item[2]}" alt="">
                                <h1 class="bottom-right">${item[0]}</h1>
                            </div>
                        </a>
                    </div>
                % endfor
            </div>
        </div>
    </div>