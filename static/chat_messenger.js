const messageField = document.getElementById('message'); // get the reference to textarea

                messageField.addEventListener('input', function () {
                    this.placeholder = ''; // Clear the placeholder text
                    this.style.height = 'auto';
                    this.style.height = (this.scrollHeight) + 'px';
                }, false);

                messageField.addEventListener('keydown', function(event) {
                    if (event.key === 'Enter' && !event.shiftKey) {  // Checking for Enter key
                        event.preventDefault();  // prevent the default action (line break in textarea)
                        sendChat();
                    }
                }, false);

                async function sendChat() {
                    const message = messageField.value;
                    const conversationDiv = document.getElementById('conversation');
                    
                    // Append user's message to the conversation
                    conversationDiv.innerHTML += `<p class="user">${message}</p>`;

                    // Clear the input field
                    messageField.value = '';
                    messageField.style.height = 'auto'; // Reset the height of textarea

                    const response = await fetch('http://localhost:5000/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message }),
                    });
                    const responseData = await response.json();
                    
                    // Append assistant's response to the conversation
                    conversationDiv.innerHTML += `<p class="bot">Wall-O: ${responseData}</p>`;            
                }