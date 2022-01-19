<%inherit file="../base.mako"/>
<%block name="title">
    Booru Browser - Filters
</%block>
<%block name="extracss">
    <link rel="stylesheet" href="/static/css/booru.css">
</%block>
<%block name="extrajs">
    <script src="/static/js/booru/booru.js"></script>
    <script src="/static/js/booru/filter.js"></script>
</%block>

<%def name="form_option(form, name, value, text)">
    <option value="${value}" ${form.option_selected(name, value)}>${text}</option>
</%def>

<div class="bg-d10-dark">
    <div class="container-lg bg-d5-dark py-2">
        <h1 class="text-center">Filters</h1>
        <hr class="my-1">
        <div class="control-group gap-1 px-1">
            <button class="btn btn-primary" onclick="showFilterDailog('Create New Filter')"><i class="fas fa-plus"></i> New filter</button>
            <button class="btn btn-success" onclick="saveFilter()"><i class="fas fa-save"></i> Save</button>
        </div>
        <hr class="my-1">

        <div class="px-1">
            % if len(ls_filter) == 0:
                <h2 class="fg-secondary text-center my-3">No filter here</h2>
            % endif
            % for filter in ls_filter:
                <div class="card my-1 bg-dark">
                    <div class="card-content p-1 bg-dark">
                        <div class="control-group vflex-center gap-1">
                            % if filter['checked']:
                                <input type="checkbox" id="ck-filter-${filter['id']}" class="ck-filter" data-id="${filter['id']}" checked>
                                <label class="flex-grow fg-success" for="ck-filter-${filter['id']}"><b>${filter['name']}</b></label>
                            % else:
                                <input type="checkbox" id="ck-filter-${filter['id']}" class="ck-filter" data-id="${filter['id']}">
                                <label class="flex-grow" for="ck-filter-${filter['id']}">${filter['name']}</label>
                            % endif
                            
                            <div>
                                % if filter['show_count'] > 0:
                                    <div class="d-iblock fg-success mr-1"><i class="fas fa-eye"></i> ${filter['show_count']}</div>
                                % endif
                                % if filter['spoiler_count'] > 0:
                                    <div class="d-iblock fg-warning mr-1"><i class="fas fa-eye-slash"></i> ${filter['spoiler_count']}</div>
                                % endif
                                % if filter['hide_count'] > 0:
                                    <div class="d-iblock fg-danger mr-1"><i class="fas fa-ban"></i> ${filter['hide_count']}</div>
                                % endif
                            </div>
                            <div class="control-group-round">
                                % if loop.index >= 1:
                                    <button class="btn-transparent px-1" onclick="swapFilterOrder(${filter['id']}, ${ls_filter[loop.index - 1]['id']})"><i class="fas fa-arrow-up"></i></button>
                                % else:
                                    <button class="btn-transparent px-1" disabled><i class="fas fa-arrow-up"></i></button>
                                % endif
                                % if loop.index < len(ls_filter) - 1:
                                    <button class="btn-transparent px-1" onclick="swapFilterOrder(${filter['id']}, ${ls_filter[loop.index + 1]['id']})"><i class="fas fa-arrow-down"></i></button>
                                % else:
                                    <button class="btn-transparent px-1" disabled><i class="fas fa-arrow-down"></i></button>
                                % endif
                            </div>
                            <button class="btn-transparent px-1" onclick="showFilterDailog('Edit Filter', true, ${filter['id']}, '${filter['name']}', '${filter['filter_text']}')"><i class="fas fa-pencil"></i></button>
                            <button class="btn-transparent btn-danger px-1" onclick="deleteFilter(${filter['id']}, '${filter['name']}')"><i class="fas fa-times"></i></button>
                        </div>
                    </div>
                </div>
            % endfor
        </div>
    </div>
</div>

