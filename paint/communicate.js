/*  CORS のせいで、３時間無駄にした...。
 *  結局、完全には理解できてないけど、
 *    1. Flask(Python) サーバー の場合は、
 *        flask-cors ライブラリを pip でインストールして、
 *        ごちゃごちゃ書き足さないといけないっぽい。
 *        ・ https://www.hands-lab.com/tech/entry/3716.html
 *        ・ https://developer.yukimonkey.com/article/20200227/
 * 
 *    2. JavaScript の（低レベルな）GET, POST メソッドとして
 *        XMLHttpRequest, fetch, axios があるが。
 *        ・ axios はなぜかエラーで動かなかった...。
 *        ・ fetch　→　動いた！？
 *        ・ XMLHttpRequest は試してない。
 */


//*--  GET通信  --*//
//// axios
axios.defaults.withCredentials = true
// function getMessage(params) {
//   axios
//     .get("http://0.0.0.0:5111/uiuxchat3287bivsgfbivf/dotsubos-test/messages/to/hogesan", {
//       withCredentials: true,
//       headers: {
//         Cookie: "key=gfg43827hnfdsfai"
//       }
//     })
//     .then(function (response) {
//       // handle success
//       console.log(response);
//     })
//     .catch(function (error) {
//       // handle error
//       console.log(error);
//     })
//     .finally(function () {
//       // always executed
//     });
// }
//// fetch
const getMessage = async (url = ``, data = {}) => {
    const response = await fetch( url, {
        // method: "POST", 
        // mode: "cors", // no-cors, cors, *same-origin
        // cache: "no-cache",
        // credentials: "same-origin",
        headers: {
          // "Cookie": "key=gfg43827hnfdsfai",
          // "Content-Type": "application/json; charset=utf-8",
        },
        // redirect: "follow",
        // referrer: "no-referrer",
    })
    const myJson = await response.json(); //extract JSON from the http response
    console.log( myJson );
}


//*--  POST通信  --*//
// function postMessage(params) {
//     $.post( 'http://0.0.0.0:5111/uiuxchat3287bivsgfbivf/dotsubos-test/messages/to/hogesan' )  //, 'key=gfg43827hnfdsfai' 
//     .done(function( data ) {
//         console.log( data.form );
//     })
// }

// function postData(url = ``, data = {}) {
//     return fetch(url, {
//         method: "POST", 
//         // mode: "cors", // no-cors, cors, *same-origin
//         // cache: "no-cache",
//         // credentials: "same-origin",
//         headers: {
//           "Cookie": "key=gfg43827hnfdsfai",
//           "Content-Type": "application/json; charset=utf-8",
//         },
//         // redirect: "follow",
//         // referrer: "no-referrer",
//         body: JSON.stringify(data), 
//     })
//     .then(response => response.json()); 
// }

function postData(url = ``, data = {}) {
  return axios.post(url, {
    withCredentials: true,
    headers: {
        Cookie: "key=gfg43827hnfdsfai; cookie2=value; cookie3=value;"
    }
  })
  .then(response => response.json()); 
}


