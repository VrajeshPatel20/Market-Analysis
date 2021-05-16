// const getData = () => {
//   fetch("http://127.0.0.1:5000/")
//     .then((response) => {
//       if (!response.ok) {
//         throw Error("ERROR");
//       }
//       return response.json();
//     })
//     .then((responseData) => {
//       const array = responseData;
//       const html = array.map((coin) => {
//         console.log(coin);
//         return `
//           <div style="font-size: x-large;color: #eeee;">
//           <p><li> Crypto : ${coin} </li></p>
//           </div>
//           `;
//       });
//       document.querySelector("#pics").insertAdjacentHTML("afterbegin", html);
//     });
// };
const getData = () => {
  fetch("https://backend00.herokuapp.com/crypto")
    .then((response) => {
      if (!response.ok) {
        throw Error("ERROR");
      }
      return response.json();
    })
    .then((responseData) => {
      const array = responseData;
      results = "<table style=\"width:2000px;k\">";
      for (var i=0; i<array.length; i+=2) {
          results += " <tr><td><div style=\"font-size: xx-large; color: #eeee;\"><li>" + array[i] + "</li></div></td>";  
          if(i+1<array.length){
            results += "<td><div style=\"font-size: xx-large; color: #eeee;\"><li>" + array[i+1] + "</li></div></td></tr>";
          }  
      }
      
      results += "<table><br /> <br />";
      
       var div = document.getElementById("pics");
          div.innerHTML = results;    
    });
};


window.onload = function() {
  getData();
};
function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}

function sendEmail(){
 
  var input = document.getElementById("msg").value;
  var email = document.getElementById("email").value;
  var name = document.getElementById("name").value;

  var detail = name + "\n"+ email + "\n" + input;

  Email.send({
    Host: "smtp.gmail.com",
    Username: "cryptoalerts167@gmail.com",
    Password:"Kaboom001$$@",
    To: "vrajesh1@my.yorku.ca",
    From: "cryptoalerts167@gmail.com",
    Subject: email,
    Body: detail
  }).then(
    message=>alert("mail sent successfully")
  );
}


