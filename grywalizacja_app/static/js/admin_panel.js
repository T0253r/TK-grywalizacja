fetch('/admin/tasks')
    .then(response => response.json())
    .then(tasks => {
        console.log('Loaded tasks:', tasks);
        const no = document.createElement('img')
        no.src = './static/images/no.png'
        no.classList.add('hover:backdrop-brightness-110')
        const reject_general = document.createElement('button')
        reject_general.classList.add(`button`)
        reject_general.appendChild(no)

        const yes = document.createElement('img')
        yes.src = './static/images/yes.png'
        yes.classList.add('hover:backdrop-brightness-110')
        const accept_general = document.createElement('button')
        accept_general.classList.add(`button`)
        accept_general.appendChild(yes)

        const container = document.getElementById('admin-panel')

        tasks.forEach(task => {
            const div = document.createElement('div');
            div.classList.add(`user-rank`, 'bg-gray-400')
            div.innerHTML = `<input type='text' class="max-w-120" disabled name='user_name' value='${task['user']}'/>
                            <input type='text' class="text-right max-w-120" disabled name='user_points' value=' ${task['task']}'/>`

            const reject = reject_general.cloneNode(true)
            const accept = accept_general.cloneNode(true)

            // reject.addEventListener('click', () => {
            //     fetch('/admin/reject')
            //         .then
            // })
            // accept.addEventListener('click', () =>{
            //     fetch('/admin/accept')
            //         .then
            // })

            div.appendChild(reject)
            div.appendChild(accept)
            container.appendChild(div)
        })
    });