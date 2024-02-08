// 获取头像容器和下拉菜单元素
var avatarContainer = document.getElementById('avatar-container');
var dropdownMenu = document.getElementById('dropdown-menu');

// 点击头像时触发的事件
avatarContainer.addEventListener('click', function () {
    // 切换下拉菜单的显示和隐藏状态
    if (dropdownMenu.classList.contains('hidden')) {
        dropdownMenu.classList.remove('hidden');
    } else {
        dropdownMenu.classList.add('hidden');
    }
});

function toggleSubLinks() {
    var subLinks = document.querySelectorAll("#image_recognition, #image_reconstruction, #video_detection");
    for (var i = 0; i < subLinks.length; i++) {
        if (subLinks[i].style.display === "none") {
            subLinks[i].style.display = "block";
        } else {
            subLinks[i].style.display = "none";
        }
    }
}