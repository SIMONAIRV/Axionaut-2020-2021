document.getElementById('start_stop_button').onclick = changeColor();   
var i=0
console.log(i)
function changeColor() {
    i=i+1;
    console.log(i)

    if(i%1==0){
        document.getElementById('start_stop_button').style.background = "red";
        document.getElementById('start_stop_button').innerHTML = "Stop";

    }
    else{
        document.getElementById('start_stop_button').style.background = "green";
        document.getElementById('start_stop_button').innerHTML = "Start";
    }
    return false;

}