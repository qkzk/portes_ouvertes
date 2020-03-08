var video;
var r = 170;
var g = 85;
var b = 0;
var counter = 0;
let buttonReset;
let buttonTint;
let buttonCyan;
let buttonJaune;
let buttonMagenta;
let buttonPicture;
let gotPicture = false;
let photo;
let invert;
let dither = false;
let doneDithering = false;
let isGray = false;

function setup() {
  createCanvas(640, 480);
  background(51);
  video = createCapture(VIDEO);
  video.size(640, 480);
  video.hide();

  buttonReset = createButton('reset');
  buttonReset.position(10, 840);
  buttonReset.mousePressed(resetVideo);

  buttonTint = createButton('Teinte aléatoire');
  buttonTint.position(80, 840);
  buttonTint.mousePressed(changeTint);

  buttonMagenta = createButton('magenta');
  buttonMagenta.position(200, 840);
  buttonMagenta.mousePressed(magenta);

  buttonJaune = createButton('jaune');
  buttonJaune.position(280, 840);
  buttonJaune.mousePressed(jaune);

  buttonCyan = createButton('cyan');
  buttonCyan.position(340, 840);
  buttonCyan.mousePressed(cyan);

  buttonInvert = createButton('Négatif')
  buttonInvert.position(400, 840);
  buttonInvert.mousePressed(negatif);

  buttonGray = createButton('gris')
  buttonGray.position(480, 840);
  buttonGray.mousePressed(grayImage);

  buttonPicture = createButton('Souriez !')
  buttonPicture.position(530, 840);
  buttonPicture.mousePressed(takePicture);

  buttonDithering = createButton('Flou')
  buttonDithering.position(610, 840);
  buttonDithering.mousePressed(dithering);
}

function resetVideo() {
  tint(255, 255, 255);
  gotPicture = false;
  invert = false;
  dither = false;
  doneDithering = false;
  isGray = false;
}

function changeTint () {
  let r = random(255);
  let g = random(255);
  let b = random(255);

  tint(r, g, b);
}

function magenta () {
  let r = 255;
  let g = 0;
  let b = 255;

  tint(r, g, b);
}

function jaune () {
  let r = 255;
  let g = 255;
  let b = 0;

  tint(r, g, b);
}

function cyan () {
  let r = 0;
  let g = 255;
  let b = 255;

  tint(r, g, b);
}

function next(c) {
  return (c + 1) % 255;
}

function takePicture() {
  tint(r, g, b);
  photo = video.get(0, 0, width, height);
  gotPicture = true;
}

function negatif() {
  invert = !invert;
}

function grayImage() {
  isGray = !isGray;
}

function dithering() {
  dither = true;
}

function draw() {
  if (gotPicture) {
    image(photo, 0, 0, width, height);
  }
  else if (dither) {
    if (!doneDithering) {
      img = makeDithered(video, 1);
      doneDithering = true;
    }
    image(img, 0, 0, width, height);
    // Apply gray filter to the whole canvas
  }
  else {
    image(video, 0, 0, width, height);
  }
  if (invert){
    filter(INVERT);
  }
  if (isGray) {
    filter(GRAY);
  }
}

function imageIndex(img, x, y) {
  return 4 * (x + y * img.width);
}

function getColorAtindex(img, x, y) {
  let idx = imageIndex(img, x, y);
  let pix = img.pixels;
  let red = pix[idx];
  let green = pix[idx + 1];
  let blue = pix[idx + 2];
  let alpha = pix[idx + 3];
  return color(red, green, blue, alpha);
}

function setColorAtIndex(img, x, y, clr) {
  let idx = imageIndex(img, x, y);

  let pix = img.pixels;
  pix[idx] = red(clr);
  pix[idx + 1] = green(clr);
  pix[idx + 2] = blue(clr);
  pix[idx + 3] = alpha(clr);
}

// Finds the closest step for a given value
// The step 0 is always included, so the number of steps
// is actually steps + 1
function closestStep(max, steps, value) {
  return round((steps * value) / 255) * floor(255 / steps);
}

function makeDithered(img, steps) {
  tint(255);
  img = video.get(0, 0, width, height);

  img.loadPixels();

  for (let y = 0; y < img.height; y++) {
    for (let x = 0; x < img.width; x++) {
      let clr = getColorAtindex(img, x, y);
      let oldR = red(clr);
      let oldG = green(clr);
      let oldB = blue(clr);
      let newR = closestStep(255, steps, oldR);
      let newG = closestStep(255, steps, oldG);
      let newB = closestStep(255, steps, oldB);

      let newClr = color(newR, newG, newB);
      setColorAtIndex(img, x, y, newClr);

      let errR = oldR - newR;
      let errG = oldG - newG;
      let errB = oldB - newB;

      distributeError(img, x, y, errR, errG, errB);
    }
  }

  img.updatePixels();
  return img;
}

function distributeError(img, x, y, errR, errG, errB) {
  addError(img, 7 / 16.0, x + 1, y, errR, errG, errB);
  addError(img, 3 / 16.0, x - 1, y + 1, errR, errG, errB);
  addError(img, 5 / 16.0, x, y + 1, errR, errG, errB);
  addError(img, 1 / 16.0, x + 1, y + 1, errR, errG, errB);
}

function addError(img, factor, x, y, errR, errG, errB) {
  if (x < 0 || x >= img.width || y < 0 || y >= img.height) return;
  let clr = getColorAtindex(img, x, y);
  let r = red(clr);
  let g = green(clr);
  let b = blue(clr);
  clr.setRed(r + errR * factor);
  clr.setGreen(g + errG * factor);
  clr.setBlue(b + errB * factor);

  setColorAtIndex(img, x, y, clr);
}
