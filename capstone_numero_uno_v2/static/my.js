$(document).ready(function(){

// -----------------------------------------------------------------------------------> 

/* Main Menu Functionality */

    const backButton = document.getElementById( 'back-button' );
    
    backButton.addEventListener( 'click', function(){

        history.back();

    })

/*  Get Pages DOM Manipulation */

    // Turn the 'text response' into an real html response 
    if (document.getElementById('wiki-page')) {
        const html = document.getElementById('wiki-page')
        html.innerHTML = html.innerText

    }
    
    // Ensure that the nav url's are set to local http://127.0.0.1:5000/, for some reason when creating an html response for a page the default will change to en.wikipedia.org
    const base = document.getElementsByTagName('base')
    for ( let i of base ) {
        i.setAttribute('href', 'http://127.0.0.1:5000/')
    }



// -------------------------------------------------------------------------------------->

/*  Search Pages DOM Manipulation */
 
    const pages = document.querySelectorAll( '[class = "form-control border border-info"]' );
    
    for ( let page of pages ){
        page.addEventListener( 'mouseenter', function (){
            page.style.padding = '15px'
            page.setAttribute( 'class', 'form-control border-2 border-info bg-dark text-light')
        });
    
        page.addEventListener( 'mouseleave', function (){
            page.style.padding = ''
            page.setAttribute( 'class', 'form-control border border-info' )
        });
    }
    

})














