$(document).ready(function () {
    // 使用Ajax请求获取用户活动信息
    $.ajax({
        url: document.getElementById('user_activity_chart').getAttribute('data-url'), // 替换为获取用户活动信息的URL
        type: "GET",
        dataType: "json",
        success: function (response) {
            var userActivityData = response;
            console.log(userActivityData);

            // 初始化 ECharts 实例
            var userChart = echarts.init(document.getElementById('user_activity_chart'));

            // 设置图表配置项和数据
            var userOption = {
                title: {
                    text: '用户活动情况'
                },
                xAxis: {
                    type: 'category',
                    data: ['登录次数', '海洋之眼使用次数', '大模型使用次数', '信息管理使用次数']
                },
                yAxis: {
                    type: 'value'
                },
                series: [{
                    data: [
                        userActivityData.login_count,
                        userActivityData.sea_eyes_count,
                        userActivityData.llms_count,
                        userActivityData.infoSys_count
                    ],
                    type: 'bar'
                }]
            };

            // 使用刚指定的配置项和数据显示图表
            userChart.setOption(userOption);
        },
        error: function (xhr, errmsg, err) {
            console.log("Error occurred while fetching user activity info:", errmsg);
        }
    });
});