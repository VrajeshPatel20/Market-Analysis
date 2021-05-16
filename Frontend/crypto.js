const getData = () => {
  fetch("http://127.0.0.1:5000/")
    .then((response) => {
      if (!response.ok) {
        throw Error("ERROR");
      }
      return response.json();
    })
    .then((responseData) => {
      const array = responseData;
      const html = array.map((coin) => {
        console.log(coin);
        return `
          <div>
          <p> Crypto : ${coin} </p>
          </div>
          `;
      });
      document.querySelector("#pics").insertAdjacentHTML("afterbegin", html);
    });
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


