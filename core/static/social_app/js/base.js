function editPost(id, body, page){
    document.getElementById("edit_post_id").value = id;
    document.getElementById("edit_post_body").value = body;
    document.getElementById("edit_post_page").value = page;
}
function addComment(id, page){
    console.log(id)
    document.getElementById("comment_id").value = id;
    document.getElementById("page_id").value = page;
    let commentsContainer = document.getElementById('comments_container');
    commentsContainer.innerHTML = "";
    fetch(`/fetch-comments/${id}`)
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 'success') {
            let commentsHtml = "";
            data.comments.forEach((comment) => {
                commentsHtml += `
                    <div class="card mb-3">
                        <div class="card-body">
                            <div class="d-flex align-items-start">
                            <img src="${comment.image}"
                            height="45px" class="rounded-circle me-3" alt="User Profile
                            Picture">
                            <div>
                                <h4 class="h6 mb-1">${comment.name}</h4>
                                <p class="mb-2">
                                ${comment.body}
                                </p>
                            </div>
                            </div>
                            <!-- Like and Reply Buttons -->
                            <div class="d-flex align-items-center mt-3">
                            <button class="btn btn-outline-primary btn-sm me-2">Like</button>
                            <button class="btn btn-outline-secondary btn-sm me-3">Reply</button>
                            <span class="text-muted small">${comment.time} ago</span>
                        </div>
                    </div>
                </div>
                `
            })
            commentsContainer.innerHTML = commentsHtml;
        }
    })
} 
function postLike(id){
    const like_btn = document.getElementById(`like_button${id}`);
    const likeCount = document.getElementById(`likes_count_${id}`);
    fetch(`/post_like/${id}`)
    .then((response) => response.json())
    .then((data) => {


        if (data.liked){
            like_btn.classList.add('text-danger');
        }
        else{
            like_btn.classList.remove('text-danger');
        }
        likeCount.textContent = data.total_likes;
        console.log(data.message);

    })
}