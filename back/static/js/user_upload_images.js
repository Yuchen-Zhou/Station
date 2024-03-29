    $(document).ready(function () {
            // 获取上传按钮和文件输入框
            var $uploadButton = $("#uploadButton");
            var $fileInput = $("#fileInput");
            var $progressBar = $(".progress-bar");
            var $progress = $(".progress");

            // 监听上传按钮点击事件
            $uploadButton.on("click", function () {
                // 触发文件输入框的点击事件
                $fileInput.click();
            });

            // 监听文件输入框的change事件
            $fileInput.on("change", function () {
                $progress.show();
                // 获取选中的文件列表
                var files = $fileInput[0].files;

                // 创建FormData对象
                var formData = new FormData();

                // 将每个选中的文件添加到FormData中
                for (var i = 0; i < files.length; i++) {
                    formData.append("files[]", files[i]);
                }

                // 发送文件到后端处理
                $.ajax({
                    url: "/infoSys/UserImages",
                    type: "POST",
                    data: formData,
                    processData: false,
                    contentType: false,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    xhr: function () {
                        var xhr = new window.XMLHttpRequest();
                    }
                    success: function (data) {
                        console.log("文件上传成功");
                        window.location.href = '/infoSys/UserImages'
                    },
                    error: function () {
                        console.error("文件上传失败");
                    }
                });
            });
        });
