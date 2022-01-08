<!DOCTYPE html>
<html lang="">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/css/style.css">
        <link rel="stylesheet" href="/static/css/fontawesome.css">
        <link rel="stylesheet" href="/static/css/sidebar.css">
        <%block name="extracss" />
        <title><%block name="title" /></title>
    </head>
    <body <%block name="bodyprop" />>
        <%include file="component/navbar.mako"/>
        <%include file="component/sidebar.mako"/>
        ${self.body()}
        <script src="/static/js/lib/jquery-3.6.0.min.js"></script>
        <script src="/static/js/lib/socket.io.min.js"></script>
        <script src="/static/js/script.js"></script>
        <%block name="extrajs" />
        <%block name="script" />
    </body>
</html>
