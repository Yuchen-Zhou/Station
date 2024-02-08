function expandSidebar() {
    document.getElementById("sidebar").style.width = "250px";
    document.getElementById("content").style.marginLeft = "250px"; /* 调整内容区域左边距 */
    document.getElementsByClassName("top-bar")[0].style.left = "250px"; /* 调整顶部栏位置 */
    document.getElementsByClassName("top-bar")[0].style.width = "calc(100% - 250px)"; /* 调整顶部栏宽度 */
}

function collapseSidebar() {
    document.getElementById("sidebar").style.width = "20px";
    document.getElementById("content").style.marginLeft = "50px"; /* 调整内容区域左边距 */
    document.getElementsByClassName("top-bar")[0].style.left = "20px"; /* 调整顶部栏位置 */
    document.getElementsByClassName("top-bar")[0].style.width = "calc(100% - 50px)"; /* 调整顶部栏宽度 */
}
