async function verifyFile() {
    // get the uploaded file
    let fileInput = document.getElementsByName("csv")[0];
    let file = fileInput.files[0];
    console.log("Verifying...");
    const response = await fetch('http://localhost:8000/verifyFile/?filename=' + file); 
    let responseJSON = await response.json(); 

    let usernametext = document.getElementById('usernametext');

    if(responseJSON['message'] == 'Valid') {
        // We change the text to green, indicating a valid file
        console.log(usernametext.style);
        usernametext.style.color = 'green';
    }

    // Set the text's content to the message
    usernametext.innerHTML = responseJSON["message"]; 
}
