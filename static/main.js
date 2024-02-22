document
  .getElementById("file-input")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    var file = document.getElementById("myFile").files[0];
    if (file) {
      var reader = new FileReader();
      reader.onload = function (event) {
        var imageUrl = event.target.result;
        var image = new Image();
        image.src = imageUrl;
        image.onload = function () {
          drawImageWithBoundingBox(image);
          // send image to model for processing
          // assuming model returns the result synchronously
          var result = detectHairLossStage(imageUrl);
          displayResult(result);
        };
      };
      reader.readAsDataURL(file);
    }
  });

const fileInput = document.getElementById("myFile");

// async function postData() {
//   const url = "https://stg.api.mosaicwellness.in/doctrina/predict";
//   const formdata = new FormData();
//   formdata.append("image", fileInput.files[0], "file");
//   formdata.append("imageId", "12");
//   formdata.append("modelId", "werg");
//   formdata.append("brand", "MM");
//   formdata.append("category", "wdv");
//   formdata.append("userId", "50000625");
//   formdata.append("appointmentId", "2");

//   const requestOptions = {
//     method: "POST",
//     body: formdata,
//     redirect: "follow",
//   };

//   fetch("https://stg.api.mosaicwellness.in/doctrina/predict", requestOptions)
//     .then((response) => response.text())
//     .then((result) => console.log(result))
//     .catch((error) => console.error(error));
// }

function drawImageWithBoundingBox(image) {
  var canvas = document.getElementById("image-preview");
  var ctx = canvas.getContext("2d");
  canvas.width = image.width;
  canvas.height = image.height;
  ctx.drawImage(image, 0, 0);

  // coordinates from backend
  var boundingBox = { x: 450, y: 300, width: 700, height: 450 };

  setTimeout(function () {
    // top left corner circle
    drawCircularMarker(ctx, boundingBox.x, boundingBox.y);

    setTimeout(function () {
      // the top right corner clircle
      drawCircularMarker(ctx, boundingBox.x + boundingBox.width, boundingBox.y);

      setTimeout(function () {
        // bottom right corner
        drawCircularMarker(
          ctx,
          boundingBox.x + boundingBox.width,
          boundingBox.y + boundingBox.height
        );
        setTimeout(function () {
          // bottom left corner
          drawCircularMarker(
            ctx,
            boundingBox.x,
            boundingBox.y + boundingBox.height
          );
        }, 250);
      }, 250);
    }, 250);
  }, 250);

  setTimeout(function () {
    // bounding box
    ctx.strokeStyle = "#00ff00";
    ctx.lineWidth = 17;
    ctx.strokeRect(
      boundingBox.x,
      boundingBox.y,
      boundingBox.width,
      boundingBox.height
    );
  }, 1250);
}

// corner circle markers
function drawCircularMarker(ctx, x, y) {
  var markerSize = 20;
  ctx.fillStyle = "#00ff00";
  ctx.beginPath();
  ctx.arc(x, y, markerSize, 0, Math.PI * 2);
  ctx.fill();
}

function detectHairLossStage(imageUrl) {
  // send the image to your model for processing
  // and get the result back for demo purpose,
  var stages = ["Stage 2", "Stage 3", "Stage 4"];
  var randomStageIndex = Math.floor(Math.random() * stages.length);
  return stages[randomStageIndex];
}

function displayResult(result) {
  document.getElementById("result").innerHTML =
    '<span><img src="/static/notepad.png" class="resultlogo" alt="Image Icon">You are at ' +
    result +
    " of hair loss</span>";
}
