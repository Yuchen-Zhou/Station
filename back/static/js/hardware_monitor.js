// 初始化 CPU 使用率图表
var url = document.getElementById("hardware_usage").getAttribute('data-url');
var cpuChart = echarts.init(document.getElementById('cpu_chart'));
var cpuOption = {
    title: {
        text: 'CPU使用率'
    },
    tooltip: {},
    xAxis: {
        data: []
    },
    yAxis: {},
    series: [{
        name: 'CPU Usage',
        type: 'line',
        data: []
    }]
};

// 初始化内存使用情况图表（饼图）
var memoryChart = echarts.init(document.getElementById('memory_chart'));
var memoryOption = {
    title: {
        text: '内存使用情况'
    },
    tooltip: {},
    series: [{
        name: 'Memory Usage',
        type: 'pie',
        radius: '55%',
        data: []
    }]
};

// 更新硬件资源使用情况
function updateHardwareUsage() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var data = JSON.parse(xhr.responseText);
            // 更新 CPU 使用率图表数据
            cpuOption.xAxis.data.push(new Date().toLocaleTimeString());
            cpuOption.series[0].data.push(data.cpu_percent);
            cpuChart.setOption(cpuOption);

            // 更新内存使用情况图表数据
            memoryOption.series[0].data = [
                {value: data.used_memory, name: '已使用的内存'},
                {value: data.free_memory, name: '空余内存'}
            ];
            memoryChart.setOption(memoryOption);
        }
    };
    xhr.open("GET", url, true);
    xhr.send();
}

setInterval(updateHardwareUsage, 1000);