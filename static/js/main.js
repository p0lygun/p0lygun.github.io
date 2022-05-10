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
