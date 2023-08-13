let form = document.querySelector("form")
let textArea = document.querySelector("textarea")
let chatContainer = document.querySelector("#chat_container");
let loadInterval;
textArea.addEventListener("input", (e) => {
    e.target.style.height = "0px";
    e.target.style.height = e.target.scrollHeight + "px";
})
function loader(elm) {
    elm.textContent = "";
    loadInterval = setInterval(() => {
        elm.textContent += ".";
        if (elm.textContent.length == 4) {
            elm.textContent = ""
        }
    }, 300)
};
function typeText(elm, text) {
    let index = 0;
    let interval = setInterval(() => {
        console.log(text)
        if (index < text.length) {
            elm.innerHTML += text.charAt(index)
            index++;
        } else {
            clearInterval(interval);
        }
    }, 20)
}
function generateUniqueId() {
    const id = Date.now()
    const random = Math.random();
    const hexaDecimal = random.toString(16)
    return `id-${id}-${hexaDecimal}`
}
function chatStrip(isAi, value, id) {
    const profile = `
        <div class="profile">
            <img src="${isAi ? '/static/assets/bot.png' : '/static/assets/user.svg'}" 
            alt="${isAi ? 'bot' : 'user'}" />
        </div>
    `
    return (
        `
            <div class="message_wrapper ${isAi ? "ai" : "user"} ">
                <div class="chat">
                    ${isAi ? profile : ""}
                    <div class="message" id="${id}">${value}</div>
                    ${!isAi ? profile : ""}
                </div>
            </div>
        `
    )
}
const handleSubmit = async (prompt) => {
    // users chatstripe
    chatContainer.innerHTML += chatStrip(false, prompt, generateUniqueId());
    // bot chatstrip
    const uniqueId = generateUniqueId();
    chatContainer.innerHTML += chatStrip(true, "", uniqueId);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    const messageDiv = document.getElementById(uniqueId);
    loader(messageDiv);
    // fetch data from server
    let responce = await fetch("/" + prompt)
    clearInterval(loadInterval);
    messageDiv.innerHTML = "";
    if (responce.ok) {
        const data = await responce.json();
        const parseData = data.result.trim();
        console.log(data)
        typeText(messageDiv, parseData)
    } else {
        const err = await responce.text();
        messageDiv.innerHTML = "Something went wrong";
        alert(err)
    }
}
form.addEventListener("submit", handleSubmit)
textArea.addEventListener("keydown", (e) => {
    if (!e.shiftKey && e.key === "Enter") {
        e.preventDefault()
        const prompt = textArea.value;
        textArea.style.height = "auto"
        textArea.value = ""
        handleSubmit(prompt)
    }
});