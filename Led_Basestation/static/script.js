document.getElementById("sendCell").addEventListener("click",()=>{
    num = document.getElementById('cellNum').value;
    console.log(num);
    fetch('/setCell/'+num)
        .then(function (response){
            return response.json();
        }).then(function (text){
            console.log(text);
        });
})

document.getElementById("updateChart").addEventListener("click",()=>{
    startDateSecs = parseInt(Date.parse(dateStartInput.value+' '+timeStartInput.value)/1000)
    endDateSecs = parseInt(Date.parse(dateEndInput.value+' '+timeEndInput.value)/1000)

    getHistData(startDateSecs,endDateSecs).then(data=>{chartData = data; updateChart(myChart,chartData)})
});

dateStartInput = document.getElementById("dateStart")
dateEndInput = document.getElementById("dateEnd")
timeStartInput = document.getElementById("timeStart")
timeEndInput = document.getElementById("timeEnd")

curDate = new Date();
curDate6hago = new Date(Date.now()-60*60*6*1000);
dateStartInput.value = curDate6hago.toISOString().substring(0,10);
dateEndInput.value = curDate.toISOString().substring(0,10);
timeStartInput.value = curDate6hago.toTimeString().substring(0,5);
timeEndInput.value = curDate.toTimeString().substring(0,5);


function getHistData(dateBegin,dateEnd){
    return fetch('/getData/'+dateBegin+'&'+dateEnd)
        .then(function (response){
            return response.json();
        }).then(function (text){
            return text;
        });
}

function updateChart(chart, chartData){

    chart.data={
        labels:chartData['date'],
        datasets: [{
            label: 'Temperatura',
            data: chartData['temp'],
            borderWidth: 1,
            borderColor:'red'
        },
        {
            label: 'Wilgotność',
            data: chartData['hum'],
            borderWidth: 1,
            borderColor:'blue'
        }]
    };
    chart.options.ticks = {
        min: chartData['date'][0],
        max: chartData['date'][chartData['date'].length]
    }
    chart.update();
}
var chartData = 0;
var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels:chartData['date'],
        datasets: [{
            label: 'Temperatura',
            data: chartData['temp'],
            borderWidth: 1,
            borderColor:'red'
        },
        {
            label: 'Wilgotność',
            data: chartData['hum'],
            borderWidth: 1,
            borderColor:'blue'
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            },
            x: {
                type: 'time',
                time: {
                    unit: 'minute',
                    displayFormats:{
                        minute: 'DD-MM HH:mm'
                    }
                }
            }
        }
    }
});
curDateInSeconds = parseInt(Date.now()/1000);
getHistData(curDateInSeconds-60*60*6,curDateInSeconds).then(data=>{chartData = data; updateChart(myChart,chartData)})
