<%inherit file="base.mako"/>
<%block name="title">
    Touch gesture test
</%block>
<%block name="extracss">
    <style>
        .body {
            position: relative;
        }
        .drag {
            position: absolute;
            top: 80px;
            left: 150px;
            width: 200px;
            height: 200px;
        }
    </style>
</%block>
<%block name="extrajs">

</%block>
<%block name="script">
    <script src="/static/js/test_touch.js"></script>
</%block>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<div class="bg-darkblue">
    <div class="container-lg bg-d25-darkblue p-2">
        <div class="body">
            <div class="card drag img-container" id="drag-card" draggable="false">
                <img src="/static/img/no-image.png" alt="" draggable="false" style="pointer-events: none;">
            </div>
        </div>

        <div id="scroller" class="progress-bar mt-4" style="height:40px">
            <div class="value" style="width:25%"></div>
        </div>
    </div>
</div>

