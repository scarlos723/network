document.addEventListener('DOMContentLoaded', function () {

    //document.querySelector('#btn-edit-post').addEventListener('click', () => edit_post());

    document.querySelectorAll('#btn-edit-post').forEach(button => {
        button.onclick = function () {
            this.style.display = "none";
            edit_post(this.dataset.page);
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

    console.log(token);
    let data = new FormData();
    
    var text = document.querySelector('#text-edit-area'+id).value;

    console.log(text);

    data.append('id',id);
    data.append('text',text);
  
    data.append('csrfmiddlewaretoken',token);

    fetch('/update',{
        method:'POST',
        body:data,
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": token
        }
    })
    .then(response => response.json())
    .then(result => {
         // Print result
         console.log(result);
         //load_mailbox('inbox');
       });

}




//function send_post(){
    // console.log('Enviando Post..');

    // console.log(token);
    // let data = new FormData();
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

