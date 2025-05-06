css = """
<style>
.chat-message {
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: row;
}
.chat-message.user {
    background-color: #DCF8C6;
    justify-content: flex-end;
}
.chat-message.bot {
    background-color: #F1F0F0;
    justify-content: flex-start;
}
.chat-message .message {
    max-width: 80%;
}
</style>
"""

user_template = """
<div class="chat-message user">
    <div class="message">{{MSG}}</div>
</div>
"""

bot_template = """
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
"""
