<template>

  <button class="open-button" @click="openForm()">Chat</button>

  <div class="chat-popup" id="myForm">
    <div class="form-container">
      <i class="fa-solid fa-chalkboard-user"></i>
      <h3>Chat with us
      </h3>
      <button type="button" class="close mb-4" style="float: right;" aria-label="Close" 
        @click="closeForm()">
        <span aria-hidden="true">&times;</span>
      </button>
      <label for="msg" class="p-2">Message</label>
      <textarea placeholder="Type message.." name="msg" v-model="query" required></textarea>
      <button type="submit" class="btn" @click="submitForm()" :disabled="disableChatBtn">Send</button>
      <div class="container queryResults">
        <p><b>Chat results</b></p>
      </div>

    </div>
  </div>
  <router-view></router-view>
</template>

<script setup>
import { backendUrl } from '@/config';
import { ref } from 'vue';

const url = backendUrl + 'ai/chat';
const query = ref('');
const disableChatBtn = ref(false);

function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

async function submitForm() {
  console.log("URL: ", url);
  disableChatBtn.value = true
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'token ' + localStorage.getItem('auth_token')
      },
      body: JSON.stringify({ query: query.value })
    })
    if (response.ok) {
      const data = await response.json();
      console.log("Data: ", data);
      const resultText = data.result;
      document.querySelector('.queryResults').innerHTML = `<p>Question: ${query.value}` + `<p>Answer: ${resultText}</p>` + document.querySelector('.queryResults').innerHTML;
      query.value = '';

    } else {
      const data = await response.json()
      this.error = data['error']
    }
  } catch (err) {
    this.error = 'Network error. Please try again.'
  } finally {
    disableChatBtn.value = false;
    console.log("Query cycle complete");
  }
}
</script>

<style scoped>
h3 {
  line-height: 0rem;
}

/* Button used to open the chat form - fixed at the bottom of the page */
.open-button {
  padding: 10px 40px;
  background-color: #04AA6D;
  color: white;
  font-size: 17px;
  max-width: 300px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  position: fixed;
  bottom: 23px;
  right: 28px;
}

/* The popup chat - hidden by default */
.chat-popup {
  display: none;
  position: fixed;
  bottom: 0;
  right: 15px;
  z-index: 9;

}

/* Add styles to the form container */
.form-container {
  max-width: 300px;
  padding: 20px;
  border-radius: 20px;
  background-color: rgb(65, 59, 59);
  color: #ede7e7;
  height: 400px;
  max-height: 400px;
  overflow: auto;
}

/* Full-width textarea */
.form-container textarea {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  border: none;
  border-radius: 20px;
  background: #ddd;
  resize: none;
  min-height: 25px;
  color: #777;
}

/* When the textarea gets focus, do something */
.form-container textarea:focus {
  background-color: #ddd;
  outline: none;
}

/* Set a style for the submit/send button */
.form-container .btn {
  background-color: #04AA6D;
  color: white;
  font-size: 17px;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  width: 100%;
  margin-bottom: 10px;
}

/* Add a red background color to the cancel button */
.form-container .cancel {
  background-color: #1974D2;
}

/* Add some hover effects to buttons */
.form-container .btn:hover,
.open-button:hover {
  opacity: 0.8;
}


</style>