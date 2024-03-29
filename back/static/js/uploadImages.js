$(document).ready(function() {
    $('#uploadButton').click(function() {
        var files = $('#images')[0].files;
        if (files.length === 0) {
            console.log('没有选择文件');
            return;
        }

        var formData = new FormData();
        for (var i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }

        $.ajax({
            url: 'http://127.0.0.1:6006/imagesUpload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function(event) {
                    if (event.lengthComputable) {
                        var percentComplete = (event.loaded / event.total) * 100;
                        $('#progressBar').width(percentComplete + '%');
                        $('#progressText').text(percentComplete.toFixed(2) + '% 完成');
                    }
                }, false);
                return xhr;
            },
            success: function(response) {
                console.log('检测完成:', response);
                var folder_name = response.folder_name;
                var results = response.results;

                // 构建新页面的 URL，并将数据作为查询参数附加
                var request_url = 'http://127.0.0.1:6006/images_results?folder_name=' + folder_name + '&results=' + JSON.stringify(results);
                window.open(request_url);
            },
            error: function(xhr, status, error) {
                console.error('上传失败:', error);
            }
        });
    });
});
