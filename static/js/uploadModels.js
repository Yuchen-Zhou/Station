$(document).ready(function() {
    $('#uploadButton2').click(function() {
        var files = $('#file')[0].files;
        if (files.length === 0) {
            console.log('没有选择文件');
            return;
        }

        var formData = new FormData();
        for (var i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }

        $.ajax({
            url: '#',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                return xhr;
            },
            success: function(response) {
                console.log('上传成功:', response);

            },
            error: function(xhr, status, error) {
                console.error('上传失败:', error);
            }
        });
    });
});
