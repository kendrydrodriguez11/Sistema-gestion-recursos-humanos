
const fetchPost = async (url, data) => {
    console.log(url)
    try {
        const res = await fetch(url,
            {
                method: 'POST',
                headers: {
                    'X-CSRFToken': Cookies.get('csrftoken')
                },
                body: data instanceof FormData
                    ? data
                    : JSON.stringify(data)
            });
        const post = await res.json()

        return { "ok": true, "data": post }
    } catch (error) {
        return { "ok": false, "data": error }
    }
};
const fetchGet = async (url) => {
    console.log(url)
    try {
        const res = await fetch(url,
            {
                method: 'GET', headers: { 'Content-Type': 'application/json' }
            })
        const data = await res.json()
        console.log(data)
        return { "ok": true, "data": data }
    } catch (error) {
        return { "ok": false, "data": error }
    }
};