const wrapper = document.querySelector(".wrapper"),
editableInput = wrapper.querySelector(".editable"),
readonlyInput = wrapper.querySelector(".readonly"),
placeholder = wrapper.querySelector(".placeholder"),
counter = wrapper.querySelector(".counter"),
button = wrapper.querySelector("button");

editableInput.onfocus = ()=>{
  placeholder.style.color = "#c5ccd3";
}
editableInput.onblur = ()=>{
  placeholder.style.color = "#98a5b1";
}

editableInput.onkeyup = (e)=>{
  let element = e.target;
  validated(element);
}
editableInput.onkeypress = (e)=>{
  let element = e.target;
  validated(element);
  placeholder.style.display = "none";
}

function validated(element){
  let text;
  let maxLength = 300;
  let currentlength = element.innerText.length;

  if(currentlength <= 0){
    placeholder.style.display = "block";
    counter.style.display = "none";
    button.classList.remove("active");
  }else{
    placeholder.style.display = "none";
    counter.style.display = "block";
    button.classList.add("active");
  }

  counter.innerText = maxLength - currentlength;

  if(currentlength > maxLength){
    let overText = element.innerText.substr(maxLength); //extracting over texts
    overText = `<span class="highlight">${overText}</span>`; //creating new span and passing over texts
    text = element.innerText.substr(0, maxLength) + overText; //passing overText value in textTag variable
    readonlyInput.style.zIndex = "1";
    counter.style.color = "#e0245e";
    button.classList.remove("active");
  }else{
    readonlyInput.style.zIndex = "-1";
    counter.style.color = "#333";
  }
  readonlyInput.innerHTML = text; //replacing innerHTML of readonly div with textTag value
}


//ACCOUNT TOGGLE BUTTONS

const accountBtn = document.querySelector(".account-btn"),
      settings = document.querySelector(".setting");
      
try {
  accountBtn.addEventListener("click", () => {
    accountBtn.classList.toggle("open");
  });
} catch (error) {
  console.error("An error occurred:", error.message);
}

function toggleIconAcct(id) {
  const toggleButton = document.getElementById('toggle' + id);
  const settingsDiv = document.getElementById('settings' + id);
  if (toggleButton.src.match('static/toggle-off.svg')) {
    toggleButton.src = "static/toggle-on.svg";
    settingsDiv.style.display = "block";
  } else {
    toggleButton.src = "static/toggle-off.svg";
    settingsDiv.style.display = "none";
  }
}

function toggleIconPub(id) {
  const toggleButton = document.getElementById('togglePub' + id);
  if (toggleButton.src.match('static/toggle-off.svg')) {
    toggleButton.src = "static/toggle-on.svg";
  } else {
    toggleButton.src = "static/toggle-off.svg";
  }
}

function toggleIconRep(id) {
  const toggleButton = document.getElementById('toggleRep' + id);
  if (toggleButton.src.match('static/toggle-off.svg')) {
    toggleButton.src = "static/toggle-on.svg";
  } else {
    toggleButton.src = "static/toggle-off.svg";
  }
}


//PLUS BUTTON
// Get the button and login form elements
document.addEventListener('DOMContentLoaded', function() {
  // Get the button and login form elements
  const plusBtn = document.getElementById('plusbtn');
  const loginForm = document.querySelector('.center');

  // Add event listener to the button
  plusBtn.addEventListener('click', function() {
    // Toggle visibility of the login form
    if (loginForm.style.display === 'none' || loginForm.style.display === '') {
      loginForm.style.display = 'block';
    } else {
      loginForm.style.display = 'none';
    }
  });
});

function copyContent () {
  document.getElementById("post-text").value =  
      document.getElementById("editable-text-area").innerHTML;
  return true;
}

// function delAccount (id) {
//   document.getElementById("del_account".concat(id)).value = 
//       document.getElementById("img_del_account".concat(id)).innerHTML;
//   return true;
// }

//EDITED
//responsive
window.addEventListener('load', function() {
  adjustPadding();
});

window.addEventListener('resize', function() {
  adjustPadding();
});

function adjustPadding() {
  const headerHeight = document.querySelector('header').offsetHeight;
  const bottomButtonHeight = document.querySelector('.bottom-button').offsetHeight;
  const totalHeight = headerHeight + bottomButtonHeight;
  document.body.style.paddingTop = headerHeight + 'px';
  document.body.style.paddingBottom = bottomButtonHeight + 'px';
}

