// 获取上传图片按钮和文件输入框
var uploadButton = document.getElementById("uploadButton");
var fileInput = document.getElementById("fileInput");
// 获取进度条元素
var progressBar = document.getElementById("progressBar");

// 点击上传图片按钮时触发的事件
uploadButton.addEventListener("click", function() {
    // 显示选择文件框
    fileInput.click();
});

// 当用户选择文件后触发的事件
fileInput.addEventListener("change", function() {
    // 获取用户选择的文件
    var files = fileInput.files;
    if (files.length > 0) {
        // 遍历文件列表，可以在这里处理每个文件的上传逻辑
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            console.log("已选择文件:", file.name);
            // 在这里可以处理上传文件的逻辑，例如将文件添加到队列中等待上传

            // 模拟上传进度（假设上传过程中每0.5秒增加1%）
            var progress = 0;
            var interval = setInterval(function() {
                progress++;
                progressBar.style.width = progress + "%"; // 更新进度条宽度
                if (progress >= 100) {
                    clearInterval(interval); // 上传完成后清除定时器
                }
            }, 500);
        }
    }
});
