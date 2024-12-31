document.addEventListener("DOMContentLoaded", () => {
    const notificationContainer = document.createElement("div");
    notificationContainer.id = "notificationContainer";
    notificationContainer.className = "fixed top-20 right-5 z-50 space-y-2";
    document.body.appendChild(notificationContainer);

    window.showNotification = (type, message) => {
        let container = document.getElementById("notificationContainer");
        if (!container) {
            container = document.createElement("div");
            container.id = "notificationContainer";
            container.className = "fixed top-20 right-5 z-50 space-y-2";
            document.body.appendChild(container);
        }

        const notification = document.createElement("div");

        const baseClasses = "px-4 py-2 rounded shadow-md flex items-center space-x-2 text-md";
        const typeClasses =
            type.toLowerCase() === "success"
                ? "bg-green-500 text-white" 
                : "bg-red-500 text-white"; 
 
        notification.className = `${baseClasses} ${typeClasses} fade-in-out`;

        notification.innerHTML = `
            <div>${type.toLowerCase() === "success" ? "✅" : "❌"}</div>
            <div>${message}</div>
        `;

        container.appendChild(notification);

        setTimeout(() => {
            notification.classList.add("opacity-0", "transition-opacity", "duration-500");
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    };
});
