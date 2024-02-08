function previewImages() {
    var preview = document.getElementById('preview');
    preview.innerHTML = '';

    var input = document.getElementById('images');
    var files = input.files;

    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var reader = new FileReader();

        reader.onload = function (e) {
            var img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'thumbnail';
            preview.appendChild(img);
        };

        reader.readAsDataURL(file);
    }
}

function uploadImages() {
    var input = document.getElementById('images');
    var files = input.files;

    // 此处可以使用 XMLHttpRequest 或 Fetch API 将文件上传到服务器
    // 以下是一个简单的演示，实际中需要根据后端的处理方式进行调整

    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        // 模拟上传到服务器的操作，实际中需要替换成真实的后端接口
        console.log('Uploading file:', file);
    }
}

function viewDetectResults() {
    window.location.href = "{% url 'detect_results' %}"
}

// 监听文件选择变化，更新预览
document.getElementById('images').addEventListener('change', previewImages);