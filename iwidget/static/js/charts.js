// This js file is based on the 2013-07-29 version of the hcharts
// application of enhydris template.

var cd=[];
var vm=[];
var cm=[]; 
var cs=[];
var cc=0;
auto_refresh = false; // TODO: something meaningful
auto_refresh_interval = 30000; // TODO: something meaningful

function gup( name )
{
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var results = regex.exec( window.location.href );
    if( results == null )
        return "";
    else
        return results[1];
}

function addChart(options){
    cm[cc]=options;
    cm[cc]['iter']=cc;
    cm[cc]['is_zoomed']=false;
    vm[cc]=[];
    cd[cc]=[];
    cs[cc]=[];
    cc++;
}

function addVariable(options){
    var chart_id = options['chart_id'];
    for(var i=0;i<cc;i++)
        if(cm[i]['id']==chart_id)
        {
            var chart_i = i;
            break;
        }
    var j = vm[chart_i].length;
    vm[chart_i][j] = options;
}

function get_data_from_server(i)
{
    $("#chartarea"+cm[i]['id']).append("<img style=\"margin: auto; position: absolute; left: 240px; top: 100px; \" src=\""+STATIC_URL+"images/icons/progress.gif\">");
    for(var j=0;j<vm[i].length;j++)
        vm[i][j]['status']=false;
    var achart_status=false;
    for(var j=0;j<vm[i].length;j++)
    {
        var url_params = {object_id: vm[i][j]['series_id'], last: cm[i].time_span};
        if(gup('date'))
        {   url_params['date'] = gup('date');
            if(gup('time'))url_params['time'] = unescape(gup('time'));
        }
        if(cm[i]['is_vector'])
            url_params['vector']="true";
        $.getJSON(js_data.timeseries_data_url, url_params, 
            (function(i,j){
            return function(chart_data){
            var astatus=true;
            if(chart_data){
                cd[i][j]=chart_data['data'];
                for(var t=0;t<chart_data['data'].length;t++)
                {
                    if(cd[i][j][t][1]!='null')
                        cd[i][j][t][1] = parseFloat(cd[i][j][t][1])*vm[i][j]['factor'];
                    cd[i][j][t][3] = cd[i][j][t][2];
                    cd[i][j][t][2] = 0;
                }
                cs[i][j]=chart_data['stats'];
                vm[i][j]['status']=true;
            }
            for(var k=0;k<vm[i].length;k++)
                astatus = astatus && vm[i][k]['status'];
            if(astatus)
            {
                achart_status=true;
                $("#chartarea"+cm[i]['id']).remove(":contains('img style')");
                if(cm[i]['can_zoom'])$("#unzoom"+cm[i]['id']).hide();
                flot_init(i);
            }
        }})(i,j));
    }
//            if(!achart_status)
//                 $("#data_holder"+cm[i]['id']).html("<h3>No data locally available!</h3>");

}

function chartUnzoom(id)
{
    var i, j;
    i=-1;
    for(j=0;j<cm.length;j++)
        if(cm[j]['id']==id)
        {
            i = j;
            break;
        }
    if(i>-1){
        $("#chartarea"+cm[i]['id']).unbind("plotselected");
        $("#chartarea"+cm[i]['id']).unbind("plothover");
        get_data_from_server(i);    
        cm[i]['is_zoomed']=false;
    }
}

var span_change = function(identifier)
{
    var elements = identifier.split('_');
    var id = elements[1];
    var span = elements[2];
    var selector = $('#textarea'+id)
    selector.find('.js-span-link').show();
    selector.find('.js-span-static').hide();
    $('#js-span-link_'+id+'_'+span).hide();
    $('#js-span-static_'+id+'_'+span).show();
    var i, j;
    i=-1;
    for(j=0;j<cm.length;j++)
        if(cm[j]['id']==id)
        {
            i = j;
            break;
        }
    if(i>-1){
        cm[i]['time_span'] = span;
        $("#chartarea"+cm[i]['id']).unbind("plotselected");
        $("#chartarea"+cm[i]['id']).unbind("plothover");
        get_data_from_server(i);    
        cm[i]['is_zoomed']=false;
    }
};

function refresh_chart()
{
    if(gup('date')||gup('time'))
        return;
    for(var i=0;i<cc;i++)
    {
        if(cm[i]['is_zoomed'])
            continue;
        $("#chartarea"+cm[i]['id']).unbind("plotselected");
        $("#chartarea"+cm[i]['id']).unbind("plothover");
        get_data_from_server(i);
    }
}

function load_initial_data()
{
    for(var i=0;i<cc;i++)
        get_data_from_server(i);
    if(auto_refresh)
        setInterval("refresh_chart()", auto_refresh_interval)
}

$(document).ready(function() {
    $("input.date").datepicker({ dateFormat: 'yy-mm-dd' });
    $("input.time").timePicker();
    $("input.date").val(gup('date'));
    if($("input.date").val())
        $("input.time").val(unescape(gup('time')));
    $("input.last").val(gup('last'));
    if($("input.date").val()||$("input.time").val())
        $("#date_select_form").show();
    $('.date_select').collapser({target: 'next', targetOnly: 'div',
                                 effect: 'fade', changeText: true,
                                 expandHtml: "Go to a specific date and reload charts",
                                 collapseHtml: "Hide date selection - Show recent (last) measurements",
                                 expandClass: 'expArrow', collapseClass: 'collArrow'},
                                 function(){},
                                 function(){
                                     if($("#date_select").hasClass("expArrow"))
                                         window.location=location.pathname;
                                 });
    var tooltipopts = {
                       position: 'bottom right',
                       offset: [-65, 10],
                       effect: 'fade'
    };
    for(i=0;i<js_data.charts.length;i++)
    {
        var avgpc;
        if('occupancy' in js_data.charts[i])
            avgpc = js_data.charts[i].occupancy;
        else
            avgpc = false;
        addChart({id: js_data.charts[i].id,
                  name: js_data.charts[i].name, 
                  min: js_data.charts[i].display_min,
                  max: js_data.charts[i].display_max,
                  avg: js_data.charts[i].display_avg,
                  avgpc: avgpc,
                  has_stats: js_data.charts[i].has_stats,
                  can_zoom: js_data.charts[i].can_zoom,
                  is_vector: js_data.charts[i].is_vector,
                  time_span: js_data.charts[i].time_span,
                  has_pie: js_data.charts[i].has_pie
                 });
        $("#chartarea"+js_data.charts[i].id).tooltip(tooltipopts);
    }

    for(i=0;i<js_data.variables.length;i++)
        addVariable({id:js_data.variables[i].id,
                     name:js_data.variables[i].name,
                     is_bar: js_data.variables[i].is_bar,
                     bar_width: js_data.variables[i].bar_width,
                     factor: js_data.variables[i].factor,
                     series_id:js_data.variables[i].timeseries_id,
                     chart_id: js_data.variables[i].chart_id});

    $('.js-span-link').click(function(e){
        span_change($(this).attr('id'));
        e.preventDefault();
    });
    load_initial_data();
});

function format_date(timestamp){
    if(timestamp==null)
        return '-';
    var hours, minutes, zoneCorrection;
    adate = new Date(timestamp);
    zoneCorrection=60000*adate.getTimezoneOffset();
    timestamp+=zoneCorrection;
    adate = new Date(timestamp);
    result = adate.getFullYear();
    result = result+'/'+(adate.getMonth()+1)+'/'+adate.getDate()+' ';
    hours = adate.getHours();
    minutes = adate.getMinutes();
    if(hours<10) hours='0'+hours;
    if(minutes<10) minutes='0'+minutes;
    result = result+hours+':'+minutes;
    return result;
}

function format_float(avalue){
    if(avalue==null)
        return '-';
    return avalue.toFixed(2);
}

function get_zoomed_data(i, ranges, datas){
    var from_pos, to_pos;
    var actual_xaxis_from, actual_xaxis_to;
    $("#chartarea"+cm[i]['id']).append("<img style=\"margin: auto; position: absolute; left: 240px; top: 100px; \" src=\""+STATIC_URL+"images/icons/progress.gif\">");
    for(var j=0;j<vm[i].length;j++)
        vm[i][j]['status']=false;
    var achart_status=false;
    $("#chartarea"+cm[i]['id']).unbind("plotselected");
    $("#chartarea"+cm[i]['id']).unbind("plothover");
    for(var j=0;j<vm[i].length;j++)
    {
        var data = datas[j]['data'];
        from_pos = data[0][3];
        to_pos = data[data.length-1][3];
        for(var k=0;k<data.length;k++){
            if(ranges.xaxis.from<=data[k][0]){
                from_pos = data[k][3];
                actual_xaxis_from = data[k][0];
                break;
            }
        }
        for(var k=data.length-1;k>=0;k--){
            if(ranges.xaxis.to>=data[k][0]){
                to_pos = data[k][3];
                actual_xaxis_to = data[k][0];
                break;
            }
        }
        var urlparams = {object_id: vm[i][j]['series_id'],
                         start_pos:from_pos, end_pos:to_pos}; 
        if(cm[i]['is_vector'])
            urlparams['vector']='true';
        $.getJSON(js_data.timeseries_data_url, urlparams, 
            (function(i,j){
            return function(chart_data){
            var astatus=true;
            if(chart_data){
                cd[i][j]=chart_data['data'];
                for(var t=0;t<chart_data['data'].length;t++)
                {
                    if(cd[i][j][t][1]!='null')
                        cd[i][j][t][1] = parseFloat(cd[i][j][t][1])*vm[i][j]['factor'];
                    cd[i][j][t][3] = cd[i][j][t][2];
                    cd[i][j][t][2] = 0;
                }
                cs[i][j]=chart_data['stats'];
                vm[i][j]['status']=true;
            }
            for(var k=0;k<vm[i].length;k++)
                astatus = astatus && vm[i][k]['status'];
            if(astatus)
            {
                achart_status=true;
                $("#chartarea"+cm[i]['id']).remove(":contains('img style')");
                flot_init(i);
                if(cm[i]['can_zoom'])$("#unzoom"+cm[i]['id']).show();
           }
        }})(i,j));
    }
    cm[i]['is_zoomed']=true;
}

var charts = [];

var redraw_charts = function(index){
    for(var i=0;i<charts.length;i++)
    {
        var chart = charts[i].plot_object;
        if (index!=undefined && index!=charts[i].index)
            continue
        chart.setupGrid();
        chart.draw();
    }
};

function flot_init(i) {
    var from_x, to_x, tol;
    var d = [];
    for(var j=0;j<cd[i].length;j++){
        d[j] = {label: vm[i][j]['name'], data: cd[i][j]}
        if(('is_bar' in vm[i][j]) && (vm[i][j]['is_bar']))
            d[j]['bars'] = {show: true, fill: true,
                    barWidth: vm[i][j]['bar_width']};
    }
    if(cm[i]['is_vector'])
    {
        var x0, x1, y0, y1, t0, t1, u0, u1;
        for(var k=d[0]['data'].length-1;k>0;k--)
        {
            y0 = d[0]['data'][k-1][1], y1 = d[0]['data'][k][1];
            if(y0=='null' || y1=='null')
                continue;
            if(Math.abs(y1-y0)>180)
            {
                x0 = d[0]['data'][k-1][0], x1 = d[0]['data'][k][0];
                t0 = d[0]['data'][k-1][2], t1 = d[0]['data'][k][2];
                u0=(y0<180?0:360)
                u1=(y1<180?0:360)
                d[0]['data'].splice(k, 0, [x0+0.25*(x1-x0), u0, t0], [0.5*(x0+x1), 'null', t1],
                                          [x1-0.25*(x1-x0), u1, t1]);
            }

        }
    }
    from_x = d[0]['data'][0][0];
    to_x = d[0]['data'][d[0]['data'].length-1][0];
    start_pos = d[0]['data'][0][3];
    end_pos = d[0]['data'][d[0]['data'].length-1][3];
    tol = (to_x-from_x)*0.01;
    from_x-=tol;
    to_x+=tol;
    var marking_opts = [];
    if(cm[i]['has_stats']){
        var stats= cs[i][0];
        if(cm[i]['is_vector'])
            stats['avg'] = stats['vavg']
        if(cm[i]['avgpc'])
            stats['avgpc'] = stats['avg'] / cm[i]['avgpc'];
        var items = ['max', 'min', 'last', 'avg', 'sum', 'avgpc'];
        for(var item in items)
            stats[items[item]] = stats[items[item]] * vm[i][0]['factor'];
        for(var item in items)
            $('#'+items[item]+cm[i]['id']).text(format_float(stats[items[item]]));
        items = items.slice(0,3);
        for(item in items){
        //Fix time zone UGLY
            $('#'+items[item]+'_tstmp'+cm[i]['id']).text(format_date(stats[items[item]+'_tstmp']));
        }
        if(cm[i]['min'])
            marking_opts = marking_opts.concat([ { yaxis: { from: stats['min'], to: stats['min'] } , color: "#8888aa"},  
                    { xaxis: { from: stats['min_tstmp'], to: stats['min_tstmp'] } , color: "#ddddff"}]);
        if(cm[i]['max'])
            marking_opts = marking_opts.concat([ { yaxis: { from: stats['max'], to: stats['max'] } , color: "#aa8888"},  
                    { xaxis: { from: stats['max_tstmp'], to: stats['max_tstmp'] } , color: "#ffdddd"}]);
        if(cm[i]['avg'])
            marking_opts.push( { yaxis: { from: stats['avg'], to: stats['avg'] } , color: "#88aa88"});
    }
    var options = {
        xaxis: { mode: "time", timeformat: "%y/%m/%d %H:%M",
        min: from_x, max: to_x, ticks: 5},
        selection: { mode: "x" },
        grid:{markings: marking_opts, hoverable: true,
              autoHighlight: false},
        legend: {show: (d.length>1), position: 'nw'}
    };
    if(cm[i]['is_vector'])
        options['yaxes'] = [ {position: "left", min:0, max:360, show: true,
        ticks: [0, 45, 90, 135, 180, 225, 270, 315, 360]},
            {position: "right", ticks: [[0, 'N'], [45, 'NE'], [90, 'E'],
                  [135, 'SE'], [180, 'S'], [225, 'SW'],
                  [270, 'W'], [315, 'NW'], [360, 'N']], show: true}];
    var plot = $.plot($("#chartarea"+cm[i]['id']), d, options);
    charts.push({index: cm[i]['id'], plot_object: plot});
    $("#chartarea"+cm[i]['id']).unbind("plotselected");
    $("#chartarea"+cm[i]['id']).unbind("plothover");
    if(cm[i]['can_zoom'])
        $("#chartarea"+cm[i]['id']).bind("plotselected", function (event, ranges) {
            get_zoomed_data(i, ranges, d);
        });
    $("#chartarea"+cm[i]['id']).bind("plothover", function(event, pos, item){
        $("#charttooltip"+cm[i]['id']).html('<div>'+format_date(pos.x)+'</div>');
        $("#charthover"+cm[i]['id']).html('<div class=""><kbd>'+format_date(pos.x)+'</kbd></div><br/>'); //added by Adeel on 18 March 2014
    });
    $("#chartarea"+cm[i]['id']).mouseout(function(){
        $("#charttooltip"+cm[i]['id']).html('');
        $("#charthover"+cm[i]['id']).html(''); //added by Adeel on 18 March 2014
    });
    global_plot = plot;
    plot.setupGrid();
    plot.draw()
    if(cm[i]['is_vector'])
    {
        var alabel = '';
        var data2 = [];
        var d2 = [];
        for(k=0;k<cs[i].length;k++)
        {
            d2[k]=[];
            for(j=0;j<8;j++)
            {
                d2[k][j] = [];   
                d2[k][j][0]=j, d2[k][j][1]=cs[i][k]['vectors'][j];
            }
            if(cs[i].length>1)
                alabel =  vm[i][k]['name'];
            data2[k]={data: d2[k], spider: {show: true}, label: alabel};
        }
        var rose = $.plot($("#rosearea"+cm[i]['id']),data2,
                            { series: { spider: {active: true,
                              scaleMode: 'all',
                              legs: { data: [{label: 'N'}, {label: 'NE'},
                              {label: 'E'}, {label: 'SE'}, {label: 'S'},
                              {label: 'SW'}, {label: 'W'}, {label: 'NW'}],
                              legStartAngle: 270, fillStyle: "blue"},
                              grid: {mode: "radar"}}}});
        charts.push({index: cm[i]['id'], plot_object: rose});
    }
    if(cm[i].has_pie!=undefined)
    {
        var pie = js_data.pies[cm[i].has_pie];
        $.ajax({
            url: js_data.periods_stats_url,
            data: {
                object_id: pie.timeseries_id,
                period_unit: pie.period_unit,
                period_from: pie.period_from,
                period_to: pie.period_to,
                start_pos: start_pos,
                end_pos: end_pos
            },
            success: function(data){
                if (!data||!data.stats)
                    return
                var pie_data = [];
                pie_data[0] = {};
                pie_data[0].label = pie.default_period;
                pie_data[0].data =  data.stats.default_period;
                pie_data[1] = {};
                pie_data[1].label = pie.alternate_period;
                pie_data[1].data = data.stats.alternate_period;
                var pie_plot = $.plot($("#piediv"+cm[i].has_pie), pie_data,
                {
                        series: {
                            pie: {
                                show: true,
                                radius: 1,
                                label:{
                                    show: true,
                                    radius: 3/4,
                                    formatter: function(label, series){
                                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                                                +series.percent
                                                .toFixed(1) + '%'
                                                +'</div>'
                                    },
                                    background: { opacity: 0.7 }
                                }
                            }
                        }
                });
                charts.push({index: cm[i]['id'],
                        plot_object: pie_plot});
            }
        });
    }
}

