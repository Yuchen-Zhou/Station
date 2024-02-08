document.addEventListener("DOMContentLoaded", function () {
    const newButton = document.getElementById("newButton");
    const userButton = document.getElementById("UserAvatar");

    // 点击新建按钮时显示或隐藏气泡
    newButton.addEventListener("click", function (event) {
        event.stopPropagation(); // 阻止事件冒泡，防止点击按钮时关闭气泡
        popover.style.display = popover.style.display === "none" ? "block" : "none";
    });

    // 点击页面其他位置时隐藏气泡
    document.addEventListener("click", function () {
        popover.style.display = "none";
        userpopover.style.display = "none";
    });
});
