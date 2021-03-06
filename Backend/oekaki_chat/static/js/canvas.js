window.addEventListener("load", () => {

    // CSRF token 設定
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    
    //*--  WebSocket 初期化  --*//
    console.log("[Info][chatSocket.onmessage] roomName :", roomName)
    var socket_url = 'ws://' + window.location.host + '/ws/chat/' + roomName + '/';
    var chatSocket = new WebSocket(socket_url);
    console.log('[Info][init] chatSocket :', chatSocket);

    
  const canvas = document.querySelector("#draw-area");
  ctx = canvas.getContext("2d");
  ctx.fillStyle = "#FFFFFF"; //筆に白い絵の具をつけて
  ctx.fillRect(0, 0, 600, 300); //四角を描く
  const context = canvas.getContext("2d");

  // 現在のマウスの位置を中心に、現在選択している線の太さを「○」で表現するために使用するcanvas
  const canvasForWidthIndicator = document.querySelector(
    "#line-width-indicator"
  );
  const contextForWidthIndicator = canvasForWidthIndicator.getContext(
    "2d"
  );

  const lastPosition = { x: null, y: null };
  let isDrag = false;
  let currentColor = "#000000";
  let previousColors = null;
  let reviousLineWidth = null;

  // 現在の線の太さを記憶する変数
  // <input id="range-selector" type="range"> の値と連動する
  let currentLineWidth = 1;

  function draw(x, y) {
    if (!isDrag) {
      return;
    }
    context.lineCap = "round";
    context.lineJoin = "round";
    context.lineWidth = currentLineWidth;
    context.strokeStyle = currentColor;
    if (lastPosition.x === null || lastPosition.y === null) {
      context.moveTo(x, y);
    } else {
      context.moveTo(lastPosition.x, lastPosition.y);
    }
    context.lineTo(x, y);
    context.stroke();

    lastPosition.x = x;
    lastPosition.y = y;
  }

  // <canvas id="line-width-indicator"> 上で現在のマウスの位置を中心に
  // 線の太さを表現するための「○」を描画する。
  function showLineWidthIndicator(x, y) {
    contextForWidthIndicator.lineCap = "round";
    contextForWidthIndicator.lineJoin = "round";
    contextForWidthIndicator.strokeStyle = currentColor;

    // 「○」の線の太さは細くて良いので1で固定
    contextForWidthIndicator.lineWidth = 1;

    // 過去に描画「○」を削除する。過去の「○」を削除しなかった場合は
    // 過去の「○」が残り続けてします。(以下の画像URLを参照)
    // https://tsuyopon.xyz/wp-content/uploads/2018/09/line-width-indicator-with-bug.gif
    contextForWidthIndicator.clearRect(
      0,
      0,
      canvasForWidthIndicator.width,
      canvasForWidthIndicator.height
    );

    contextForWidthIndicator.beginPath();

    // x, y座標を中心とした円(「○」)を描画する。
    // 第3引数の「currentLineWidth / 2」で、実際に描画する線の太さと同じ大きさになる。
    // ドキュメント: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/arc
    contextForWidthIndicator.arc(
      x,
      y,
      currentLineWidth / 2,
      0,
      2 * Math.PI
    );

    contextForWidthIndicator.stroke();
  }

  function clear() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    ctx = canvas.getContext("2d");
    ctx.fillStyle = "#FFFFFF"; //筆に白い絵の具をつけて
    ctx.fillRect(0, 0, 600, 300); //四角を描く あとで調べる
  }

  function dragStart(event) {
    context.beginPath();

    isDrag = true;
  }

  function dragEnd(event) {
    context.closePath();
    isDrag = false;
    lastPosition.x = null;
    lastPosition.y = null;
  }


  function initEventHandler() {
    const clearButton = document.querySelector("#clear-button");
    // const eraserButton = document.querySelector("#eraser-button");
    clearButton.addEventListener("click", clear);

    // layeredCanvasAreaは2つのcanvas要素を保持している。2つのcanvasはそれぞれ以下の役割を持つ
    //
    // 1. 絵を書くためのcanvas
    // 2. 現在のマウスの位置を中心として、太さを「○」の形で表現するためのcanvas
    //
    // 1と2の機能を1つのキャンパスで共存することは出来ない。
    // 共存できない理由は以下の通り。
    //
    // - 1の機能は過去に描画してきた線の保持し続ける
    // - 2の機能は前回描画したものを削除する必要がある。削除しなかった場合は、過去の「○」が残り続けてしまう。(以下の画像URLを参照)
    //   - https://tsuyopon.xyz/wp-content/uploads/2018/09/line-width-indicator-with-bug.gif
    //
    // 上記2つの理由より
    // - 1のときはcontext.clearRectを使うことが出来ず
    // - 2のときはcontextForWidthIndicator.clearRectを使う必要がある
    const layeredCanvasArea = document.querySelector(
      "#layerd-canvas-area"
    );

    // 元々はcanvas.addEventListenerとしていたが、
    // 2つのcanvasを重ねて使うようになったため、親要素である <span id="layerd-canvas-area">に対して
    // イベント処理を定義するようにした。
    layeredCanvasArea.addEventListener("mousedown", dragStart);
    layeredCanvasArea.addEventListener("mouseup", dragEnd);
    layeredCanvasArea.addEventListener("mouseout", dragEnd);
    layeredCanvasArea.addEventListener("mousemove", (event) => {
      // 2つのcanvasに対する描画処理を行う

      // 実際に線を引くcanvasに描画を行う。(ドラッグ中のみ線の描画を行う)
      draw(event.layerX, event.layerY);

      // 現在のマウスの位置を中心として、線の太さを「○」で表現するためのcanvasに描画を行う
      showLineWidthIndicator(event.layerX, event.layerY);
    });
  }

  function initColorPalette() {
    const joe = colorjoe.rgb("color-palette", currentColor);
    joe.on("done", (color) => {
      currentColor = color.hex();
    });
  }

  // 文字の太さの設定・更新を行う機能
  function initConfigOfLineWidth() {
    const textForCurrentSize = document.querySelector("#line-width");
    const rangeSelector = document.querySelector("#range-selector");
    const numberField = document.getElementById("line-width-number-field");

    // 線の太さを記憶している変数の値を更新する
    currentLineWidth = rangeSelector.value;

   // 線を<input type='number'>からも更新できるようにする。
    numberField.addEventListener("input", (event) => {
      const width = event.target.value;
      // 線の太さを記憶している変数の値を更新する
      currentLineWidth = width;
      updateLineWidth(currentLineWidth);
      // rangeSelector.value = width;
      // 更新した線の太さ値(数値)を<input id="range-selector" type="range">の右側に表示する
      // textForCurrentSize.innerText = width;
    });
    // "input"イベントをセットすることでスライド中の値も取得できるようになる。
    // ドキュメント: https://developer.mozilla.org/ja/docs/Web/HTML/Element/Input/range

    rangeSelector.addEventListener("input", (event) => {
      const width = event.target.value;
      // 線の太さを記憶している変数の値を更新する
      currentLineWidth = width;
      updateLineWidth(currentLineWidth);
      // numberField.value = width;
      // 更新した線の太さ値(数値)を<input id="range-selector" type="range">の右側に表示する
      // textForCurrentSize.innerText = width;
    });
  }

// 線の太さを更新して表示する
  function updateLineWidth(LineWidth){
    const textForCurrentSize = document.querySelector("#line-width");
    const rangeSelector = document.querySelector("#range-selector");
    const numberField = document.getElementById("line-width-number-field");

    textForCurrentSize.innerText = LineWidth;

    if(rangeSelector.value != LineWidth){
      rangeSelector.value = LineWidth;
    }
    if(numberField.value != LineWidth){
      numberField.value = LineWidth;
    }
  }

  const switch_btn = document.getElementById('switch_pen_eraser')
  switch_btn.addEventListener('click', checkSwitchBtn)

  // swichボタン
  function checkSwitchBtn(){
    const color_palette = document.getElementById('color-palette')
    const color_palette_div = document.getElementById('color-palette-div')

    if(switch_btn.checked == true){ //消しゴム
      console.log('消しゴムモード');
      previousColors = currentColor;
      previousLineWidth = currentLineWidth;
      currentColor = "#FFFFFF";
      //カラーパレットのクリックを無効化
      color_palette.style.pointerEvents = 'none';
      color_palette_div.style.opacity = 0.6;

    }else{
      console.log('ペンモード'); //ペン
      color_palette.style.pointerEvents = 'auto';
      color_palette_div.style.opacity = 1.0;

      if (previousColors != null){
        currentColor = previousColors;
      }
      if (previousLineWidth != null){
        currentLineWidth = previousLineWidth;
        updateLineWidth(currentLineWidth);
      }
    }
  }

  initEventHandler();
  initColorPalette();

  // 文字の太さの設定を行う機能を有効にする
  initConfigOfLineWidth();
  //*--  「送信」ボタン  --*//
  // CSRF token 設定
  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
  // 保存して送信
  const button = document.getElementById("download");
  button.onclick = function() {
    let canvas = document.getElementById("draw-area");
    // console.dir(canvas)
    let base64img = canvas.toDataURL("image/jpeg");
    // document.getElementById("download").href = base64;

    // console.log(location.pathname)
    axios.post('/paint/receive/', {
      imgBase64: base64img,
      loc_path : location.pathname,
    })
    .then(function (response) {
    //   console.log(response);
      chatSocket.send(JSON.stringify({
        'id': response.data.id,
        'message': base64img
      }));
    })
    .catch(function (error) {
      console.log(error);
    });

    document.getElementById("download").href = base64img;

    // テストコード　以下２行(L267~268)　と　canvas.htmlの<ul id=test_ul><\ul>　コメント外して
    // var tag = `<li>画像です<br><br><img src="${base64img}" width="50%" height="50%"></li>`
    // $('#test_ul').prepend(tag);

    // 親ウィンドウを更新する。
    window.opener.location.reload();
    window.close();
  };

  //キャンバスに文字を描く
function drawText(){
	var canvas = document.getElementById("draw-area");
	var ctx = canvas.getContext('2d');
	var text = document.getElementById("canvas_text");
	//文字のスタイルを指定
	ctx.font = '32px serif';
	ctx.fillStyle = currentColor;

	//文字の配置を指定（左上基準にしたければtop/leftだが、文字の中心座標を指定するのでcenter
	ctx.textBaseline = 'top'; // 中心基準ならcenter
	ctx.textAlign = 'left'; // 中心基準ならcenter

	//座標を指定して文字を描く（座標は画像の中心に）
  var x = 30; //画像中心なら (canvas.width / 2)
  var y = 30; //画像中心なら (canvas.height / 2)
	ctx.fillText(text.value, x, y);
}

// 文字入力
// const text_btn = document.getElementById('input_text')
// text_btn.addEventListener('click', drawText)

const save_btn = document.getElementById('save-btn')
save_btn.addEventListener('click', showDialog)

function showDialog(){
  var dialogElement = document.getElementById('save-dialog') ;
  dialogElement.showModal();
}


const save_btn_dialog = document.getElementById('save-btn-dialog')
save_btn_dialog.addEventListener('click', savePic)

function savePic(){
  let canvas = document.getElementById("draw-area");
  var filename = document.getElementById("filename").value;

  console.dir(canvas)
  let base64 = canvas.toDataURL("image/jpeg");

  save_btn_dialog.href = base64;
  save_btn_dialog.setAttribute('download', filename || 'noname');
  save_btn_dialog.dispatchEvent(new CustomEvent('click'));
}

});
