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


// Posts
// 1. get post data from the API endpoint (/api/posts?limit=10
// 2. when the data arrives, build HTML cards (string)
// 3. update the container and put the html inside of it


/*
            <div class="comments">
                {% if post.comments')|length > 1 %}
                    <p><button class="link">View all {{ post.get('comments')|length }} comments</button></p>
                {% endif %}
                {% for comment in post.get('comments')[:1] %}
                    <p>
                        <strong>{{ comment.get('user').get('username') }}</strong>
                        {{ comment.get('text') }}
                    </p>
                {% endfor %}
                <p class="timestamp">{{ post.get('display_time') }}</p>
            </div>
        </div>
        <div class="add-comment">
            <div class="input-holder">
                <input type="text" aria-label="Add a comment" placeholder="Add a comment...">
            </div>
            <button class="link">Post</button>
        </div>
    </section>
*/

const likeUnlike = ev => {
    console.log('like ')
}

const displayComments = comments => {
    let html = '';

    if (comments.length > 1 ) {
        html += `
            <p><button class="link">View all ${ comments.length } comments
            </button></p>
          `;
    }
    if (comments && comments.length >0) {
        const lastComment = comments[comments.length-1];
        html += `
            <p>
                <strong>${ lastComment.user.username }</strong>
                ${ lastComment.text }
             </p>
            <div>${lastComment.display_time}</div>
        `
    }

    html += `
        <div class="add-comment">
            <div class="input-holder">
                <input type="text" aria-label="Add a comment" placeholder="Add a comment...">
            </div>
            <button class="link">Post</button>
        </div>
    `

    return html;

}

const post2Html = post => {
    return `
         <section class="card">
            <div class="header">
                <h3>${ post.user.username} - </h3>
                <i class="fa fa-dots"></i>
            </div>
            <img src="${post.image_url }" alt="Image posted by ${post.user.username }" width="300" height="300">
            <div class="info">
                <div class="buttons">
                <div>
                     <button onclik="likeUnlike(event)">
                        <i class="fa${post.current_user_like_id ? 's' : 'r'} fa-heart"></i>
                    </button>
                    <i class="far fa-comment"></i>
                    <i class="far fa-paper-plane"></i>
                </div>
                <div>
                    <i class="fa${post.current_user_bookmark_id ? 's': 'r'} fa-bookmark"></i>
                </div>
                
                </div>
                 <p class="likes"><strong>${post.likes.length } like${post.likes.length != 1 ? "s": ""}</strong></p>
                <div class="caption">
                    <p>
                        <strong>${post.user.username }</strong>
                        ${ post.caption }
                    </p>
                </div>
                
                 <div class="comments">
                    ${displayComments(post.comments)}
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

const initPage = () => {
    displayStories();
    displayPosts();
};

// invoke init page to display stories:
initPage();