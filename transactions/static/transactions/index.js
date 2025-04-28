
        //function calls
        requestQuestion()


        const form = document.getElementById('profile-form')
        form.addEventListener('submit', (e) => {
            e.preventDefault()
            const btn = document.getElementById('proceed')

            btn.disabled = true
            const firstName = document.getElementById('first-name')
            const lastName = document.getElementById('last-name')

            if(firstName.value.trim().length < 2 || lastName.value.trim() === ''){
                alert('all fields are required')
               
                return
            }

            authenticate().then((data) => {
                if(!data.id){
                    return
                }
                saveProfile(firstName, lastName)
            })
            btn.disabled = false

        })

        // authentication 
        async function authenticate(){
            try{
                const response = await fetch('/blog/check-auth/')
                const data = await response.json()

                if(!response.ok){
                    throw new Error('server error')
                }
                if(data.error){
                    alert(data.error)
                    return false
                }
                else if(data.success){
                    return {id:data.id, isVerified:data.is_verified}
                }
                else{
                    return false
                }
            }
            catch(error){
                alert(error.message)
                return false
            }
        }

        //save profile
        function saveProfile(x, y){
            const formData = new FormData()
            formData.append('firstName', x.value,)
            formData.append('lastName', y.value)
            fetch('/transactions/save-profile/', {
                method: 'POST',
                headers: {
                    'X-csrftoken': get_token('csrftoken'),
                },
                body: formData
            })
            .then(async response => {
                const data = await response.json()
                if(!response.ok){
                    throw new Error('server error')
                }
                if(!data.success){
                    throw new Error(data.error)
                }
                document.querySelector('.verify-pro').style.display = 'none'
                window.location.reload()
                requestQuestion()
            })
            .catch(error => alert(error.message))
        }

        //request for question
        function requestQuestion(){
            if((!document.querySelector('.verify-pro') || document.querySelector('.verify-pro').style.display === 'none') && document.querySelector('.question-lab')){

                fetch('/transactions/request-question')
                .then(async response => {
                    const data = await response.json()
                    if(!response.ok){
                        throw new Error('server error')
                    }
                    if(!data.success){
                        throw new Error(data.error)
                    }
                    document.getElementById('qs').textContent = data.question
                    document.querySelector('.question-lab').style.display = 'block'
                })
                .catch(error => alert(error.message))

                const ans = document.getElementById('ans').addEventListener('submit', (e) => {
                    e.preventDefault()
                    const value = document.getElementById('answer')
                    try{
                        const v = Number(value.value)
                        if(!v){
                            alert('enter a valid number')
                            return
                        }
                        const btn = document.getElementById('ansbtn')
                        btn.disabled = true
                        submitAnswer(value, btn)

                    }
                    catch(error){
                        alert(error.message)
                        return
                    }
                    
                })

            }
            
        }

        //submit answer 

        function submitAnswer(x, y){
            y.disabled = true
            const formData = new FormData()
            formData.append('answer', x.value)
            fetch('/transactions/submit-answer/', {
                method: 'POST',
                headers: {
                    'X-csrftoken': get_token('csrftoken'),
                },
                body: formData
            })
            .then(async response => {
                const data = await response.json()
                if(!response.ok){
                    throw new Error('server error')
                }
                if(!data.success){
                    throw new Error(data.error)
                }
                document.querySelector('.question-lab').style.display = 'none'
                alert(data.result)
                x.value = ''

            })
            .catch(error => {
                alert(error.message)
                setTimeout(() => {
                   window.location.reload() 
                }, 500);

            })
            
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



        