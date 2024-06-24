$(document).ready(function () {
    let token = localStorage.getItem("access_token");

    if (token) {
        $.ajaxSetup({
            headers: {
                'X-CSRF-TOKEN': token,
                'Authorization': 'Bearer ' + token
            }
        });
    }
});

// Websocket
// let user_id = prompt("Enter your user ID:");
// let ws = new WebSocket(`ws://localhost:8000/ws/chat/${user_id}`);

// ws.onmessage = function(event) {
//     console.log(event);
//     // let messages = document.getElementById('messages');
//     // let message = document.createElement('div');
//     // message.textContent = event.data;
//     // messages.appendChild(message);
// };

function register() {
    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("userpassword").value;

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/user/register",
        data: {
            username: username,
            email: email,
            password: password
        },
        dataType: "json",
        success: function (response) {
            console.log(response);
        }
    });
}

function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("userpassword").value;

    $.ajax({
        type: "POST",
        url: "/api/v1/login",
        data: {
            username: username,
            password: password
        },
        success: function (response) {
            // Save the token in localStorage or cookies for further use
            localStorage.setItem("access_token", response.access_token);
            localStorage.setItem("refresh_token", response.refresh_token);
            window.location.href = "/";
        },
        error: function (error) {
            console.log(error);
        }
    });
}

// Get User Chats
function getChats() {
    $.ajax({
        type: "GET",
        url: "/api/v1/chats",
        success: function (response) {
            // Display the user's chats
            $("#content").html(response.html_sidebar);
            $("#list_contact").html(response.html_chats);
        }
    });
}

function addContact(id) {
    $.ajax({
        url: "/api/v1/chats",
        type: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        data: JSON.stringify({
            user_id: String(id)
        }),
        success: function(response) {
            // Close the modal
            $("#addContactModal").modal("hide");
        },
        error: function(error) {
            $("#toast-body").html(error.responseJSON.message);
            $("#liveToast").toast("show");
        }
    });
}

function openChat(id) {
    let token = localStorage.getItem("access_token");
    if (!token) {
        console.error("No access token found");
        return;
    }

    let ws = new WebSocket(`ws://localhost:8000/ws/chat/${id}?token=${token}`);
    ws.onmessage = function(event) {
        console.log(event);
    };
    ws.onerror = function(event) {
        console.error("WebSocket error observed:", event);
    };
    $.ajax({
        url: "/api/v1/chats/" + id,
        type: "GET",
        success: function(response) {
            $("#chat-content").html(response.html_contacts);
        },
        error: function(error) {
            $("#toast-body").html(error.responseJSON.message);
            $("#liveToast").toast("show");
        }
    });
}



function editEvent(id) {
    let content = document.getElementById("chat-input").value;

    $.ajax({
        type: "PUT",
        url: `/api/v1/chats/${id}/messages`,
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        data: JSON.stringify({content: content}),
        dataType: "json",
        success: function (response) {
            console.log(response);
        }
    });
}

