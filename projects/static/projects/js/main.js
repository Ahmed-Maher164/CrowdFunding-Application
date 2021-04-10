let tagButton = document.getElementById("tagButton")
let tagConatiner = document.getElementById("tagContainer")
let commentButton = document.getElementById("commentButton")
let commentConatiner = document.getElementById("commentContainer")
let photoButton = document.getElementById("photoButton")
let photoConatiner = document.getElementById("photoContainer")
let countImg = document.getElementById("countImg")

function addTag() {
    let tag = document.createElement("input")
    tag.setAttribute("name", "tags[]")
    tagConatiner.appendChild(tag)
}

let counter = -1
function addPhoto() {
    counter++
    let photo = document.createElement("input")
    photo.setAttribute("name", "photos"+counter)
    photo.setAttribute("type", "file")
    photoConatiner.appendChild(photo)
    countImg.value = counter
}

//function addComment() {
//    let comment = document.createElement("input")
//    comment.setAttribute("name", "comments[]")
//    commentConatiner.appendChild(comment)
//}
