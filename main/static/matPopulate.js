async function matPopulate() {
    // get the selected matrix size
    let size = parseInt(document.getElementById("matrixSize").value);
    let maxVal = 20;
    // iterate over each row and column of the matrix
    for (var i = 0; i < size; i++) {
      for (var j = 0; j < size; j++) {
        // generate a random number between 0 and maxVal
        var rand = Math.floor(Math.random() * maxVal+1);
  
        // set the value of the input field at this position
        document.getElementsByName(i.toString() + j.toString())[0].value = rand;
      }
    }
  }