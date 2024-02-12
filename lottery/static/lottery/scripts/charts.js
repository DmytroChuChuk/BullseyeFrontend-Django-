// chart_stuff();
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
// function change_graph() {
//     console.log("CHANGE GRAPH");
// }
//
// function populate_chart() {
//     console.log("POPULATE GRAPH");
// }
//
// function chart_stuff() {
//     const ctx = document.getElementById('myChart');
//
//   new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//       datasets: [{
//         label: '# of Votes',
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1
//       }]
//     },
//     options: {
//       scales: {
//         y: {
//           beginAtZero: true
//         }
//       }
//     }
//   });
// }