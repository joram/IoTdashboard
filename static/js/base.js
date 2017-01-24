
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
    $('.grid-stack').on('change', layout_change);
    update_dashboard_list();
}


function layout_change(event, items) {
    serializedData = _.map($('.grid-stack > .grid-stack-item:visible'), function (el) {
        el = $(el);
        var node = el.data('_gridstack_node');
        return {
            x: node.x,
            y: node.y,
            width: node.width,
            height: node.height
        };
    }, this);
    data = JSON.stringify(serializedData, null, '    ');

    $.ajax({
      type: "POST",
      url: "/ajax/dashboard/default",
        data: data,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
    });
    console.log("layout changed")
};


function update_dashboard_list() {
    dashboards_list = $("#dashboards_list")
    dashboards_list.empty()

    $.getJSON( "/ajax/dashboards", function( data ) {
        $.each( data, function( key, val ) {
            $anchor = $("<a>"+val+"</a>");
            $item = $("<li></li>");
            $item.append($anchor);
            dashboards_list.append($item);
            $item.click(function(){load_dashboard(val)});
        });
    });
};


function load_dashboard(slug){
    $.ajax({
        type: "GET",
        url: "/ajax/dashboard/"+slug,
        success: function( data ) {
            this.grid = $('.grid-stack').data('gridstack');
            this.grid.removeAll();
            $panels = JSON.parse(data)
            $.each($panels, function(key, panel ) {
                add_panel(panel.title, panel.content, panel.x, panel.y, panel.width, panel.height)
            })
        }
    })
}


function add_panel(title, content, x, y, w, h){
    panel = $(`
    <div>
        <div class="grid-stack-item-content panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">`+title+`</h3>
            </div>
            <div class="panel-body">`+content+`</div>
        </div>
    </div>`);

    this.grid.addWidget(panel, x, y, w, h);
}