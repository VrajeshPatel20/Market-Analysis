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
