
$(document).ready(function(){
    init();
});


function init() {
    var options = {
        height:20,
    };
    $('.grid-stack').gridstack(options);
    this.grid = $('.grid-stack').data('gridstack');
    add_panel("hello world", "hello body", 1, 0, 4, 4);
    add_panel("hello world 2", "hello body", 0, 1, 4, 4);
    console.log("inited")
}

function add_panel(title, content, x, y, w, h){
    panel = $(`
    <div>
        <div class="grid-stack-item-content panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Panel title</h3>
            </div>
            <div class="panel-body">Panel content</div>
        </div>
    </div>`);

    this.grid.addWidget(panel, x, y, w, h);
}