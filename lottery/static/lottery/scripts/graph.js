
common_init("side_charts_graphs", true,false);
//common_init("side_latest_results", buildFavoritesDisplay, false, "My Favorites", false);
//
// console.log("BEFORE");
//
// let draw;
// let graph_ball_data = {};
// let x_axis = [];
// let data_set = {};
// let history_data_to_use = {};
//
// $('#graphType').on('change', function () {
//     console.log("In update chart type");
//     change_graph();
// });
// $('#displayType').on('change', function () {
//     console.log("In update display type");
//     change_graph();
// });
// $('#ballType').on('change', function () {
//     console.log("In update ball type");
//     change_graph();
// });
// $('#myRange').on('change', function () {
//     console.log("In update chart range");
//     document.getElementById("rangeValue").innerText = "Draws: " + $('#myRange').val();
//     populate_chart();
// });
//
// function populateWithFavData() {
//     topDataBarSetup(populate_chart, true);
//     call_for_lottery_history(populate_chart, null);
// }
//
// function getTopElements(limit) {
//     let data = {};
//     let i = 0;
//     for(let r in history_data) {
//         if(i < limit) {
//             data[r] = history_data[r];
//             i++;
//         }
//         else
//             return data;
//     }
//     return data;
// }
//
// function populate_chart() {
//     let table = document.getElementById("data_table");
//     if (table != null) {
//         return;
//     }
//     console.log("Call start calculation");
//     draw = Number($('#myRange').val());
//
//     // get subset of data to use
//     history_data_to_use = getTopElements(draw);
//
//     build_graph_data();
//
//     change_graph();
// }
//
// function change_graph() {
//     let g_type = $('#graphType').val();
//     // draw = Number($('#myRange').val());
// //        draw_data = dataArray.slice(Math.max(0, draw));
//     if(g_type == "ballFreq") {
//         graph_ball_frequency(false);
//     } else if(g_type == "ballSumSymbols"){
//         graph_ball_frequency(true);
//     } else if(g_type == "ballSum"){
//         graph_ball_sum();
//     } else if(g_type == "pairs"){
//         graph_ball_pairs();
//     } else if(g_type == "triplets"){
//         graph_ball_triplets();
//     } else if(g_type == "ballInDraw"){
//         graph_ball_in_draw();
//     } else if(g_type == "oddEven"){
//         graph_ball_odd_even();
//     } else if(g_type == "summary"){
//         graph_ball_summary();
//     } else if(g_type == "deltas"){
//         graph_ball_deltas();
//     }
// }
//
// function build_graph_data() {
//     graph_ball_data = {};
//
//     // BALL FREQUENCY
//
//     let count = {};
//     data_set = {};
//     x_axis = [];
//     let chart_data = [];
//    // let ball = [];
//     let balls = [];
//
//     let index = 0;
//     Object.keys(history_data_to_use).forEach((key) => {
//         index = index + 1;
//         let nData = history_data_to_use[key]["Balls"].split(',');
//         nData.forEach((k)=>{
//             balls.push(Number(k));
//         });
//     });
//     console.log("INDEX COUNT: " + index);
//     balls.forEach(function(i) { count[i] = (count[i]||0) + 1;});
//     Object.keys(count).forEach((key) => {
//         x_axis.push(key);
//         chart_data.push(count[key]);
//     });
//
//     data_set['x_axis'] = x_axis;
//     data_set['chart_data'] = chart_data;
//     graph_ball_data['ball_frequency'] = data_set;
//
//     // BALL SUM
//
//     // let count = {};
//     // let data_set = {};
//     // let x_axis = [];
//     // let chart_data = [];
//     // let sum = [];
//
//     // Object.keys(draw_data).forEach((key) => {
//     //     let nData = draw_data[key]["Balls"].split(',');
//     //     sum = nData.reduce(add, 0);
//     // });
//     // balls.forEach(function(i) { count[i] = (count[i]||0) + 1;});
//     // Object.keys(count).forEach((key) => {
//     //     x_axis.push(key);
//     //     chart_data.push(count[key]);
//     // });
//
//     // data_set['x_axis'] = x_axis;
//     // data_set['chart_data'] = chart_data;
//     // graph_ball_data['ball_sum'] = data_set;
// }
//
// // 'column'
// // 'BALL FREQUENCY A'
// // 'Number of times each ball number has appeared in the '+draw+' draws'
// //
// // Times
// // '<span style="font-size:10px">{point.key}</span><table>'
// // '<tr><td style="color:{series.color};padding:0">{series.name}: </td><td style="padding:0"><b>{point.y:.0f} times</b></td></tr>'
// // '</table>'
// // 'Ball'
// function update_chart(title, sub_title, x_axis, y_axis_text, header_format, point_format, footer_format, chart_series) {
//     //series_name_array, chart_data_array, chart_color_array
// //     series: [{
// //         name: series_name,
// //         data: chart_data,
// //         color: "#37adb1"
// //     }]
//   Highcharts.chart('container', {
//         chart: {
//             type: $('#displayType').val(),
//             backgroundColor: "#0d1e25"
//         },
//         title: {
//             text: title
//         },
//         subtitle: {
//             text: sub_title
//         },
//         xAxis: {
//             categories: x_axis,
//             crosshair: true
//         },
//         yAxis: {
//             min: 0,
//             title: {
//                 text: y_axis_text
//             }
//         },
//         tooltip: {
//             headerFormat: header_format,
//             pointFormat: point_format,
//             footerFormat: footer_format,
//             shared: true,
//             useHTML: true
//         },
//         plotOptions: {
//             column: {
//                 pointPadding: 0.2,
//                 borderWidth: 0
//             }
//         },
//         series: chart_series
//     });
// }
//
// function graph_ball_frequency(use_symbols) {
// //         count = {};
// //         x_axis = [];
// //         chart_data = [];
//
// //         Object.keys(draw_data).forEach((key) => {
// //             let nData = draw_data[key]["Balls"].split(',');
// //             nData.forEach((k)=>{
// //                 balls.push(Number(k));
// //             });
// //         });
// // //        balls = balls.sort();
// //         balls.forEach(function(i) { count[i] = (count[i]||0) + 1;});
//
// //         Object.keys(count).forEach((key) => {
// //             x_axis.push(key);
// //             chart_data.push(count[key]);
// //         });
//
//     let display_type = $('#displayType').val();
//
//     Highcharts.chart('container', {
//         chart: {
//             type: display_type,
//             backgroundColor: "#0d1e25"
//         },
//         title: {
//             text: 'BALL FREQUENCY'
//         },
//         subtitle: {
//             text: 'Number of times each ball number has appeared in the '+draw+' draws'
//         },
//         xAxis: {
//             categories: graph_ball_data['ball_frequency']['x_axis'],
//             crosshair: true
//         },
//         yAxis: {
//             min: 0,
//             title: {
//                 text: 'Times'
//             }
//         },
//         tooltip: {
//             headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
//             pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
//                 '<td style="padding:0"><b>{point.y:.0f} times</b></td></tr>',
//             footerFormat: '</table>',
//             shared: true,
//             useHTML: true
//         },
//         plotOptions: {
//             column: {
//                 pointPadding: 0.2,
//                 borderWidth: 0
//             }
//         },
//         series: [{
//             name: 'Ball',
//             data: graph_ball_data['ball_frequency']['chart_data']
//         }]
//     });
//  }
//
// function graph_ball_sum() {
//     let count = {};
//     let x_axis = [];
//     let chart_data1 = [];
//     let chart_data2 = [];
//     let total = 0;
//     let et = 0, t = 0;
//
//     Object.keys(history_data_to_use).forEach((key) => {
//         let nData = history_data_to_use[key].split(',');
//         et = 0;
//         nData.forEach((k)=>{
//             et = et + Number(k);
//         });
//
//         chart_data1.push(et);
//         total = total + et;
//         t++;
//     });
//     let avg = total/t;
//
//     for(i=0;i<draw;i++){
//         chart_data2.push(Number(avg.toFixed(2)));
//         x_axis.push(i+1);
//     }
//
//     Highcharts.chart('container', {
//         chart: {
//             type: 'column'
//         },
//         title: {
//             text: 'BALL SUM'
//         },
//         subtitle: {
//             text: 'Sum of all the balls in each draw'
//         },
//         xAxis: {
//             categories: x_axis,
//             title: {
//                 enabled: true,
//                 text: 'Number of Draws'
//             }
//         },
//         yAxis: {
//             min: 0,
//             title: {
//                 text: 'Sum'
//             }
//         },
//         tooltip: {
//             headerFormat: '<span style="font-size:10px">Draw: {point.key}</span><table>',
//             pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
//                 '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
//             footerFormat: '</table>',
//             shared: true,
//             useHTML: true
//         },
//         plotOptions: {
//             column: {
//                 pointPadding: 0.2,
//                 borderWidth: 0
//             }
//         },
//         series: [{
//             name: 'Sum',
//             data: chart_data1
//         },{
//             name: 'Average',
//             data: chart_data2
//         }]
//     });
//
//
// }
// function graph_ball_pairs() {
//     let count = {};
//     let x_axis = [];
//     let pairs = [];
//     let chart_data1 = [];
//     let total = 0;
//     let et = 0, t = 0;
//
//     Object.keys(history_data_to_use).forEach((key) => {
//         let nData = history_data_to_use[key].split(',');
//         for(i=0;i<nData.length;i++){
//             let x = Number(nData[i])+1;
//             let y  = (i != (nData.length - 1)) ? nData[i+1] : nData[i];
//             if(x == y){
//                 pairs.push(nData[i]+"-"+y);
//             }
//         }
//     });
//     pairs.forEach(function(i) { count[i] = (count[i]||0) + 1;});
//
//     Object.keys(count).forEach((key)=>{
//         chart_data1.push(count[key]);
//         x_axis.push(key.replace('-',','));
//     });
//
//     Highcharts.chart('container', {
//         chart: {
//             type: 'column'
//         },
//         title: {
//             text: 'NUMBER PAIRS'
//         },
//         subtitle: {
//             text: 'Number of times in a draw that there are two numbers in a row'
//         },
//         xAxis: {
//             categories: x_axis
//         },
//         yAxis: {
//             min: 0,
//             title: {
//                 text: 'Times'
//             }
//         },
//         tooltip: {
//             headerFormat: '<span style="font-size:10px">Pair: {point.key}</span><table>',
//             pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
//                 '<td style="padding:0"><b>{point.y:.0f} times</b></td></tr>',
//             footerFormat: '</table>',
//             shared: true,
//             useHTML: true
//         },
//         plotOptions: {
//             column: {
//                 pointPadding: 0.2,
//                 borderWidth: 0
//             }
//         },
//         series: [{
//             name: 'Pair',
//             data: chart_data1
//         }]
//     });
// }
//
//
//
