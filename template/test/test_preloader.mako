<%inherit file="base.mako"/>
<%block name="title">
    Preloader test
</%block>
## <%block name="extracss">
## </%block>
<%block name="extrajs">
    <script src="/static/js/util/loader.js"></script>
</%block>
<%block name="script">
    <script>
        var loader = new PagePreLoader(20, function(page, perpage) {
            return new Promise((resolve) => {
                socket.emit('cyoa_image_data', {page:page, perpage:perpage, cyoaId:1}, function(data) {
                    resolve(JSON.parse(data));
                });
            });
        });

        async function loadPage() {
            let num = parseInt($('#pagenum').val());
            let data = await loader.get(num);
            $('#result').text(JSON.stringify(data, null, 2));
        }
    </script>
</%block>

<% ls_perpage = [40, 80, 100, 200, 0] %>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<div class="bg-darkblue">
    <div class="container-lg bg-d25-darkblue p-2">
        <div class="control-group">
            <input class="form-control" type="number" id="pagenum" value="1" min="1">
            <button class="btn btn-primary ml-2" id="btn-load" onclick="loadPage()">Load Page</button>
        </div>
        <pre class="card mt-2 p-1" id="result">Result here...</pre>
    </div>
</div>

