window.onload = () => {
    // lesson-detail
    let lessonElem = document.getElementsByClassName('lesson-detail')
    if (lessonElem.length === 1) {
        for (const el of lessonElem[0].children) {
            if (el.id && /^lesson-\w+-block$/.test(el.id)) {
                el.classList.remove('hidden')
                break
            }
        }
    }

    // ticket form
    const formEl = document.getElementById('footer-questions-form')
    if (formEl) {
        formEl.onsubmit = (e) => {
            e.preventDefault()
            fetch('/tickets/', {
                method: 'POST',
                body: new FormData(formEl),
            }).then((resp) => {
                if (resp.status === 200) {
                    e.target.reset()
                    alert('Ваше сообщение отправлено!')
                } else {
                    alert('Произошла ошибка при отправке сообщения!')
                }
            }).catch((err) => {
                alert('Произошла ошибка при отправке сообщения!')
            })
        }
    }
}

const changeActiveContentBlock = (blockId) => {
    for (const el of document.getElementsByClassName('lesson-detail')[0].children) {
        if (el.id && /^lesson-\w+-block$/.test(el.id)) {
            el.id === blockId
                ? el.classList.remove('hidden')
                : el.classList.add('hidden')
        }
    }
}
