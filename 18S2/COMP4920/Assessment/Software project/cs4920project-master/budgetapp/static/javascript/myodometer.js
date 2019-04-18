setTimeout(function(){
    odometer.innerHTML = 0;
    odometer1.innerHTML = 5555;
    odometer2.innerHTML = 432425;
    odometer3.innerHTML = 900000;
}, 1000);

var tmp1 = 0;
var tmp2 = parseInt(document.getElementById("myVar5").value);
var tmp3 = parseInt(document.getElementById("myVar6").value);
setInterval(function(){
	tmp1 += 5;
	tmp2 += 55;
	tmp3 -= 658
	odometer.innerHTML = tmp1;
	odometer1.innerHTML = tmp2;
	odometer2.innerHTML = Math.floor(Math.random() * 100000000);
	odometer3.innerHTML = tmp3;
}, 2000)