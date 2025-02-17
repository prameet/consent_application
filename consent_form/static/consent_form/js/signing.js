document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("signatureCanvas");
    const ctx = canvas.getContext("2d");
    const signatureInput = document.getElementById("signatureInput");
    const clearButton = document.getElementById("clearButton");

    // تنظیمات اولیه
    ctx.strokeStyle = "#000"; // رنگ قلم
    ctx.lineWidth = 2; // ضخامت خط
    ctx.lineCap = "round"; // انتهای خط گرد

    // تابع تنظیم اندازه بوم
    function setCanvasSize() {
        canvas.width = 550; // عرض بوم را برابر با عرض والدش قرار می‌دهیم
        canvas.height = 200; // ارتفاع ثابت
    }

    setCanvasSize();
    // تنظیم اندازه بوم هنگام بارگذاری صفحه و تغییر اندازه
    window.addEventListener("load", setCanvasSize);
    window.addEventListener("resize", setCanvasSize);

    let drawing = false;

    // گرفتن مختصات موس/لمس
    function getCoordinates(event) {
        if (event.touches) {
            const rect = canvas.getBoundingClientRect();
            return {
                x: event.touches[0].clientX - rect.left,
                y: event.touches[0].clientY - rect.top,
            };
        } else {
            return {x: event.offsetX, y: event.offsetY};
        }
    }

    // شروع رسم
    function startDrawing(event) {
        event.preventDefault();
        drawing = true;
        const {x, y} = getCoordinates(event);
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    // رسم خط
    function draw(event) {
        if (!drawing) return;
        event.preventDefault();
        const {x, y} = getCoordinates(event);
        ctx.lineTo(x, y);
        ctx.stroke();
    }

    // توقف رسم و ذخیره امضا
    function stopDrawing() {
        drawing = false;
        saveSignature();
    }

    // ذخیره امضا در input مخفی
    function saveSignature() {
        signatureInput.value = canvas.toDataURL("image/png");
    }

    // پاک کردن بوم و مقدار input
    function clearCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        signatureInput.value = "";
    }

    // رویدادهای موس
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseleave", stopDrawing);

    // رویدادهای لمسی (پشتیبانی از موبایل)
    canvas.addEventListener("touchstart", startDrawing);
    canvas.addEventListener("touchmove", draw);
    canvas.addEventListener("touchend", stopDrawing);

    // دکمه پاک کردن امضا
    clearButton.addEventListener("click", clearCanvas);

});
