const paint_button = document.getElementById("paint-button");

paint_button.addEventListener("click", (event) => {
  console.log("クリックされました");
  window.open('canvas.html', '', 'location=no, width=1000, height=500');
});
