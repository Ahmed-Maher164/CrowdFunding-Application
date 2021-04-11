let tagButton = document.getElementById("tagButton")
let tagConatiner = document.getElementById("tagContainer")
let photoButton = document.getElementById("photoButton")
let photoConatiner = document.getElementById("photoContainer")
let countImg = document.getElementById("countImg")

function addTag() {
    let tag = document.createElement("input")
    tag.setAttribute("name", "tags[]")
    tag.setAttribute("placeholder", "Add Tag")

    tagConatiner.appendChild(tag)

}

let counter = -1
function addPhoto() {
console.log("test")
    counter++
    let photo = document.createElement("input")
    photo.setAttribute("name", "photos"+counter)
    photo.setAttribute("type", "file")
    photo.required=true

    photoConatiner.appendChild(photo)
    countImg.value = counter
}



