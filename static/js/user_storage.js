$(document).ready(function() {
    // 使用 Ajax 请求获取用户存储信息
    $.ajax({
        url: document.getElementById("user_storage_chart").getAttribute("data-url"),  // 替换为获取用户存储信息的 URL
        type: "GET",
        dataType: "json",
        success: function(response) {
            // 成功接收到数据后，在此处处理数据
            var userStorageData = response;
            console.log(userStorageData);  // 在控制台打印数据进行检查

            // 绘制饼图
            var storageChart = echarts.init(document.getElementById('user_storage_chart'));
            var storageOption = {
                title: {
                    text: '用户存储空间使用情况',
                    subtext: '单位: GB',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} GB ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 10,
                    data: ['已使用', '未使用']
                },
                series: [
                    {
                        name: '存储空间使用情况',
                        type: 'pie',
                        radius: ['50%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '30',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: [
                            {value: userStorageData.used, name: '已使用'},
                            {value: userStorageData.unused, name: '未使用'}
                        ]
                    }
                ]
            };

            storageChart.setOption(storageOption);
        },
        error: function(xhr, errmsg, err) {
            console.log("Error occurred while fetching user storage info:", errmsg);
        }
    });
});
