signined = false;
const socket = io({autoConnect: false});

document.getElementById("join-btn").addEventListener("click", function() {
    let username = document.getElementById("username").value;

    socket.connect();

    socket.on("connect", function() {
        socket.emit("user_join", username);
    })

    document.getElementById("chat").style.display = "block";
    document.getElementById("landing").style.display = "none";
})

document.getElementById("message").addEventListener("keyup", function (event) {
    if (event.key == "Enter") {
        let message = document.getElementById("message").value;
        socket.emit("new_message", message);
        document.getElementById("message").value = "";
    }
})

socket.on("chat", function(data) {
    let ul = document.getElementById("chat-messages");
    let li = document.createElement("li");
    li.appendChild(document.createTextNode(data["username"] + ": " + data["message"]));
    ul.appendChild(li);
    ul.scrolltop = ul.scrollHeight;
})

function register() {
  socket.connect();
  username = "test";
  socket.on("connect", function() {
      socket.emit("user_join", username);
  })

  
  // d3.json('/register', {
  //   method:"POST",
  //   body: JSON.stringify({
  //     username: document.getElementById('username').value,
  //     password: document.getElementById('password').value
  //   }),
  //   headers: {
  //     "Content-type": "application/json; charset=UTF-8",
  //     "Access-Control-Allow-Origin": "*"
  //   }
  // })
  // .then(json => {
  //     if(json.status === 'loggedin' || json.status === 'registered') {
  //         localStorage.setItem('username', json.username);
  //         localStorage.setItem('points', json.points);
  //         localStorage.setItem('status', json.status);
  //         d3.select('#hi_user').html('Hi, ' + json.username);
  //         selectPage('language_page');
  //         signined = true;
  //     } else {
  //         alert('Wrong username or password');
  //     }           
  // });
}

function signin() {
    // d3.json('/login', {
    //   method:"POST",
    //   body: JSON.stringify({
    //     username: document.getElementById('username').value,
    //     password: document.getElementById('password').value
    //   }),
    //   headers: {
    //     "Content-type": "application/json; charset=UTF-8",
    //     "Access-Control-Allow-Origin": "*"
    //   }
    // })
    // .then(json => {
    //     if(json.status === 'loggedin' || json.status === 'registered') {
    //         localStorage.setItem('username', json.username);
    //         localStorage.setItem('points', json.points);
    //         localStorage.setItem('status', json.status);
    //         d3.select('#hi_user').html('Hi, ' + json.username);
    //         selectPage('language_page');
    //         signined = true;
    //     } else {
    //         alert('Wrong username or password');
    //     }           
    // });
}

const validateEmail = (email) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
  };
  
// d3.select('#username').on('input', function() {
//     d3.select('#result').text('');
//     val = d3.select('#username').node().value;
//     if(validateEmail(val)) {
//         d3.select('#result').text(val + ' is valid');
//         d3.select('#result').style('color', 'green');
//     } else {
//         d3.select('#result').text(val + ' is not valid');
//         d3.select('#result').style('color', 'red');
//     }
// });

// d3.select('#password').on('input', function() {
//     val = d3.select('#password').node().value;
//     d3.select('#result1').text('');
//     if(val.length < 5) {
//         d3.select('#result1').text('Password must be at least 5 characters');
//         d3.select('#result1').style('color', 'red');
//     }
// });