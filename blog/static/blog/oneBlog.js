const csrfToken = get_token('csrftoken')
        const likeBtns = document.querySelectorAll('.like-btn')
        likeBtns.forEach((likeBtn) => {
            likeBtn.addEventListener('click', (e) => {
                const target = e.target
                const id = target.dataset.id
                likeBlog(id, target)
            })
        })

        async function likeBlog(x, y){
            authenticate().then(data => {
                if(data.id){

                    fetch(`/blog/like-blog/${x}/`, {
                            method:'POST',
                            headers: {
                                'X-Csrftoken': csrfToken,
                            },
                        })
                        .then(async response => {
                            const data = await response.json()
                            if(!response.ok){
                                throw new Error('unable to perform operation')
                            }
                            if(data.success){

                                if(data.liked){
                                    y.textContent = `${data.value} Unlike`
                                    await reloadLike(data.likes)
                                }
                                if(!data.liked){
                                    y.textContent = `${data.value} Like`
                                    await reloadLike(data.likes)
                                }
                            }
                            if(data.error){
                                throw new Error(data.error)
                            }
                        }).catch(error => alert(error.message))
                }
            })
        }


        //uauthentication function
        async function authenticate(){
            try{
                const response = await fetch('/blog/check-auth/')
                const data = await response.json()
                if(!response.ok){
                    throw new Error('server error')
                }
                if(data.error){
                    throw new Error(data.error)
                }
                if(data.success){
                    return {id: data.id}
                }
            }
            catch(error){
                alert(error.message)
            }
            

        }

        //reload likes function
        async function reloadLike(x){
            const likes = x
            const toPut = likes.map((like) => {
                return `<span>${like}, </span> `
            }).join('')
            document.querySelector('.likers').innerHTML = toPut
        }

        //comment submit
        const commentForm = document.getElementById('comment')
        commentForm.addEventListener('submit', (e) => {
            e.preventDefault()
            const target = e.target.dataset.id
            const message = document.getElementById('message')
            if(message.value.trim().length < 2){
                alert('enter at least two characters')
                return
            }
            authenticate().then(data => {
                if(!data.id){
                    return
                }
                createMessage(message.value.trim(), target)
                message.value = ''
            })
        })

        //create message function
        function createMessage(x, y){
            const formData = new FormData()
            formData.append('comment', x)
            fetch(`/blog/make-comment/${y}/`, {
                method: 'POST',
                headers: {
                    'X-Csrftoken':csrfToken,
                },
                body: formData
            })
            .then(async response => {
                const data = await response.json()
                if(!response.ok){
                    throw new Error('error from server')
                }
                if(data.error){
                    throw new Error(data.error)
                }
                if(data.success){
                    document.getElementById('comment-count').textContent = data.count
                    reloadComment(data.comment)
                }
            })
            .catch(error => alert(error.message))
        }

        //refresh comments
        function reloadComment(x){
            const result = x.map((comment) => {
                return `<span>${comment.user} => ${comment.comment},</span><br>`
            }).join('')
            document.querySelector('.comments').innerHTML = result
        }


        //csrf token generator
        function get_token(name) {
               let cookieValue = null;
               if (document.cookie && document.cookie !== '') {
                  const cookies = document.cookie.split(';');
                  for (let i = 0; i < cookies.length; i++) {
                      const cookie = cookies[i].trim();
                      // Check if this cookie starts with the desired name
                      if (cookie.startsWith(name + '=')) {
                          cookieValue = cookie.substring(name.length + 1);
                          break;
                      }
                  }
               }
            return cookieValue;
        }
