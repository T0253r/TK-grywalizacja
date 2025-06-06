fetch('/users')
    .then(response => response.json())
    .then(users => {
        let colors = {
            '1': 'bg-amber-400',
            '2': 'bg-slate-400',
            '3': 'bg-amber-700',
            _: 'bg-gray-400'
        }
        const container = document.getElementById('ranking')
        users.forEach((user, index) => {
            const div = document.createElement('div');
            div.classList.add(`user-rank`)
            div.classList.add(colors[(index+1).toString()] || colors._)
            div.innerHTML = `<input type='text' class="max-w-120" disabled name='user_name' value='#${index+1}  ${user['name']}'/>
                            <input type='text' class="text-right max-w-20" disabled name='user_points' value='${user['points']}'/>`
            container.appendChild(div)
        })
    }
)