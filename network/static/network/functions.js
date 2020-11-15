document.addEventListener('DOMContentLoaded', function () {

    //document.querySelector('#btn-edit-post').addEventListener('click', () => edit_post());

    document.querySelectorAll('#btn-edit-post').forEach(button => {
        button.onclick = function () {
            this.style.display = "none";
            edit_post(this.dataset.page);
        }
    });

    document.querySelectorAll('#like-btn').forEach(button2 => {
        button2.onclick = function () {
            console.log("Entro al selector");
            this.style.display = "none";
            send_like(this.dataset.page);
        }
    });

});



function edit_post(id) {

    var newTextArea = document.createElement('textarea', '');
    var newButton = document.createElement('button');
    var texto = document.getElementById('text-post-' + id).innerHTML;

    document.getElementById('text-post-' + id).innerHTML = "";

    var content = document.getElementById('text-post-' + id);

    newTextArea.setAttribute('id','text-edit-area'+id);
    newTextArea.innerHTML = texto;
    newButton.setAttribute('id', 'button-edit-send-'+ id);
    newButton.innerHTML = "Editar";

    content.appendChild(newTextArea);
    content.appendChild(newButton);

    document.querySelector('#button-edit-send-' + id).addEventListener('click', () => update_post(id));
}

function update_post(id) {

    console.log('Enviando Post..');

    let data = new FormData();
    
    var text = document.querySelector('#text-edit-area'+id).value;

    data.append('id',id);
    data.append('text',text);
  
    data.append('csrfmiddlewaretoken',token);

    fetch('/update',{
        method:'POST',
        body:data,
        
        
    })
    .then(response => response.json())
    .then(result => {
         // Print result
         console.log(result);
         //load_mailbox('inbox');
       });


    document.getElementById('text-post-' + id).innerHTML = text;
    document.querySelector('#text-edit-area'+id).style.display="none";
    document.querySelector('#button-edit-send-'+ id).style.display="none";


}


function send_like(id){
    console.log(id);

    let data = new FormData();

    data.append('id',id);
  
    data.append('csrfmiddlewaretoken',token);

    fetch('/like',{
        method:'POST',
        body:data,
        
    })
    .then(response => response.json())
    .then(result => {
         // Print result
         console.log(result);
         //load_mailbox('inbox');
       });

    var count = document.getElementById('num-likes-id-'+id);
    var sum = parseInt(count.innerHTML)+1;

    count.innerHTML = sum;

    console.log("El contador es " + sum);
}

//function send_post(){
    // console.log('Enviando Post..');

    // console.log(token);
    // let data = nea "[da "[w FormData();
    // var username = document.getElementById('user-name').value;
    // var useremail = document.getElementById('user-email').value;
    // var pass= document.getElementById('user-password').value;
    // var idUser = document.getElementById('user-id').value;
    // var text = document.getElementById('post-text').value;

    // data.append('username',username);
    // data.append('email',useremail);
    // data.append('password',pass);

    // data.append('idUser', idUser);
    // data.append('text', text);
    // data.append('likes', 0 );
    // data.append('csrfmiddlewaretoken',token);

    // fetch('/post',{
    //     method:'POST',
    //     body:data,
    //     credentials: 'same-origin',
    // })
    // .then(response => response.json())
    // .then(result => {
    //      // Print result
    //      console.log(result);
    //      //load_mailbox('inbox');
    //    });


    // fetch('/post', {
    //   method: 'POST',
    //   body: JSON.stringify({
    //     username: document.getElementById('user-name').value,
    //     email: document.getElementById('user-email').value,
    //     password: document.getElementById('user-password').value,

    //     csrfmiddlewaretoken : token,

    //     userId: document.getElementById('user-id').value,
    //     text: document.getElementById('post-text').value,
    //     likes: 0,
    //   }),
    //   credentials:'same-origin',
    // })
    //   .then(response => response.json())
    //   .then(result => {
    //     // Print result
    //     console.log(result);
    //     //load_mailbox('inbox');
    //   });

//}

