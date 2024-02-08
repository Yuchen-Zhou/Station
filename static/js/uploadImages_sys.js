// 获取上传图片按钮和文件输入框
var uploadButton = document.getElementById("uploadButton");
var fileInput = document.getElementById("imageInput");
// 获取进度条元素
var progressBar = document.getElementById("progressBar");

// 点击上传图片按钮时触发的事件
uploadButton.addEventListener("click", function () {
    // 显示选择文件框
    fileInput.click();
});

// 当用户选择文件后触发的事件
fileInput.addEventListener("change", function () {
    // 获取用户选择的文件
    var files = fileInput.files;
    if (files.length > 0) {
        // 创建一个 FormData 对象，用于将文件数据发送到服务器
        var formData = new FormData();
        formData.append("file", files[0]); // 将文件添加到 FormData 中

        // 创建一个新的 XMLHttpRequest 对象
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/upload/"); // 指定上传文件的 URL

        // 监听上传进度事件
        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                var percentComplete = (event.loaded / event.total) * 100;
                progressBar.style.width = percentComplete + "%"; // 更新进度条宽度
            }
        };

        // 监听上传完成事件
        xhr.onload = function() {
            if (xhr.status == 200) {
                // 上传成功，可以根据服务器返回的数据做进一步处理
                console.log("上传成功");
            } else {
                // 上传失败
                console.error("上传失败");
            }
        };

        // 发送 FormData 到服务器
        xhr.send(formData);
    }
});
