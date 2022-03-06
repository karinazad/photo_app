const getCookie = key => {
    let name = key + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
};


// Stories Start |---->
const story2Html = story => {
    return `
        <div>
            <img src="${ story.user.thumb_url }" class="pic" alt="profile pic for ${ story.user.username }" />
            <p>${ story.user.username }</p>
        </div>
    `;
};

// fetch data from your API endpoint:
const displayStories = () => {
    fetch('/api/stories')
        .then(response => response.json())
        .then(stories => {
            const html = stories.map(story2Html).join('\n');
            document.querySelector('.stories').innerHTML = html;
        })
};
// <---| Stories End



// Suggestions Start |--->

const toggleFollow = ev => {
    const elem = ev.currentTarget

    if (elem.innerHTML === "unfollow") {
        unfollowUser(elem.dataset.followingId, elem);

    } else {
        followUser(elem.dataset.userId, elem);

    }
};


const followUser = (userId, elem) => {
    const postData = {
        "user_id": userId
    };

    fetch("http://127.0.0.1:5000/api/following/", {
            method: "POST",
            headers: {
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            elem.innerHTML = "unfollow";
            elem.classList.add("unfollow");
            elem.classList.remove("follow");

            elem.setAttribute("aria-checked","true")
            elem.setAttribute("data-following-id", data.id);

            console.log(`Successfully followed  ${userId}`)
         });
};

const unfollowUser = (followingId, elem) => {
    // console.log("Unfollowing a user")
    // console.log(followingId)
    const deleteURL = `http://127.0.0.1:5000/api/following/${followingId}`
    fetch(deleteURL, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        elem.innerHTML = "follow";
        elem.classList.add("follow");
        elem.classList.remove("unfollow")

        elem.setAttribute("aria-checked","false")
        elem.removeAttribute('data-following-id');

        console.log(`Successfully unfollowed  ${followingId}`)
    });

}


const user2Html = user => {
   return  `
        <div class="suggestion">
        <img src="${user.thumb_url}"/>
        <div>
            <p class="bold-font">${user.username} </p>
            <p class="small-font">suggested for you</p>
        </div>
        <div>
            <button 
                class="follow" 
                aria-label="Follow"
                aria-checked="false"
                data-user-id = "${user.id}"
                onclick = "toggleFollow(event)"
                >             
                follow
              </button>
        </div>
    </div>
    `

};

const getSuggestions = () => {
   fetch("http://127.0.0.1:5000/api/suggestions/", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        }
    })
        .then(response => response.json())
        .then(users => {
            const html = users.map(user2Html).join('')
            document.querySelector(".suggestions").innerHTML = html
        });
};



// <---| Suggestions End




// Comments Start |--->


const postComments = ev => {
    const text = document.querySelector('.comment-input').value
    const postId = ev.currentTarget.dataset.postId;

     console.log("TEXT is " + text)
    const postData = {
        "post_id": postId,
        "text": text,
    };


    fetch("http://127.0.0.1:5000/api/comments", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
             console.log("Posted a comment: " + postData)
        })
        .then( () => {
            displayPosts();
            console.log("reload");

        })

    // displayPosts();


}


const displayComments = (comments, postId) => {
    let html = '';

    if (comments.length > 1 ) {
        html += `
            <p><button class="link view-all-comments" data-post-id="${postId}" onclick = "showPostDetail(event);">
                View all ${ comments.length } comments
            </button></p>
          `;
    }
    if (comments && comments.length > 0) {
        const lastComment = comments[comments.length-1];
        html += `
            <p>
                <strong>${ lastComment.user.username }</strong>
                ${ lastComment.text }
             </p>
            <div> <p class="uppercase gray xs"> ${lastComment.display_time}</p></div>
        `
    }

    return html;
}

const likeUnlike = ev => {
    const elem = ev.currentTarget
    let heart_color = ""
    let aria_check = ""

    if (elem.dataset.likeId === "undefined") {


        const postData = {};

        fetch(`http://127.0.0.1:5000/api/posts/${elem.dataset.postId}/likes/`, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': getCookie('csrf_access_token'),
                },
                body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(data => {
                elem.setAttribute('data-like-id', data.id);

                console.log(`Created a like ${data.id}`)
            });

        heart_color = "s"
        aria_check = "true"

    } else {

        const deleteURL = `http://127.0.0.1:5000/api/posts/${elem.dataset.postId}/likes/${elem.dataset.likeId}`
        fetch(deleteURL, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            elem.setAttribute('data-like-id', "undefined");

            console.log("Removed the like")
        });

        heart_color = "r"
        aria_check = "false"
    }

    elem.innerHTML = `<i class="fa${heart_color} fa-heart fa-lg" 
                        aria-label="Follow"
                        aria-checked="${aria_check}">
                        
</i>`

};




const bookmarkUnbookmark = ev => {
    const elem = ev.currentTarget
    let bookmark_color = ""
    let aria_check = ""

    console.log(elem)

    if (elem.dataset.bookmarkId === "undefined") {
        // Create a bookmark
        const postData = {
                "post_id": parseInt(elem.dataset.postId)
            };
            fetch("http://127.0.0.1:5000/api/bookmarks/", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
                    },
                    body: JSON.stringify(postData)
                })
                .then(response => response.json())
                .then(data => {
                    elem.setAttribute('data-bookmark-id', data.id);
                    console.log(`Created a bookmark ${data.id}`)

                });
             bookmark_color = "s"
            aria_check = "true"
    } else {
        // Remove a bookmark
        fetch(`http://127.0.0.1:5000/api/bookmarks/${elem.dataset.bookmarkId}`, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': getCookie('csrf_access_token'),
            }
        })
            .then(response => response.json())
            .then(data => {
                elem.setAttribute('data-bookmark-id', "undefined");
                console.log(`Removed the bookmark`)

            });
         bookmark_color = "r"
         aria_check = "false"
    }


    elem.innerHTML = `<i 
                        class="fa${bookmark_color} fa-bookmark " 
                        aria-label="Follow"
                        aria-checked="${aria_check}">
                        
                        </i>`
};

// <button data-post-id=${post.id} onClick="updateLikes(event)">Update likes</button>

const post2Html = post => {

    return `
         <section class="card">
            <div class="header">
                <h3>${ post.user.username} 
                 </h3>
                <i class="fa fa-dots"></i>
            </div>
            <img src="${post.image_url }" alt="Image posted by ${post.user.username }" width="300" height="300">
            <div class="info">
                <div class="buttons">
                <div>
                     <button 
                     data-like-id = "${post.current_user_like_id}"
                      data-post-id = "${post.id}"
                      class = "no-border-button"
                       onclick="likeUnlike(event)">
                        <i class="fa${post.current_user_like_id ? 's' : 'r'} fa-heart fa-lg"></i>
                    </button>
                    <i class="far fa-comment"></i>
                    <i class="far fa-paper-plane"></i>
                </div>
                <div onclick="bookmarkUnbookmark(event)"
                    data-bookmark-id = "${post.current_user_bookmark_id}" 
                    data-post-id = "${post.id}">
                    <i class="fa${post.current_user_bookmark_id ? 's': 'r'} fa-bookmark"></i>
                </div>
                
                </div>                  
                
                   <p class="likes"><strong>${post.likes.length} like${post.likes.length != 1 ? "s" : ""}</strong></p>
                                
                <div class="caption">
                    <p>
                        <strong>${post.user.username }</strong>
                        ${ post.caption }
                    </p>
                    <div> <p class="uppercase gray xs"> ${post.display_time}</p></div>
                </div>
                
                 <div class="comments">
                    ${displayComments(post.comments, post.id)}
                    
                    <div class="add-comment">
                      
                            <input class = "comment-input" data-post-id="${post.id}" type="text" aria-label="Add a comment"
                               placeholder="Add a comment...">

                        <button
                            class="link" data-post-id="${post.id}" onclick="postComments(event)">Post
                        </button>
                    </div>
           
                </div>
            </div>
         </section>
    `;

}


// fetch data from your API endpoint:
const displayPosts = limit => {
    fetch('/api/posts')
        .then(response => response.json())
        .then(posts => {
            const html = posts.map(post2Html).join('\n');
            console.log(posts);
            document.querySelector('#posts').innerHTML = html;
        })
};

// <---| Comments End



const destroyModal = ev => {
    const elem = ev.currentTarget
    elem.setAttribute("aria-check", "false")
    document.querySelector('#modal-container').innerHTML = "";
    document.querySelector('.view-all-comments').focus()
}


const showPostDetail = ev => {
    const postId = ev.currentTarget.dataset.postId;
    console.log("post id:")
    console.log(postId)
    fetch(`/api/posts/${postId}`)
        .then(response => response.json())
        .then(post => {
            console.log(post)
            console.log(post.image_url)

            const html = `
                     <div class ="modal-bg">
                        <button onclick="destroyModal(event)" class="modal-close-button" aria-label="Modal Open" aria-check="true" autofocus>
                        X </button>
                        
                        <div class="modal">
                            <img class = "modal center-img"src="${post.image_url}" />
                                
                              <div class="modal-left">
                                <div class ="modal-user">
                                    ${displayModalUser()}
                                </div>                             
                                <div class = "model-comments"> 
                                 ${displayModalComments(post.comments, post.id)}
                                </div>
                                 
                             </div>
                        </div>
                    </div>`;


            document.querySelector('#modal-container').innerHTML =  html;
            document.querySelector('.modal-close-button').focus()
        })
};


const displayModalComments = (comments, id) => {
    console.log("displayModalComments", comments, id)
    console.log(typeof commments)

    let html = ""

    for (let i = 0; i < comments.length; i++) {
        comment = comments[i]
          html += `
            <div class="modal-comment">
                  <div>
                        <img src = ${comment.user.thumb_url} />
                  </div>
                  <div>
                        <p> <strong>${comment.user.username}</strong></p>
                          <p>  ${comment.text}</p>
                          <p class="uppercase gray xs">${comment.display_time}</p>
                  </div>
                  <div>
                        <i class="far fa-heart"></i>
                   </div>
                   
        </div>
    `
    }


    return html
}


const displayModalUser = () => {

    fetch("http://127.0.0.1:5000/api/profile/", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            // 'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        }
    })
    .then(response => response.json())
    .then(user => {
        console.log(user);

        const html = `
        <div class ="modal-user">
            <img src="${user.thumb_url}" class="modal-user-pic" alt="Profile pic for ${user.username}"/>
            <h2>${user.username}</h2>
             </div>
         `
        document.querySelector(".modal-user").innerHTML = html
    });
}





const displayProfile = () => {
    fetch("http://127.0.0.1:5000/api/profile/", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            // 'X-CSRF-TOKEN': getCookie('csrf_access_token'),
        }
    })
    .then(response => response.json())
    .then(user => {
        console.log(user);

        const html = `
            <img src="${ user.thumb_url}" class="pic" alt="Profile pic for ${user.username}"/>
            <h2>${user.username}</h2>
      `
        document.querySelector(".user").innerHTML = html
    });

}



const initPage = () => {
    displayProfile();
    displayStories();
    getSuggestions();
    displayPosts();
};


initPage()
