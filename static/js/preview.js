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


// 监听文件选择变化，更新预览
document.getElementById('images').addEventListener('change', previewImages);



