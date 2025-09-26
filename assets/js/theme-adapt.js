function adjustTextColor() {
  const body = document.body;
  const bgColor = window.getComputedStyle(body).backgroundColor;

  // 提取RGB
  const rgb = bgColor.match(/\d+/g);
  const brightness = (rgb[0]*299 + rgb[1]*587 + rgb[2]*114) / 1000;

  if (brightness < 125) {
    body.classList.add("light-text");
  } else {
    body.classList.add("dark-text");
  }
}

window.onload = adjustTextColor;
