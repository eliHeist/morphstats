// declare let checklistPage: boolean

//#region facilitator checklist

async function getFacilitators(url: string) {
    url = `${url}?format=json`

    const response = await fetch(url)
    return await response.json();
}

async function getServices(url: string) {
    url = `${url}?format=json`

    const response = await fetch(url)
    return await response.json();
}

async function udpadeFacilitators(url:string, service:object, csrf: string) {
    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify(service),
    })
    const data = await response.json();
    console.log(data);
}

function handleWildChecks(available: string, absent: string) { 
    const avcont = document.querySelector(`.${available}`)
    const abcont = document.querySelector(`.${absent}`)

    avcont?.querySelectorAll('input').forEach((input) => {
        if (!input.classList.contains('checked')) {
            input.classList.add('checked')
        }
    })
    abcont?.querySelectorAll('input').forEach((input) => {
        if (input.classList.contains('checked')) {
            input.classList.remove('checked')
        }
    })
    return true
}

function CheckActions(facilitator: object, isAvailable: boolean, active_facilitators: Array<object>, inactive_facilitators: Array<object>) {
    if (isAvailable) {
        let index = active_facilitators.indexOf(facilitator)
        active_facilitators.splice(index, 1)
        inactive_facilitators.push(facilitator)
    }
    else {
        let index = inactive_facilitators.indexOf(facilitator)
        inactive_facilitators.splice(index, 1)
        active_facilitators.push(facilitator)
    }
    return handleWildChecks('available', 'absent')
}

//#endregion facilitator checklist