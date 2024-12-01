sendButton = $(".chatbot-container .message-container .tools .search #send-button")
inputField = $(".chatbot-container .message-container .tools .search input")
inputElem = $(".chatbot-container .message-container .tools")
messagesContainer = $(".chatbot-container .message-container .conversation")
chatsLoading = $(".chatbot-container .session-container .first #chats-loading")
addNewChatElem = $(".chatbot-container .session-container .first .options .addchat")
deleteChatElem = $(".chatbot-container .session-container .second .clearchat")
chatContainerElem = $(".chatbot-container .session-container .first .options .chats")

messages = []
let userID, chatsList=[], currchatID

/* Preventing hitting "Enter" From Submitting Form instead it'll send Message  */
$(document).ready(function() {
    if(location.href.slice(location.href.length-4)=='/bot'){
        $(window).keydown(function(event){
        if(event.keyCode == 13) {
            event.preventDefault();
            sendButton.click()
            return false;
        }
        });
    }
});

/* Listenning for changes on chatsList */
window.setInterval(()=>{
    if(!currchatID){
        inputElem.css("opacity", "0")
        inputElem.css("pointer-events", "none")
    } else {
        inputElem.css("opacity", "1")
        inputElem.css("pointer-events", "all")
    }
}, 500)


$(window).on("load", ()=>{
    /* Get Current User and Save it to user id */
    $.ajax({
        type:"GET",
        dataType: "json",
        url: "/api/curr/user",
        success:function(id)
        {
            userID = id
            loadChats(id)
        }
    });
})

function loadChats(id){
    /* Loading Chats */
    $.ajax({
        type:"GET",
        dataType: "json",
        url: "/api/chats/"+id,
        success: function(data){
            chatsList = data
            for(let i=0; i<data.length; i++){
                var chatElem = document.createElement("div")
                chatElem.setAttribute("class", "chat")
                var chatElemSpan = document.createElement("span")
                chatElemSpan.setAttribute("id", "text")
                chatElemSpan.append("Chat ")
                var chatElemSpanNumber = document.createElement("span")
                chatElemSpanNumber.append("#"+(i+1))
                chatElem.append(chatElemSpan, chatElemSpanNumber)
                chatElem.setAttribute("onclick", `loadMessagesFor('${data[i]}');toggleChatButton(this);`)
                chatContainerElem.append(chatElem)
            }

        },
        complete: function(){
            chatsLoading.css("display", 'none')
            // Disabling Delete Button if number of chats is 1
            let len = $(".chatbot-container .session-container .first .options .chats").children().length
            if(len==1){
                deleteChatElem.css("opacity", ".4")
                deleteChatElem.css("pointer-events", "none")
                $(".chatbot-container .session-container .first .options .chats .chat").click()
            } else {
                deleteChatElem.css("opacity", "1")
                deleteChatElem.css("pointer-events", "all")
                $(".chatbot-container .session-container .first .options .chats .chat")[len-1].click()
            }
        },
        error: function(){
            chatsLoading.css("display", 'none')
            errorTextElem = document.createElement("p")
            errorTextElem.append("An Error has occured, please try again.")
            errorTextElem.setAttribute("style", "color:var(--white);font-weight:500;font-size:14px;")
            $(".chatbot-container .session-container .first").append(errorTextElem)
        },
        timeout: 30000 
    });
}


function loadMessagesFor(chatID){
    /* Load Previous Messages */
    currchatID = chatID
    messagesContainer.empty()  // Empty Chat
    /*
    var loadingElem = document.createElement("div")
    loadingElem.setAttribute("class", "lds-ring")
    loadingElem.setAttribute("id", "conversation-loading")
    loadingElem.append(document.createElement("div"))
    loadingElem.append(document.createElement("div"))
    loadingElem.append(document.createElement("div"))
    messagesContainer.append(loadingElem)
    */

    $.ajax({
        type:"GET",
        dataType: "json",
        url: "/api/msgs/"+userID+"/"+chatID,
        success:function(data)
        {
            messagesContainer.empty()  // Empty Chat
            data.forEach(message => {
                messages.push([message[0], message[1]]) // [message, type(user or bot)]

                var messageElem = document.createElement("div")
                if(message[1]=="user"){
                    messageElem.setAttribute("class", "user")
                    messageElem.append(message[0])
                    messagesContainer.append(messageElem)
                } else {

                    if(message[0][0]=='GRAPH PLOT' || message[0][0]=='GRAPH PRED'){

                        img_name = message[0][1]

                        div = document.createElement('div')
                        div.setAttribute('class', 'img-container')
                        div.setAttribute('onclick', `window.open('${location.href.replace('/bot', '')}/static/data/${img_name}.png')`)

                        img = document.createElement('div')
                        img.setAttribute("class", "bot-img")
                        img.setAttribute("style", "background-image: url(static/data/"+img_name+".png);")

                        text_inside = document.createElement('p')
                        text_inside.innerHTML = "View Full Image."

                        img_overlay = document.createElement('div')
                        img_overlay.setAttribute("class", "bot-img-overlay")
                        img_overlay.append(text_inside)

                        div.append(img_overlay)
                        div.append(img)
                        messagesContainer.append(div)
                    }
                    else {
                        messageElem.setAttribute("class", "bot")
                        messageElem.innerHTML = message[0][1]
                        messagesContainer.append(messageElem)
                    }
                }

            });
            
            ConvoScrollDown()
        },
        complete: function(){
            convoLoading = $(".chatbot-container .message-container .conversation #conversation-loading")
            convoLoading.css("display", "none")
        },
        error: function(){
            convoLoading = $(".chatbot-container .message-container .conversation #conversation-loading")
            convoLoading.css("display", "none")
            errorTextElem = document.createElement("p")
            errorTextElem.append("An Error has occured, please try again.")
            errorTextElem.setAttribute("style", "color:var(--message-white);margin:0 auto;")
            messagesContainer.append(errorTextElem)
        },
        timeout: 30000
        
    });
}

sendButton.on("click", ()=>{
    if(inputField.val().trim()){
        sendButton.addClass("sent")
        setTimeout(function() {
            sendButton.removeClass("sent")
        }, 1000);
        // Generating Message Element
        /*var messageElem = document.createElement("div")
        messageElem.setAttribute("class", "user")
        messageElem.setAttribute("style", "opacity: .4;")
        messageElem.append(inputField.val().trim())
        */

        //Loading
        let loadingReply = document.createElement('div')
        loadingReply.setAttribute("class", "loadingio-spinner-dual-ring-3ihhaxjkj9m")
        let loadingReplyChild = document.createElement('div')
        loadingReplyChild.setAttribute("class", "ldio-vnlgna7uy9")
        loadingReplyChild.append(document.createElement('div'))
        let loadingReplyChildDiv = document.createElement('div')
        loadingReplyChildDiv.append(document.createElement('div'))
        loadingReplyChild.append(loadingReplyChildDiv)
        loadingReply.append(loadingReplyChild)

        document.querySelector(".chatbot-container .message-container .tools").append(loadingReply)
        document.querySelector(".chatbot-container .message-container .tools .search").setAttribute("style", "opacity: 0;")


        // Sending Data to server
        $.ajax({ 
            url: '/bot', 
            type: 'POST', 
            data: "INSERT " + inputField.val().trim()+" "+currchatID,
            complete: function(){
                //messageElem.setAttribute("style", "opacity: 1;")
                loadMessagesFor(currchatID)
                document.querySelector(".chatbot-container .message-container .tools .loadingio-spinner-dual-ring-3ihhaxjkj9m").remove()
                document.querySelector(".chatbot-container .message-container .tools .search").setAttribute("style", "opacity: 1;")
            }
        })

        // Adding messages to ConvoElem (showing live messages to user)
        //messagesContainer.append(messageElem)

        // Clearing Input Field 
        inputField.val('')
        ConvoScrollDown()
    }
})

addNewChatElem.on("click", ()=>{
    // Add New Chat
    // Sending Data to server
    $.ajax({ 
        url: '/bot', 
        type: 'POST', 
        data: "AddChat",
        complete: function(){
            //Refresh Chats
            chatContainerElem.empty()
            loadChats(userID)
        }
    })
})

deleteChatElem.on("click", ()=>{
    // Delete Chat
    // Sending Data to server
    let len = $(".chatbot-container .session-container .first .options .chats").children().length
    if(len!=1 && currchatID){
        $.ajax({ 
            url: '/bot', 
            type: 'POST', 
            data: "DeleteChat none "+currchatID,
            complete: function(){
                chatContainerElem.empty()
                loadChats(userID)
            }
        })
    } else {
        
    }
})




function ConvoScrollDown(){
    $(".chatbot-container .message-container .conversation").scrollTop($(".chatbot-container .message-container .conversation").prop("scrollHeight"));
}

function toggleChatButton(e){
    $(".chatbot-container .session-container .first .options .chats .chat").css("background-color", "var(--convo-grey)")
    $(".chatbot-container .session-container .first .options .chats .chat").css("color", "var(--white)")
    $(e).css("background-color", "var(--primary)")
    $(e).css("color", "white")
}