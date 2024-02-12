//document.cookie = "username=John Doe";
jQuery(document).ready(function () {
    let g_type, draw, i, len, draw_data;
    let graph_ball_data = {};
    let count = {};
    let x_axis = [];
    let chart_data = [];
    let myData = [];
    let myFavs = {};
    let lottery_id = 0;
    let lottery_game = "";
    let jackpot = "";
    let dataArray = [];
    let lottery_map = {};
    let lottery_details = {};
    let generatedPicks = [];
    let currentWheelTab = "WheelStep1";
    let currentWheelButton = "tabButton1";
    let userid = 1;
    let countdownInfo = null;
    let next_interval = null;

    // TODO: need to load this from the document cookie for current lottery OR top of the list as a fallback
    $('#graphType').on('change', function () {
        console.log("In update chart type");
        change_graph();
    });
    $('#displayType').on('change', function () {
        console.log("In update display type");
        change_graph();
    });
    $('#ballType').on('change', function () {
        console.log("In update ball type");
        change_graph();
    });
    $('#myRange').on('change', function () {
        console.log("In update chart range");
        document.getElementById("rangeValue").innerText = "Draws: " + $('#myRange').val();
        start_calculation();
    });
    $('#lottoSelect').on('change', function () {
        var x = document.getElementById("lottoSelect").value;
        updateCookieData("currentlottery", x);
        target_lottery_id = x;
//        alert("NEW KEY: " + x);
        getLotteryMetadata();
        refreshLastestResults();
        call_for_data(x);
        // setJackpotDisplay();
        // setCountdownDisplay();
    });


    $('#run_default_generation').on('click', function () {
        var x = document.getElementById("lottoSelect").value;
        call_for_default_pics(x);
        setGeneratedPicks();
    });

    
    $('#generation_results_deselect').on('click', function () {
        var inputs = document.forms["genResultsForm"].getElementsByTagName("input");
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].checked = false;
        }
    });

    
    $('#generation_results_select').on('click', function () {
        var inputs = document.forms["genResultsForm"].getElementsByTagName("input");
        for (let i = 0; i < inputs.length; i++) {
            inputs[i].checked = true;
        }
    });

    $('#generation_results_clear').on('click', function () {
        var form = document.getElementById("genResultsForm");
        var child = form.lastElementChild; 
        while (child) {
            form.removeChild(child);
            child = form.lastElementChild;
        }
    });

    $('#side_latest_results').on('click', function () {
        refreshSideBar("side_latest_results");
    });

    $('#side_check_tickets').on('click', function () {
        refreshSideBar("side_check_tickets");
    });

    $('#side_draw_history').on('click', function () {
        refreshSideBar("side_draw_history");
    });

    $('#side_charts_graphs').on('click', function () {
        refreshSideBar("side_charts_graphs");
    });

    $('#side_user_draw_history').on('click', function () {
        refreshSideBar("side_user_draw_history");
    });

    $('#generation_results_save').on('click', function () {
        let full_save_list = ""; 
        var inputs = document.forms["genResultsForm"].getElementsByTagName("input");
        for (let i = 0; i < inputs.length; i++) {
            if (inputs[i].checked) {
                
                full_save_list += generatedPicks[i].Balls;
                if (generatedPicks[i].hasOwnProperty("SpecialBalls")) {
                    full_save_list += ":::";
                    full_save_list += generatedPicks[i].SpecialBalls;
                }
                full_save_list += "\n";    
            }
        }
        alert("Saving the following\n" + full_save_list);
    });

//     $('#tabButton1').on('click', function () {
// //        openCity("tabButton1", 'WheelStep1');
//     });

//     $('#tabButton2').on('click', function () {
// //        openCity("tabButton2", 'WheelStep2');
//     });

//     $('#tabButton3').on('click', function () {
// //        openCity("tabButton3", 'WheelStep3');
//     });

//     $('#tabButton4').on('click', function () {
//   //      openCity("tabButton4", 'WheelStep4');
//     });

    $('#wheel_next_button_1').on('click', function () {
        openCity("tabButton2", 'WheelStep2');
//        document.getElementById("tabButton1").click();
        });

    $('#wheel_next_button_2').on('click', function () {
        openCity("tabButton3", 'WheelStep3');
//        document.getElementById("tabButton1").click();
        });

    $('#wheel_back_button_2').on('click', function () {
        openCity("tabButton1", 'WheelStep1');
//        document.getElementById("tabButton1").click();
        });

    $('#wheel_next_button_3').on('click', function () {
        openCity("tabButton4", 'WheelStep4');
//        document.getElementById("tabButton1").click();
        });

    $('#wheel_back_button_3').on('click', function () {
        openCity("tabButton2", 'WheelStep2');
//        document.getElementById("tabButton1").click();
        });
    
    $('#wheel_back_button_4').on('click', function () {
        openCity("tabButton3", 'WheelStep3');
//        document.getElementById("tabButton1").click();
        });

    function getCookieData(key) {
        if (document.cookie.length == 0) {
          return "";
        }
        data = JSON.parse(document.cookie);
        if (key in data) {
          return data[key];
        }
        return "";
      }

    function updateCookieData(key, value) {
      if (document.cookie.length == 0) {
        data = {};
      } else {
        data = JSON.parse(document.cookie);
      }
      data[key] = value;
      document.cookie = JSON.stringify(data);
    }
    
    // openCity(null, "WheelStep1A");
//     document.getElementById("WheelStep1").style.display = "block";
    function openCity(newButton, newTab) {
        // alert(currentWheelTab + ":" + currentWheelButton);
        // alert(newTab + ":" + newButton);
        document.getElementById(currentWheelTab).style.display = "none";
        document.getElementById(newTab).style.display = "block";
        document.getElementById(currentWheelButton).className = document.getElementById(currentWheelButton).className.replace(" active", "");
        document.getElementById(newButton).className += " active";
        currentWheelTab = newTab;
        currentWheelButton = newButton;

    //     // alert("tab advance");
    //     // alert(cityName);
    //  //   alert(cityName);
    //   var i, tabcontent, tablinks;
    //   tabcontent = document.getElementsByClassName("tabcontent");
    //   for (i = 0; i < tabcontent.length; i++) {
    //     tabcontent[i].style.display = "none";
    //   }
    //   tablinks = document.getElementsByClassName("tablinks");
    //   for (i = 0; i < tablinks.length; i++) {
    //     tablinks[i].className = tablinks[i].className.replace(" active", "");
    //   }
    //   document.getElementById(cityName).style.display = "block";
    //   document.getElementById(tabButton).className += " active";
    }
    
    userid = getCookieData('userid');
    console.log(">>>" + userid + "<<<");
    if (userid == '') {
      userid = 1;
      updateCookieData('userid', 1);
    }

    //call_for_data(userid);

    //openCity(currentWheelButton, currentWheelTab);
    call_for_favorites(userid);
    refreshSideBar("side_draw_history");
    
    function buildColumnShell() {
        row_object_outer = document.createElement("div");      
        row_object_outer.className = "col-12 col-md-6 col-xl-3";
        row_object_inner = document.createElement("div");      
        row_object_inner.className = "p-3 stats_inner d-flex align-items-center";
        row_object_outer.appendChild(row_object_inner);
        return row_object_outer;
    }

    function buildImage(src) {
        img_object = document.createElement("img");
        img_object.className = "img-fluid me-4";
        img_object.alt = "balance";
        img_object.src = src;
        return img_object;
    }

    function buildH5(text) {
        h5 = document.createElement("h5");
        h5.className = "text-warning mb-0";
        h5.innerText = text;
        return h5;
    }

    function buildSpan(text) {
        span = document.createElement("span");
        span.className = "mb-0 text_lgray text-capitalize";
        span.innerText = text;
        return span;
    }

/*
              <div class="amount_text">
                <h5 class="text-warning mb-0">Powerball</h5>
                <span class="mb-0 text_lgray text-capitalize">Multistate, USA</span>
*/
    function buildFavoritesDisplayLotteryNameColumn(rowData) {
        div_object = buildColumnShell();
        div_object.appendChild(buildImage("assets/images/how-it-works02.png"));
        inner_div = document.createElement("div");
        inner_div.className = "amount_text";
        country = rowData.Country;
        state = rowData.State;
        detailsText = "TEMP";
        if (state == null) {
            if (country == "USA") {
                detailsText = "Multistate, USA"
            } else {
                detailsText = country
            }
        } else {
            detailsText = state + ", " + country 
        }
        inner_div.appendChild(buildH5(rowData.Game));
        inner_div.appendChild(buildSpan(detailsText));
        div_object.appendChild(inner_div);
        return div_object;
    }

    function buildFavoritesDisplayLatestDrawColumn(rowData) {
        div_object = buildColumnShell();
        div_object.appendChild(buildImage("assets/images/bonus-promo.png"));
        inner_div = document.createElement("div");
        inner_div.className = "amount_text";
        inner_div.appendChild(buildSpan(rowData.DrawDate));
        ball_div = document.createElement("div");
        //build_ball_display(balls, special_balls, null);
    }

    function buildFavoritesDisplayCountdownColumn(rowData) {
        div_object = buildColumnShell();
        div_object.appendChild(buildImage("assets/images/bonus-promo.png"));

    }

    function buildFavoritesDisplayJackpotColumn(rowData) {
        div_object = buildColumnShell();
        div_object.appendChild(buildImage("assets/images/unbeat.png"));

    }

    function buildFavoritesDisplayRow(rowData) {
        row_object = document.createElement("div");
        row_object.className = "row";
        row_object.appendChild(buildFavoritesDisplayLotteryNameColumn(rowData));
        row_object.appendChild(buildFavoritesDisplayLatestDrawColumn(rowData));
        row_object.appendChild(buildFavoritesDisplayCountdownColumn(rowData));
        if (rowData.TrackJackpot) {
            row_object.appendChild(buildFavoritesDisplayJackpotColumn(rowData));
        }
    }

    function buildFavoritesDisplay() {
        outer_div = document.getElementById("favorites-display");
        for (const [key, value] of Object.entries(myFavs)) {
            rowOutput = buildFavoritesDisplayRow(value);
            outer_div.appendChild(rowOutput);
        }
    }

    function refreshSideBar(activate_item) {
        var list_items = document.getElementById("generation_ticket_count").getElementsByTagName("li");
        for (let i = 0; i < list_items.length; i++) {
            list_items[i].setAttribute("class", "one");
        }
        var target_item = document.getElementById(activate_item);
        target_item.setAttribute("class", "active_side");
    }

    function setGeneratedPicks() {
        var form = document.getElementById("genResultsForm");
        var child = form.lastElementChild; 
        while (child) {
            form.removeChild(child);
            child = form.lastElementChild;
        }
        len = Object.keys(generatedPicks).length;
        for (var i = 0; i < len; i++) {
            balls = generatedPicks[i].Balls;
            special_balls = generatedPicks[i].SpecialBalls;
//            alert(generatedPicks[0].Balls);
            current_name = "pick" + i;
            outer_div = document.createElement("div"); 
            outer_div.setAttribute("class", "generated_row");
            left_div = document.createElement("div");
          //  left_div.style.width = "10%";
            left_div.setAttribute("class", "generated_column_left");
            right_div = document.createElement("div");
          //  right_div.style.width = "90%"; 
            right_div.setAttribute("class", "generated_column_right");
            new_input = document.createElement("input");
            new_input.setAttribute("type", "checkbox");
            new_input.setAttribute("name", current_name);
            new_input.setAttribute("id", current_name);
            new_input.setAttribute("value", "TODO");
//            new_input.innerHTML = build_ball_display(balls, special_balls, null);
//            new_input.innerHTML = '<h4 class="text-white">' + generatedPicks[i].Balls + '</h4>';
//            form.appendChild(new_input);
            new_div = document.createElement("div");
    //        new_div.innerHTML = build_ball_display(balls, special_balls, null); 
            left_div.appendChild(new_input);
            inside_right_div = document.createElement("div");
            inside_right_div.setAttribute("class", "generated_row");
            inside_right_div.innerHTML = build_ball_display(balls, special_balls, null);
            right_div.appendChild(inside_right_div);
            outer_div.appendChild(left_div);
            outer_div.appendChild(right_div);
//            outer_div.innerHTML = build_ball_display(balls, special_balls, null); 
//            outer_div.appendChild(new_div);
            form.appendChild(outer_div);
//            form.appendChild(new_div);
            form.appendChild(document.createElement("br"));       
        }
    }

//http://localhost/bullseye-php-website/Bullseye-Picks.php

    function call_for_default_pics(lottery_id) {
//        console.log("Calling data with: " + lottery_id);
        var gen_count = document.getElementById("generation_ticket_count").value;
//        console.log("Calling defgen for pic count: " + gen_count);
        $.ajax({
            url: "api_call.php",
            type: "POST",
            data: {lottery_id: lottery_id, draw_count: gen_count, call: 'defgen'},
            beforeSend: function(){
                $('#loading').slideDown();
            },
            success: function(output){
                if(output){
               //     alert(output);
//                    generatedPicks = output;
                    generatedPicks = JSON.parse(output);
                    setGeneratedPicks();
  //                  len = Object.keys(generatedPicks).length;
    //                alert(len);
                    // myData = JSON.parse(output);
                    // len = Object.keys(myData).length;
                    // if(len){
                    //     $('#loading').slideUp();
                    //     $('#err_loading').slideUp();
                    //     jackpot = myData["Jackpot"];
                    //     dataArray = myData["Data"];
                    //     setJackpotDisplay();
                    //     setCountdownDisplay();
                    //     document.getElementById("last_draw_text").innerHTML = build_first_ball_display(dataArray[0]);
                    //     document.getElementById("last_draw_date").innerText = "LAST DRAW " + dataArray[0].Date;
                    //     start_calculation();
                    //     populate_table();
                    // } else {
                    //     alert("FAIL DATA");
                    //     $('#loading').slideUp();
                    //     $('#err_loading').slideDown();
                    // }
                }
            }
        });    
    }



    function call_for_data(lottery_id) {
        console.log("Calling data with: " + lottery_id);
        $.ajax({
            url: "api_call.php",
            type: "POST",
            data: {lottery_id: lottery_id, call: 'history'},
            beforeSend: function(){
                $('#loading').slideDown();
            },
            success: function(output){
                if(output){
//                    console.log(output);
//                    alert(output);
                    myData = JSON.parse(output);
                    console.log(myData);
                    dataArray = myData["history"];
                    len = Object.keys(myData).length;
                    if(len){
                        $('#loading').slideUp();
                        $('#err_loading').slideUp();
                        setJackpotDisplay();
                        setCountdownDisplay();
                        start_calculation();
                        populate_table();
                    } else {
                        alert("FAIL DATA");
                        $('#loading').slideUp();
                        $('#err_loading').slideDown();
                    }
                }
            }
        });    
    }

    function getLotteryMetadata() {
  //      console.log("UPDATE METADATA FOR LOTTERY KEY: " + target_lottery_id);
        for (const [key, value] of Object.entries(myFavs)) {
            if (value.Id == target_lottery_id) {
                lottery_details = value;
                return true;
            }
        }
        return false;
    }

    String.prototype.replaceAt = function(index, replacement) {
        return this.substring(0, index) + replacement + this.substring(index + replacement.length);
    }

    function buildDrawDaysString(input_string, output_string) {
        console.log(input_string);
        result = output_string;
        input_string.split('').forEach(element => {
            console.log(element);
            switch(element) {
                case 'D':
                    console.log("IN CASE D");
                    result = "1111111";
                    break;
                case 'M':
                    console.log("IN CASE M");
                    result = result.replaceAt(0,"1");
                    break;
                case 'T':
                    console.log("IN CASE T");
                    result = result.replaceAt(1,"1");
                    break;
                case 'W':
                    console.log("IN CASE W");
                    result = result.replaceAt(2,"1");
                    break;
                case 'R':
                    console.log("IN CASE R");
                    result = result.replaceAt(3,"1");
                    break;
                case 'F':
                    console.log("IN CASE F");
                    result = result.replaceAt(4,"1");
                    break;
                case 'S':
                    console.log("IN CASE S");
                    result = result.replaceAt(5,"1");
                    break;
                case 'U':
                    console.log("IN CASE U");
                    result = result.replaceAt(6,"1");
                    break;
                default:
                    console.log("FAILURE");
                    break;
                }
                console.log(result);
        });
        return result;
    }

    Date.prototype.addDays = function(days) {
        var date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date;
    }

    function setCountdownDisplay() {
        console.log("UPDATE COUNTDOWN DISPLAY");
//         // need last date w/ data
//         last_draw_date = getLastDate();
//         console.log("LAST DRAW");
//         console.log(last_draw_date);
// //        next_draw_date = getFutureDate(last_draw_date);
//         console.log("NEXT DRAW");
//         console.log(next_draw_date);
        // get draw times
        // find next
        // if next in past (poll for new results, mark as pending(balls and jackpot), find next,next)
        // compute time delta (adjust for timezone issues)
        // pass to countdown display thingy
        if (next_interval != null) {
            clearInterval(next_interval);
        }
        countdown_object = document.getElementById("draw_countdown"); //buildColumnShell();
        countDownDate = Date.parse(lottery_details.NextDateTime);
      //  countdownInfo = countDownDate;
        fillCountdown(countDownDate, "draw_countdown");
        next_interval = setInterval(function() {
            fillCountdown(countDownDate, "draw_countdown");
            // var now = new Date().getTime(); 
            
            // var tzDifference = new Date(now).getTimezoneOffset();
            // var correctedTime = new Date(countDownDate - tzDifference * 60000);
            // var distance = correctedTime - now;
            // var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            // var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            // var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            // var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            // if (distance < 0)  {
            //     document.getElementById("draw_countdown").innerHTML = "WAITING FOR LATEST RESULTS";                            
            // } else {
            //     document.getElementById("draw_countdown").innerHTML = days + " days " + hours + " hours\n"
            //     + minutes + " mins " + seconds + " secs";    
            // }
        }, 1000);
        
        //      div_object.appendChild(buildImage("assets/images/bonus-promo.png"));
            //  alert(datetime_object);
            //   inner_div = document.createElement("div");
            //   div_id = "timerID_" + lottery_index.toString();
            //   inner_div.id = div_id;
            //   div_object.appendChild(inner_div);
            //   countDownDate = Date.parse(rowData.NextDateTime);
            //   console.log("0:" + countDownDate);
            //   countdownInfo = {'div_name': div_id, 'date': countDownDate}
            //   next_draw_info.push(countdownInfo);
      //        var countDownDate = Date.parse(rowData.NextDateTime); 
      //        inner_div.innerText = rowData.NextDateTime;
            //   div_object.appendChild(inner_div);
            //   return div_object;
    }

    function fillCountdown(date, id) {
        var now = new Date().getTime(); 
            
        var tzDifference = new Date(now).getTimezoneOffset();
        var correctedTime = new Date(date - tzDifference * 60000);
        var distance = correctedTime - now;
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        if (distance < 0)  {
            document.getElementById(id).innerHTML = "WAITING FOR LATEST RESULTS";                            
        } else {
            document.getElementById(id).innerHTML = days + " days " + hours + " hours\n"
            + minutes + " mins " + seconds + " secs";    
        }
    }

    function setJackpotDisplay() {
        if (lottery_details.hasOwnProperty("TrackJackpot") && lottery_details["TrackJackpot"] == true) {
            document.getElementById("jackpot_text").innerText = lottery_details["Jackpot"];
            document.getElementById("jackpot_div").style.display = "block";
        } else {
            document.getElementById("jackpot_div").style.display = "none";
        }
    }

    function call_for_favorites(user_id) {
        console.log("Call for favorites");
        $.ajax({
            url: "api_call.php",
            type: "POST",
            data: {user_id: user_id, call: 'favoriteDetails'},
            beforeSend: function(){
                $('#loading').slideDown();
            },
            success: function(output){
                if(output){
                    console.log(output);
                    myData = JSON.parse(output);
                    len = Object.keys(myData).length;
                    if(len){
                        $('#loading').slideUp();
                        $('#err_loading').slideUp();
                        myFavs = myData["favorites"];
                        target_lottery_id = getCookieData("currentlottery");

                        found = getLotteryMetadata();

                        if (found == false || target_lottery_id == "") {
                            target_lottery_id = myFavs[0].Id;
                            lottery_details = myFavs[0];
                            updateCookieData("currentlottery", target_lottery_id);
                        }
                        index = 0;
                        selectElement = document.getElementById("lottoSelect");
                        for (const [key, value] of Object.entries(myFavs)) {
                            var opt = document.createElement("option");
                            opt.value= index;
                            opt.classList = "text-white mt-2 mb-4 text-capitalize";
                            console.log(value);
                            if (value.State == null) {
                                opt.innerHTML = value.Game + " (" + value.Country + ")"; // whatever property it has
                            } else {
                                opt.innerHTML = value.Game + " (" + value.State + ", " + value.Country + ")"; // whatever property it has
                            }
                            opt.value = value.Id;
                            selectElement.appendChild(opt);
                            index++;
                        }
                        selectElement.value = target_lottery_id;
                        lottery_id = target_lottery_id;
                        refreshLastestResults();
                        // document.getElementById("last_draw_text").innerHTML = build_first_ball_display(lottery_details);
                        // document.getElementById("last_draw_date").innerText = "LAST DXRAW " + lottery_details.DrawDate;

                        call_for_data(target_lottery_id);
                    } else {
                        alert("FAIL FAV");
                        $('#loading').slideUp();
                        $('#err_loading').slideDown();
                    }
                }
            }
        });     
    }

    function refreshLastestResults() {
        htmlText = "";
        div_object = document.createElement("div");
        //    div_object.appendChild(buildImage("assets/images/bonus-promo.png"));
        // inner_div = document.createElement("div");
        // inner_div.className = "amount_text row";
        // div_object.appendChild(inner_div);
 //       ball_div = document.createElement("div");
        htmlText += build_first_ball_display(lottery_details);
//        ball_div.innerHTML = build_first_ball_display(lottery_details);
    //    div_object.appendChild(ball_div);
        if (lottery_details.SecondDrawBalls.length > 0) {
            htmlText += '<span class="amount_text row">' + lottery_details.SecondDrawName + '</span>'
            htmlText += build_second_ball_display(lottery_details);
            // inner_div = document.createElement("div");
            // inner_div.className = "amount_text row";
            // inner_div.appendChild(buildSpan(lottery_details.SecondDrawName));
            // div_object.appendChild(inner_div);
            // ball_div = document.createElement("div");
            // ball_div.innerHTML = build_second_ball_display(lottery_details);
            // div_object.appendChild(ball_div);    
        }
        if (lottery_details.ThirdDrawBalls.length > 0) { 
            htmlText += '<span class="amount_text row">' + lottery_details.ThirdDrawName + '</span>'
            htmlText += build_third_ball_display(lottery_details);
            // inner_div = document.createElement("div");
            // inner_div.className = "amount_text row";
            // inner_div.appendChild(buildSpan(lottery_details.ThirdDrawName));
            // div_object.appendChild(inner_div);
            // ball_div = document.createElement("div");
            // ball_div.innerHTML = build_third_ball_display(lottery_details);
            // div_object.appendChild(ball_div);
        }
        document.getElementById("last_draw_text").innerHTML =htmlText;// div_object;//build_first_ball_display(lottery_details);
        document.getElementById("last_draw_date").innerText = "LAST DRAW " + lottery_details.DrawDate;
    }

    function build_ball_display(balls, special_balls, multiplier) {
        let outputHTML = "";

        balls.forEach(function (item, index) {
            if (lottery_details.BallColor == undefined) {
                outputHTML += '<span class="balls">' + item + '</span>';
            } else if (lottery_details.BallColor == "Red") {
                outputHTML += '<span class="balls redballs">' + item + '</span>';
            }
        });
        if (special_balls != null) {
            special_balls.forEach(function (item, index) {
                if (lottery_details.SpecialBallColor == undefined) {
                    outputHTML += '<span class="balls sballs">' + item + '</span>';
                } else if (lottery_details.SpecialBallColor == "White") {
                    outputHTML += '<span class="balls sballs whiteballs">' + item + '</span>';
                }
            });
        }
        if (multiplier != null) {
            outputHTML += '<span class="multiplier"> ' + multiplier.trim() + '</span>';
        }
        return outputHTML;
    }

    // function build_ball_display(balls, speical_balls, multiplier) {
    //     let outputHTML = ""
    //     balls_list = data.Balls.split(",");
    //     balls_list.forEach(function (item, index) {
    //         outputHTML += '<span class="balls">' + item + '</span>';
    //     });
    //     if (data.SpecialBalls.length > 0) {
    //         sballs_list = data.SpecialBalls.split(",");
    //         sballs_list.forEach(function (item, index) {
    //             outputHTML += '<span class="balls sballs">' + item + '</span>';
    //         });
    //     }
    //     if (data.Multiplier.trim().length > 0) {
    //         outputHTML += '<span class="multiplier"> ' + data.Multiplier.trim() + '</span>';
    //     }
    //     return outputHTML;
    // }

    function build_first_ball_display(data) {
        balls = data.Balls.split(",");
        sballs = null;
        if (data.SpecialBalls.length > 0) {
            sballs = data.SpecialBalls.split(",");
        }
        multiplier = null;
        if (data.Multiplier.trim().length > 0) {
            multiplier = data.Multiplier.trim();
        }
        return build_ball_display(balls, sballs, multiplier);
    }

    function build_second_ball_display(data) {
        balls = data.SecondDrawBalls.split(",");
        sballs_list = null;
        if (data.SecondDrawSpecialBalls.length > 0) {
            sballs_list = data.SecondDrawSpecialBalls.split(",");
        }
        multiplier = null;
        // if (data.Multiplier.trim().length > 0) {
        //     multiplier = data.Multiplier.trim();
        // }
        return build_ball_display(balls, sballs_list, multiplier);
    }

    function build_third_ball_display(data) {
        balls = data.ThirdDrawBalls.split(",");
        sballs_list = null;
        // if (data.SpecialBalls.length > 0) {
        //     sballs_list = data.SpecialBalls.split(",");
        // }
        multiplier = null;
        // if (data.Multiplier.trim().length > 0) {
        //     multiplier = data.Multiplier.trim();
        // }
        return build_ball_display(balls, sballs_list, multiplier);
    }

    function populate_table() {
        var table = document.getElementById("data_table");
        if (table == null) {
            return;
        }
        //draw_data = dataArray.slice(Math.max(0, draw));
        target_lottery_id = getCookieData("currentlottery");
//        target_lottery_id = getCookie("favorite");
        //$("#data_table tr").remove();
//        $("#table_of_items tr").remove();
       // alert(table.rows.length);
        while (table.rows.length > 1) {
            table.deleteRow(1);
        }
        for (i = 1; i <= 20; i++) {
            var row = table.insertRow(i);
            // row.insertCell(0).innerHTML = target_lottery_id;
            // row.insertCell(1).innerHTML = lottery_details.Game;
            row.insertCell(0).innerHTML = dataArray[i - 1].Date;
            // let ball_data = dataArray[i - 1].Balls;
            // if (lottery_details.NumberOfSpecialBalls != 0) {
            //     ball_data = ball_data + dataArray[i - 1].SpecialBalls;
            //     ballName = lottery_details.BallName || "Balls";
            //     speicalName = lottery_details.SpecialBallName || "Special Ball";
            //     document.getElementById("ball1_text").innerText = ballName + " and " + speicalName;
            // } else {
            //     document.getElementById("ball1_text").innerText = "Balls";
            // }
            // multiplier = dataArray[i - 1].Multiplier  || "";
            // multiplier = multiplier.trim();
            // if (multiplier.length > 0) {
            //     ball_data = ball_data + multiplier;
            // }
            var ball_data = build_first_ball_display(dataArray[i - 1]);
            row.insertCell(1).innerHTML = ball_data;            
            if (lottery_details.HasSecondDraw) {
                var ball_data = build_second_ball_display(dataArray[i - 1]);
                row.insertCell(2).innerHTML = ball_data;           
                document.getElementById("ball2_text").innerText = lottery_details.SecondDrawName;
            }
            else 
            {
                document.getElementById("ball2_text").innerText = "";
            }
            if (lottery_details.HasThirdDraw) {
                var ball_data = build_third_ball_display(dataArray[i - 1]);
                row.insertCell(3).innerHTML = ball_data;           
                document.getElementById("ball3_text").innerText = lottery_details.ThirdDrawName;
            }
            else 
            {
                document.getElementById("ball3_text").innerText = "";
            }
            // var ball_data = build_second_ball_display(dataArray[i - 1]);
            // row.insertCell(2).innerHTML = ball_data;            
            // if (lottery_details.HasSecondDraw) {
            //     let ball_data = dataArray[i - 1].SecondDrawBalls;
            //     if (lottery_details.NumberOfSpecialBalls != 0) {
            //         ball_data = ball_data + dataArray[i - 1].SecondDrawSpecialBalls;
            //         ballName = lottery_details.BallName || "Balls";
            //         speicalName = lottery_details.SpecialBallName || "Special Ball";
            //         document.getElementById("ball2_text").innerText = "Second Draw";
            //     } else {
            //         document.getElementById("ball2_text").innerText = "Second Draw";
            //     }    
            //     row.insertCell(2).innerHTML = ball_data;
            // } else {
            //     document.getElementById("ball2_text").innerText = "";
            // }
            // if (lottery_details.HasThirdDraw) {
            //     let ball_data = dataArray[i - 1].ThirdDrawBalls;
            //     document.getElementById("ball3_text").innerText = "Third Draw";
            //     row.insertCell(3).innerHTML = ball_data;
            // } else {
            //     document.getElementById("ball3_text").innerText = "";
            // }
        }
    }

    function start_calculation() {
        var table = document.getElementById("data_table");
        if (table != null) {
            return;
        }
        console.log("Call start calculation");
        draw = Number($('#myRange').val());
        draw_data = dataArray.slice(0, draw);
        console.log(draw);
        console.log(draw_data.length);
        build_graph_data();
        change_graph();
    }

    function change_graph() {
        g_type = $('#graphType').val();
        // draw = Number($('#myRange').val());
//        draw_data = dataArray.slice(Math.max(0, draw));
        if(g_type == "ballFreq") {
            graph_ball_frequency(false);
        } else if(g_type == "ballSumSymbols"){
            graph_ball_frequency(true);
        } else if(g_type == "ballSum"){
            graph_ball_sum();
        } else if(g_type == "pairs"){
            graph_ball_pairs();
        } else if(g_type == "triplets"){
            graph_ball_triplets();
        } else if(g_type == "ballInDraw"){
            graph_ball_in_draw();
        } else if(g_type == "oddEven"){
            graph_ball_odd_even();
        } else if(g_type == "summary"){
            graph_ball_summary();
        } else if(g_type == "deltas"){
            graph_ball_deltas();
        }
    }

    function build_graph_data() {
        graph_ball_data = {};

        // BALL FREQUENCY

        count = {};
        data_set = {};
        x_axis = [];
        chart_data = [];
        ball = [];
        balls = [];

        Object.keys(draw_data).forEach((key) => {
            let nData = draw_data[key]["Balls"].split(',');
            nData.forEach((k)=>{
                balls.push(Number(k));
            });
        });
        balls.forEach(function(i) { count[i] = (count[i]||0) + 1;});
        Object.keys(count).forEach((key) => {
            x_axis.push(key);
            chart_data.push(count[key]);
        });

        data_set['x_axis'] = x_axis;
        data_set['chart_data'] = chart_data;
        graph_ball_data['ball_frequency'] = data_set;

        // BALL SUM

        count = {};
        data_set = {};
        x_axis = [];
        chart_data = [];
        sum = [];

        // Object.keys(draw_data).forEach((key) => {
        //     let nData = draw_data[key]["Balls"].split(',');
        //     sum = nData.reduce(add, 0);
        // });
        // balls.forEach(function(i) { count[i] = (count[i]||0) + 1;});
        // Object.keys(count).forEach((key) => {
        //     x_axis.push(key);
        //     chart_data.push(count[key]);
        // });

        data_set['x_axis'] = x_axis;
        data_set['chart_data'] = chart_data;
        graph_ball_data['ball_sum'] = data_set;

    }

    // 'column'
    // 'BALL FREQUENCY A'
    // 'Number of times each ball number has appeared in the '+draw+' draws'
    //
    // Times
    // '<span style="font-size:10px">{point.key}</span><table>'
    // '<tr><td style="color:{series.color};padding:0">{series.name}: </td><td style="padding:0"><b>{point.y:.0f} times</b></td></tr>'
    // '</table>'
    // 'Ball'
    function update_chart(title, sub_title, x_axis, y_axis_text, header_format, point_format, footer_format, chart_series) {
        //series_name_array, chart_data_array, chart_color_array
    //     series: [{
    //         name: series_name,
    //         data: chart_data,
    //         color: "#37adb1"
    //     }]
      Highcharts.chart('container', {
            chart: {
                type: $('#displayType').val(),
                backgroundColor: "#0d1e25"
            },
            title: {
                text: title
            },
            subtitle: {
                text: sub_title
            },
            xAxis: {
                categories: x_axis,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: y_axis_text
                }
            },
            tooltip: {
                headerFormat: header_format,
                pointFormat: point_format,
                footerFormat: footer_format,
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: chart_series
        });
    }

    function graph_ball_frequency(use_symbols) {
//         count = {};
//         x_axis = [];
//         chart_data = [];

//         Object.keys(draw_data).forEach((key) => {
//             let nData = draw_data[key]["Balls"].split(',');
//             nData.forEach((k)=>{
//                 balls.push(Number(k));
//             });
//         });
// //        balls = balls.sort();
//         balls.forEach(function(i) { count[i] = (count[i]||0) + 1;});

//         Object.keys(count).forEach((key) => {
//             x_axis.push(key);
//             chart_data.push(count[key]);
//         });

        display_type = $('#displayType').val();

        Highcharts.chart('container', {
            chart: {
                type: display_type,
                backgroundColor: "#0d1e25"
            },
            title: {
                text: 'BALL FREQUENCY'
            },
            subtitle: {
                text: 'Number of times each ball number has appeared in the '+draw+' draws'
            },
            xAxis: {
                categories: graph_ball_data['ball_frequency']['x_axis'],
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Times'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.0f} times</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: 'Ball',
                data: graph_ball_data['ball_frequency']['chart_data']
            }]
        });
     }

    function graph_ball_sum() {
        count = {};
        x_axis = [];
        let chart_data1 = [];
        let chart_data2 = [];
        let total = 0;
        let et = 0, t = 0;

        Object.keys(draw_data).forEach((key) => {
            let nData = draw_data[key].split(',');
            et = 0;
            nData.forEach((k)=>{
                et = et + Number(k);
            });

            chart_data1.push(et);
            total = total + et;
            t++;
        });
        let avg = total/t;

        for(i=0;i<draw;i++){
            chart_data2.push(Number(avg.toFixed(2)));
            x_axis.push(i+1);
        }

        Highcharts.chart('container', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'BALL SUM'
            },
            subtitle: {
                text: 'Sum of all the balls in each draw'
            },
            xAxis: {
                categories: x_axis,
                title: {
                    enabled: true,
                    text: 'Number of Draws'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Sum'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">Draw: {point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: 'Sum',
                data: chart_data1
            },{
                name: 'Average',
                data: chart_data2
            }]
        });


    }
    function graph_ball_pairs() {
        count = {};
        x_axis = [];
        let pairs = [];
        let chart_data1 = [];
        let total = 0;
        let et = 0, t = 0;

        Object.keys(draw_data).forEach((key) => {
            let nData = draw_data[key].split(',');
            for(i=0;i<nData.length;i++){
                let x = Number(nData[i])+1;
                let y  = (i != (nData.length - 1)) ? nData[i+1] : nData[i];
                if(x == y){
                    pairs.push(nData[i]+"-"+y);
                }
            }
        });
        pairs.forEach(function(i) { count[i] = (count[i]||0) + 1;});

        Object.keys(count).forEach((key)=>{
            chart_data1.push(count[key]);
            x_axis.push(key.replace('-',','));
        });

        Highcharts.chart('container', {
            chart: {
                type: 'column'
            },
            title: {
                text: 'NUMBER PAIRS'
            },
            subtitle: {
                text: 'Number of times in a draw that there are two numbers in a row'
            },
            xAxis: {
                categories: x_axis
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Times'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">Pair: {point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.0f} times</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: 'Pair',
                data: chart_data1
            }]
        });
    }
});
