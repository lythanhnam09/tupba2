<nav class="nav ${nav.theme} shadow-md pos-sticky-top">
    <div class="nav-container-left">
        % if nav.show_menu_button:
            <div id="btn-menu" class="nav-item px-2" title="Menu" onclick="toggleSidebar()">
                <i class="fas fa-bars"></i>
            </div>
        % endif
        % if len(nav.left_buttons) > 0:
            <div id="btn-exp-left" class="nav-item nav-expand-button px-2" title="Navigation option" onclick="toggleExpandable('exp-left', 'btn-exp-left')">
                <i class="fas fa-ellipsis-v"></i>
            </div>
        % endif
        <div id="exp-left" class="nav-expandable left" style="display: none">
            % for button in nav.left_buttons:
                ${button.html()}
            % endfor
        </div>
        <a class="nav-title" {{nav.show_title_href()}}>
            <h2 class="fg-warning" ${'style="font-size:%s"' % nav.title_size if nav.title_size != None else ''}>${nav.title}</h2>
        </a>
    </div>
    <div class="nav-container-right">
        % if len(nav.left_buttons) > 0:
            <div id="btn-exp-right" class="nav-item nav-expand-button px-2" title="Navigation option" onclick="toggleExpandable('exp-right', 'btn-exp-right', false)">
                <i class="fas fa-ellipsis-v"></i>
            </div>
        % endif
        <div id="exp-right" class="nav-expandable right" style="display: none">
            % for button in nav.right_buttons:
                ${button.html()}
            % endfor
        </div>
    </div>
</nav>
% if nav.show_progress:
<div class="nav-progress top-previous">
    <div id="mark-container" class="mark-container">
        ## <div class="qm-mark" style="left:12px"></div>
    </div>
    <div id="nav-progress-value" class="value"></div>
</div>
% endif