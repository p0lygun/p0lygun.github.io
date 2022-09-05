if(window.location.hostname !== "0.0.0.0") {
    window.addEventListener('load', schedule_set_online_presence)
}

async function schedule_set_online_presence(){
    await fetch("https://ranger.stilllearning.tech/user/?id=338947895665360898&guild_id=870246147455877181").then(
        resp => resp.json().then(json =>set_online_presence(json)))

    setTimeout(schedule_set_online_presence,60000); // call itself every 1 min
}

function set_online_presence(json){
    if(json['status']){
        const status_element = document.getElementById("online-status"),
            status_dot = document.getElementById("online-status-dot");
        if(json['message'] === "online"){
            status_element.textContent = "Online"
            if(status_dot.classList.contains("offline")){
                status_dot.classList.remove("offline");
            }
            status_dot.classList.add("online");
        } else {
            status_element.textContent = "Offline"
            if(status_dot.classList.contains("online")){
                status_dot.classList.remove("online");
            }
            status_dot.classList.add("offline");
        }
    }
}

function checkCommandInput(event){
    if (event.key === "Enter") {
        const command = document.getElementById("command-input").value;
        const input = document.getElementById("command-input");
        const valid_cmds = ["fetch"];
        const cmd_array = command.split(" ");
        if (cmd_array[0] === "fetch") {
            if (cmd_array[1] === "about") {
                window.location = window.location.origin;
            } else if (cmd_array[1] === "contact") {
                window.location = window.location.origin + "/contact";
            }
        } else if (cmd_array[0] === "help") {
            document.getElementById("error-text").textContent = ``;
            document.getElementById("stdout").textContent = `Available commands are ${valid_cmds.toString()}`;

        } else {
            document.getElementById("error-text").textContent = `Command ${input.value} not found,\nUse command \`help\` for more info`;
        }
        input.value = '';
    }
}

const input = document.getElementById("command-input");
const ps1 = document.getElementsByClassName("PS1")[0];
input.focus();
input.value = '';
if (window.location.pathname === "/contact") {
  input.value = "fetch contact";
}
input.addEventListener('keypress', checkCommandInput);
input.setAttribute('size',`${input.getAttribute('placeholder').length}`);
window.addEventListener('focus', function (event) {
   input.focus();
});
ps1.addEventListener('click', function () {
    input.focus();
});
