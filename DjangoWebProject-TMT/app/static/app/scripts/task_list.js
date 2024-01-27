
    // Fetch tasks data from the server for the logged in user
    fetch('/task-json/')
        .then(response => response.json())
        .then(tasks => {
            console.log(tasks);
            // Check if the browser supports notifications
            if (!("Notification" in window)) {
                alert("This browser does not support desktop notification");
            }

            // Let's check whether notification permissions have already been granted
            else if (Notification.permission === "granted") {
                // If it's okay let's create a notification
                if(!localStorage.getItem('notified')){
                    notifyTasks(tasks);
                    localStorage.setItem('notified', 'true');
                }
            }

            // Otherwise, we need to ask the user for permission
            else if (Notification.permission !== 'denied') {
                Notification.requestPermission().then(function (permission) {
                    // If the user accepts, let's create a notification
                    if (permission === "granted") {
                        notifyTasks(tasks);
                        localStorage.setItem('notified', 'true');
                    }
                });
            }
        });

    function notifyTasks(tasks) {
        tasks.forEach(task => {
            // Check if the due date is within 2 days
            let dueDate = new Date(task.fields.due_date);
            let now = new Date();
            let diffTime = Math.abs(dueDate - now);
            let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            if (diffDays <= 2) {
                var notification = new Notification(`Task ${task.fields.title} is due in ${diffDays} days`);
            }
        });
    }

    // Add event listener for logout button
    window.addEventListener('load', function() {
        var logoutForm = document.getElementById('logoutForm');
        if (logoutForm) {
            logoutForm.addEventListener('click', function() {
                // Clear the 'notified' flag from local storage when the user logs out
                localStorage.removeItem('notified');
            });
        }
    });
