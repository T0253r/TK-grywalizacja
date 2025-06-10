fetch('/admin/tasks')
    .then(response => response.json())
    .then(tasks => {
        console.log('Loaded tasks:', tasks);
        const no = document.createElement('img')
        no.src = './static/images/no.png'
        no.classList.add('hover:brightness-140')
        const reject_general = document.createElement('button')
        reject_general.classList.add(`button`)
        reject_general.appendChild(no)

        const yes = document.createElement('img')
        yes.src = './static/images/yes.png'
        yes.classList.add('hover:brightness-130')
        const accept_general = document.createElement('button')
        accept_general.classList.add(`button`)
        accept_general.appendChild(yes)

        const container = document.getElementById('admin-panel')
        container.style.scrollbarGutter = 'stable'

        tasks.forEach(task => {
            const div = document.createElement('div');
            div.classList.add(`user-rank`, 'bg-gray-400')
            div.innerHTML = `<input type='text' class="max-w-60" disabled name='user_name' value='${task['user']}'/>
                            <input type='text' class="text-right max-w-90 mr-2.5" disabled name='user_points' value='${task['task']}'/>`
            console.log(task['user_id'])
            const reject = reject_general.cloneNode(true)
            const accept = accept_general.cloneNode(true)

            reject.addEventListener('click', () => {
                fetch('/admin/reject', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: task['user_id'],
                        task_id: task['task_id'],
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('python code threw an error')
                        }
                        return response.json()
                    })
                    .then(response => {
                        div.remove()
                    })
            })
            accept.addEventListener('click', () => {
                fetch('/admin/accept', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: task['user_id'],
                        task_id: task['task_id'],
                    })
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('python code threw an error')
                        }
                        return response.json()
                    })
                    .then(response => {
                        div.remove()
                    })
            })

            div.appendChild(reject)
            div.appendChild(accept)
            container.appendChild(div)
        })
        container.addEventListener('wheel', function (e) {
            if (e.deltaY !== 0) {
                e.preventDefault();
                container.scrollTop += e.deltaY;
            }
        }, {passive: false});
    });