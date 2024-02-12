// var currentUrl = window.location.href;
// if (currentUrl.endsWith("/#")) {
//     currentUrl = currentUrl.slice(0,-2)
// }
// if (currentUrl.endsWith("/")) {
//     currentUrl = currentUrl.slice(0,-1)
// }
// parts = currentUrl.split("/")
// pageName = parts[parts.length-1]
//
// if (pageName == "favorites") {
//     title = document.getElementById("headerText")
//     title.innerText = "Favorites"
//     drop_down = document.getElementById("lottoSelectDiv")
//     drop_down.style.display = "none"
// }
// HANDLE DATA HERE!!!!

$('#lotterySelect').on('change', function () {
    // console.log("CALLED select");
    // var x = document.getElementById("lotterySelect").value;
    // console.log(x);
    // updateCookieData("currentlottery", x);
    // target_lottery_id = x;
    // getLotteryMetadata();
    // setJackpotDisplay();
    // setCountdownDisplay();
    // refreshLastestResults();
    // call_for_lottery_history(lottery_select_post_call, null);
});

function getCookieData(key) {
    if (document.cookie.length == 0) {
      return "";
    }
    let data = JSON.parse(document.cookie);
    if (key in data) {
      return data[key];
    }
    return "";
 }

 function updateCookieData(key, value) {
    let data = {};
    if (document.cookie.length != 0) {
      data = JSON.parse(document.cookie);
    }
    data[key] = value;
    document.cookie = JSON.stringify(data);
  }

function common_init(side_bar_reference, show_lotto_select, is_picker_page) {
    refreshSideBar(side_bar_reference);
    // let selectElement = document.getElementById("lottoSelect");
    // if (show_lotto_select) {
    //     selectElement.style.display = "block";
    // } else {
    //     selectElement.style.display = "none";
    // }
}

function updateCookieData(key, value) {
    let data = {};
    if (document.cookie.length != 0) {
      data = JSON.parse(document.cookie);
    }
    data[key] = value;
    document.cookie = JSON.stringify(data);
}

function refreshSideBar(activate_item) {
    var list_items = document.getElementById("sidebar").getElementsByTagName("li");
    for (let i = 0; i < list_items.length; i++) {
        list_items[i].setAttribute("class", "one");
    }
    var target_item = document.getElementById(activate_item);
    target_item.setAttribute("class", "active_side");
}

let next_interval = null;
function setCountdownDisplay(nextTime) {
    if (next_interval != null) {
        clearInterval(next_interval);
    }
    fillCountdown(nextTime, "draw_countdown", new Date().getTime());
    next_interval = setInterval(function() {
        fillCountdown(nextTime, "draw_countdown", new Date().getTime());
    }, 1000);
}

function setFavoriteTimers(next_draw_info) {
        var now = new Date().getTime();
        for (let i = 0; i < next_draw_info.length; i++) {
            fillCountdown(next_draw_info[i]['date'], next_draw_info[i]['div_name'], now);
        }
        next_interval = setInterval(function() {
            var now = new Date().getTime();
            for (let i = 0; i < next_draw_info.length; i++) {
                fillCountdown(next_draw_info[i]['date'], next_draw_info[i]['div_name'], now);
            }
        }, 1000);
}

function fillCountdown(date, id, now) {
    // var tzDifference = new Date(now).getTimezoneOffset();
    // var correctedTime = new Date(date - tzDifference * 60000);
    // var distance = correctedTime - now;
    var distance = date - now;
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