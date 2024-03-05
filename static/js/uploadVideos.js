$(document).ready(function() {
    $('#uploadButton').click(function() {
        var files = $('#video')[0].files; // 修改文件输入框的ID为videos
        if (files.length === 0) {
            console.log('没有选择文件');
            return;
        }

        var formData = new FormData();
        for (var i = 0; i < files.length; i++) {
            formData.append('video', files[i]); // 修改键名为videos
        }

        $.ajax({
            url: 'http://127.0.0.1:6006/videoUpload', // 修改为视频上传接口的URL
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function(event) {
                    if (event.lengthComputable) {
                        var percentComplete = (event.loaded / event.total) * 100;
                        $('#progressBar').width(percentComplete + '%'); // 修改进度条的ID为progressBar
                        $('#progressText').text(percentComplete.toFixed(2) + '% 完成'); // 修改进度文本的ID为progressText
                    }
                }, false);
                return xhr;
            },
            success: function(response) {
                console.log('上传成功:', response);
                // 处理上传成功的响应数据
            },
            error: function(xhr, status, error) {
                console.error('上传失败:', error);
                // 处理上传失败的响应数据
            }
        });
    });
});
