document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // 将 CSRF token 存储到全局变量
    window.csrfToken = csrftoken;
});
