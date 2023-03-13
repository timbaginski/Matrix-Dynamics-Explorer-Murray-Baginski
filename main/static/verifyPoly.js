async function verifyPoly() {
    let polynomial = document.getElementById('polynomial').value; 

    // We must convert any plus signs 
    polynomial = convertPlusSigns(polynomial);

    const response = await fetch('http://localhost:8000/verifyPoly/?polynomial=' + polynomial); 
    let responseJSON = await response.json(); 

    let usernametext = document.getElementById('usernametext');

    if(responseJSON['message'] == 'Valid') {
        // We change the text to green, indicating a valid poly
        console.log(usernametext.style);
        usernametext.style.color = 'green';
    }

    // Set the text's content to the message
    usernametext.innerHTML = responseJSON["message"]; 
}

function convertPlusSigns(polynomial) {
    for(let i = 0; i < polynomial.length; i++) {
        if(polynomial.charAt(i) == '+') {
            let temp = polynomial.substring(0, i) + '%2B'; 
            if(i < polynomial.length - 1) {
                temp += polynomial.substring(i+1, polynomial.length);
            }
            polynomial = temp; 
        }
    }   

    return polynomial;
}